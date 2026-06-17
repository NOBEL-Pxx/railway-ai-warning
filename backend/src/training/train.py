"""
模型训练脚本
支持 MambaSwin-UNet-STA 和 LoongClaw 动态路由框架
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, random_split
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import TensorBoardLogger, WandbLogger
from omegaconf import DictConfig, OmegaConf
from typing import Optional, Dict, Any, Tuple, List
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class PrecipitationDataset(Dataset):
    """降水预报数据集"""
    
    def __init__(self, 
                 data_path: str, 
                 time_steps: int = 6, 
                 forecast_steps: int = 6,
                 variables: List[str] = None,
                 transform=None,
                 mode: str = 'train'):
        """
        Args:
            data_path: 数据路径 (包含 .npy 或 .nc 文件)
            time_steps: 输入时间步数
            forecast_steps: 预报时间步数
            variables: 输入变量列表
            transform: 数据增强
            mode: 'train', 'val', 'test'
        """
        self.data_path = Path(data_path)
        self.time_steps = time_steps
        self.forecast_steps = forecast_steps
        self.variables = variables or ['precipitation']
        self.transform = transform
        self.mode = mode
        
        # 扫描数据文件
        self.samples = self._scan_samples()
        
        # 缓存
        self.cache = {}
        
    def _scan_samples(self) -> List[dict]:
        """扫描可用样本"""
        samples = []
        
        if self.data_path.exists():
            # 查找 .npy 文件
            npy_files = list(self.data_path.glob("**/*.npy"))
            
            for f in npy_files:
                samples.append({
                    'path': str(f),
                    'type': 'npy'
                })
            
            # 查找 .nc 文件
            nc_files = list(self.data_path.glob("**/*.nc"))
            for f in nc_files:
                samples.append({
                    'path': str(f),
                    'type': 'nc'
                })
        
        if not samples:
            # 没有实际数据时，生成虚拟数据用于测试
            print(f"   警告: {self.data_path} 中未找到数据文件，使用虚拟数据")
            samples = [{'path': 'dummy', 'type': 'dummy'}] * 100
        
        return samples
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        if sample['type'] == 'dummy':
            # 生成虚拟数据
            x = torch.randn(self.time_steps, len(self.variables), 128, 128)
            y = torch.randn(self.forecast_steps, 128, 128)
            return x, y
        
        elif sample['type'] == 'npy':
            # 加载 numpy 数据
            data = np.load(sample['path'])
            return self._process_numpy(data)
        
        elif sample['type'] == 'nc':
            # 加载 NetCDF 数据
            return self._process_netcdf(sample['path'])
        
        else:
            raise ValueError(f"未知数据类型: {sample['type']}")
    
    def _process_numpy(self, data: np.ndarray) -> Tuple[torch.Tensor, torch.Tensor]:
        """处理 numpy 数据"""
        # 假设数据形状为 (T, H, W) 或 (T, C, H, W)
        if data.ndim == 3:
            data = data[:, np.newaxis, :, :]  # 添加通道维度
        
        T = data.shape[0]
        
        # 划分输入和目标
        if T >= self.time_steps + self.forecast_steps:
            x = data[:self.time_steps]
            y = data[self.time_steps:self.time_steps + self.forecast_steps, 0]  # 只取降水
        else:
            # 数据不足，填充
            x = np.zeros((self.time_steps, data.shape[1], data.shape[2], data.shape[3]))
            y = np.zeros((self.forecast_steps, data.shape[2], data.shape[3]))
            x[:min(T, self.time_steps)] = data[:min(T, self.time_steps)]
        
        # 数据增强
        if self.transform and self.mode == 'train':
            x, y = self.transform(x, y)
        
        return torch.from_numpy(x).float(), torch.from_numpy(y).float()
    
    def _process_netcdf(self, path: str) -> Tuple[torch.Tensor, torch.Tensor]:
        """处理 NetCDF 数据"""
        try:
            import xarray as xr
            ds = xr.open_dataset(path)
            
            # 提取降水变量
            if 'tp' in ds:
                precip = ds['tp'].values  # (T, H, W)
            elif 'precipitation' in ds:
                precip = ds['precipitation'].values
            else:
                # 使用第一个变量
                var_name = list(ds.data_vars)[0]
                precip = ds[var_name].values
            
            ds.close()
            
            return self._process_numpy(precip)
            
        except Exception as e:
            print(f"加载 NetCDF 失败: {e}")
            # 返回虚拟数据
            return torch.randn(self.time_steps, len(self.variables), 128, 128), \
                   torch.randn(self.forecast_steps, 128, 128)


class DataAugmentation:
    """数据增强"""
    
    def __init__(self, 
                 flip_prob: float = 0.5,
                 rotate_prob: float = 0.5,
                 noise_prob: float = 0.3,
                 noise_std: float = 0.01):
        self.flip_prob = flip_prob
        self.rotate_prob = rotate_prob
        self.noise_prob = noise_prob
        self.noise_std = noise_std
    
    def __call__(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """应用数据增强"""
        # 水平翻转
        if np.random.random() < self.flip_prob:
            x = np.flip(x, axis=-1)
            y = np.flip(y, axis=-1)
        
        # 垂直翻转
        if np.random.random() < self.flip_prob:
            x = np.flip(x, axis=-2)
            y = np.flip(y, axis=-2)
        
        # 旋转90度
        if np.random.random() < self.rotate_prob:
            k = np.random.randint(1, 4)
            x = np.rot90(x, k, axes=(-2, -1))
            y = np.rot90(y, k, axes=(-2, -1))
        
        # 添加噪声
        if np.random.random() < self.noise_prob:
            x = x + np.random.randn(*x.shape) * self.noise_std
        
        return x.copy(), y.copy()


class PrecipitationLightningModule(pl.LightningModule):
    """降水预报 Lightning 模块"""
    
    def __init__(self, model: nn.Module, config: DictConfig):
        super().__init__()
        self.model = model
        self.config = config
        self.save_hyperparameters(config)
        
        # 损失函数
        self._setup_losses()
        
        # 用于累积指标
        self.val_preds = []
        self.val_targets = []
    
    def _setup_losses(self):
        """设置损失函数"""
        # 主损失: 加权MSE
        self.mse_loss = nn.MSELoss()
        
        # 辅助损失
        self.l1_loss = nn.L1Loss()
        
        # 平衡权重 (降水越大，权重越高)
        self.register_buffer('threshold_weights', torch.tensor([1.0, 2.0, 5.0, 10.0]))
    
    def forward(self, x):
        return self.model(x)
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        prediction = self(x)
        
        # 主损失
        mse = self.mse_loss(prediction, y)
        
        # L1损失
        l1 = self.l1_loss(prediction, y)
        
        # 平衡损失 (对高降水区域加权)
        weights = torch.ones_like(y)
        for i, thresh in enumerate([0.1, 1.0, 5.0, 10.0]):
            weights = torch.where(y > thresh, self.threshold_weights[i], weights)
        weighted_mse = ((prediction - y) ** 2 * weights).mean()
        
        # 总损失
        loss = mse + 0.1 * l1 + 0.5 * weighted_mse
        
        # 计算指标
        ts_score = self._compute_ts_score(prediction, y)
        pod = self._compute_pod(prediction, y)
        
        # 日志
        self.log('train_loss', loss, prog_bar=True, on_step=True, on_epoch=True)
        self.log('train_mse', mse, prog_bar=False)
        self.log('train_ts', ts_score, prog_bar=True)
        self.log('train_pod', pod, prog_bar=False)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        prediction = self(x)
        
        # 损失
        mse = self.mse_loss(prediction, y)
        l1 = self.l1_loss(prediction, y)
        
        # 指标
        ts_score = self._compute_ts_score(prediction, y)
        pod = self._compute_pod(prediction, y)
        far = self._compute_far(prediction, y)
        csi = self._compute_csi(prediction, y)
        
        # 日志
        self.log('val_loss', mse, prog_bar=True)
        self.log('val_mse', mse, prog_bar=False)
        self.log('val_l1', l1, prog_bar=False)
        self.log('val_ts', ts_score, prog_bar=True)
        self.log('val_pod', pod, prog_bar=False)
        self.log('val_far', far, prog_bar=False)
        self.log('val_csi', csi, prog_bar=False)
        
        # 累积预测和目标 (用于epoch结束时计算多阈值指标)
        self.val_preds.append(prediction.detach())
        self.val_targets.append(y.detach())
        
        return mse
    
    def on_validation_epoch_end(self):
        """验证epoch结束时计算多阈值指标"""
        if not self.val_preds:
            return
        
        # 合并所有batch
        preds = torch.cat(self.val_preds, dim=0)
        targets = torch.cat(self.val_targets, dim=0)
        
        # 计算不同阈值下的指标
        thresholds = [0.1, 1.0, 5.0, 10.0]
        for thresh in thresholds:
            ts = self._compute_ts_score(preds, targets, threshold=thresh)
            pod = self._compute_pod(preds, targets, threshold=thresh)
            far = self._compute_far(preds, targets, threshold=thresh)
            
            self.log(f'val_ts_{thresh}mm', ts, prog_bar=False)
            self.log(f'val_pod_{thresh}mm', pod, prog_bar=False)
            self.log(f'val_far_{thresh}mm', far, prog_bar=False)
        
        # 清空缓存
        self.val_preds.clear()
        self.val_targets.clear()
    
    def test_step(self, batch, batch_idx):
        x, y = batch
        prediction = self(x)
        
        # 损失
        mse = self.mse_loss(prediction, y)
        
        # 多阈值指标
        results = {'mse': mse}
        
        thresholds = [0.1, 1.0, 5.0, 10.0]
        for thresh in thresholds:
            results[f'ts_{thresh}mm'] = self._compute_ts_score(prediction, y, threshold=thresh)
            results[f'pod_{thresh}mm'] = self._compute_pod(prediction, y, threshold=thresh)
            results[f'far_{thresh}mm'] = self._compute_far(prediction, y, threshold=thresh)
            results[f'csi_{thresh}mm'] = self._compute_csi(prediction, y, threshold=thresh)
        
        # 日志
        for key, value in results.items():
            self.log(f'test_{key}', value, prog_bar=True)
        
        return results
    
    def configure_optimizers(self):
        # 优化器
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.config.training.lr,
            weight_decay=self.config.training.weight_decay,
            betas=(0.9, 0.999)
        )
        
        # 学习率调度器
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer,
            max_lr=self.config.training.lr,
            total_steps=self.trainer.estimated_stepping_batches,
            pct_start=0.1,
            anneal_strategy='cos',
            final_div_factor=100
        )
        
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'interval': 'step'
            }
        }
    
    def _compute_ts_score(self, prediction: torch.Tensor, 
                          target: torch.Tensor, 
                          threshold: float = 0.1) -> torch.Tensor:
        """计算 TS (Threat Score)"""
        pred_binary = (prediction > threshold).float()
        target_binary = (target > threshold).float()
        
        hits = (pred_binary * target_binary).sum()
        false_alarms = (pred_binary * (1 - target_binary)).sum()
        misses = ((1 - pred_binary) * target_binary).sum()
        
        ts = hits / (hits + false_alarms + misses + 1e-8)
        return ts
    
    def _compute_pod(self, prediction: torch.Tensor, 
                     target: torch.Tensor,
                     threshold: float = 0.1) -> torch.Tensor:
        """计算 POD (Probability of Detection)"""
        pred_binary = (prediction > threshold).float()
        target_binary = (target > threshold).float()
        
        hits = (pred_binary * target_binary).sum()
        misses = ((1 - pred_binary) * target_binary).sum()
        
        pod = hits / (hits + misses + 1e-8)
        return pod
    
    def _compute_far(self, prediction: torch.Tensor,
                     target: torch.Tensor,
                     threshold: float = 0.1) -> torch.Tensor:
        """计算 FAR (False Alarm Rate)"""
        pred_binary = (prediction > threshold).float()
        target_binary = (target > threshold).float()
        
        false_alarms = (pred_binary * (1 - target_binary)).sum()
        hits = (pred_binary * target_binary).sum()
        
        far = false_alarms / (hits + false_alarms + 1e-8)
        return far
    
    def _compute_csi(self, prediction: torch.Tensor,
                     target: torch.Tensor,
                     threshold: float = 0.1) -> torch.Tensor:
        """计算 CSI (Critical Success Index)"""
        return self._compute_ts_score(prediction, target, threshold)


def create_datasets(config: DictConfig) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """创建数据集和数据加载器"""
    
    # 数据增强
    train_transform = DataAugmentation(
        flip_prob=0.5,
        rotate_prob=0.5,
        noise_prob=0.3
    ) if config.training.get('augmentation', True) else None
    
    # 创建数据集
    train_dataset = PrecipitationDataset(
        data_path=config.data.train_path,
        time_steps=config.model.time_steps,
        forecast_steps=config.model.forecast_steps,
        transform=train_transform,
        mode='train'
    )
    
    val_dataset = PrecipitationDataset(
        data_path=config.data.val_path,
        time_steps=config.model.time_steps,
        forecast_steps=config.model.forecast_steps,
        transform=None,
        mode='val'
    )
    
    test_dataset = PrecipitationDataset(
        data_path=config.data.test_path,
        time_steps=config.model.time_steps,
        forecast_steps=config.model.forecast_steps,
        transform=None,
        mode='test'
    )
    
    # 数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.training.batch_size,
        shuffle=True,
        num_workers=config.training.num_workers,
        pin_memory=True,
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.training.batch_size,
        num_workers=config.training.num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.training.batch_size,
        num_workers=config.training.num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader


def create_model(config: DictConfig) -> nn.Module:
    """创建模型"""
    from src.models.mamba_swin_unet import MambaSwinUNetSTA
    from src.models.router import LoongClawFramework
    
    # 基础模型
    base_model = MambaSwinUNetSTA(
        in_channels=config.model.in_channels,
        out_channels=config.model.forecast_steps,
        base_channels=config.model.base_channels,
        time_steps=config.model.time_steps
    )
    
    # 是否使用 LoongClaw 动态路由
    if config.model.get('use_loongclaw', False):
        model = LoongClawFramework(base_model, config)
        print(f"   使用 LoongClaw 动态路由框架")
    else:
        model = base_model
    
    # 打印模型信息
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"   总参数量: {total_params:,}")
    print(f"   可训练参数: {trainable_params:,}")
    
    return model


def train(config: DictConfig):
    """训练函数"""
    
    print("\n" + "="*60)
    print("  LoongClaw-Railway-Forecast 训练")
    print("="*60)
    
    # 设置随机种子
    pl.seed_everything(config.seed)
    
    # 创建数据集
    print("\n📁 加载数据集...")
    train_loader, val_loader, test_loader = create_datasets(config)
    print(f"   训练集: {len(train_loader.dataset)} 样本")
    print(f"   验证集: {len(val_loader.dataset)} 样本")
    print(f"   测试集: {len(test_loader.dataset)} 样本")
    
    # 创建模型
    print("\n🔧 创建模型...")
    model = create_model(config)
    
    # 创建 Lightning 模块
    lightning_module = PrecipitationLightningModule(model, config)
    
    # 回调函数
    callbacks = [
        ModelCheckpoint(
            dirpath=config.training.checkpoint_dir,
            filename='epoch{epoch:03d}-ts{val_ts:.4f}',
            monitor='val_ts',
            mode='max',
            save_top_k=5,
            save_last=True,
            auto_insert_metric_name=False
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=config.training.early_stopping_patience,
            mode='min',
            verbose=True
        ),
        LearningRateMonitor(logging_interval='step')
    ]
    
    # 日志记录器
    loggers = [
        TensorBoardLogger(
            save_dir=config.logging.log_dir,
            name=config.project_name,
            version=None
        )
    ]
    
    if config.logging.get('use_wandb', False):
        try:
            loggers.append(WandbLogger(
                project=config.logging.get('wandb_project', 'loongclaw-forecast'),
                name=config.project_name,
                config=OmegaConf.to_container(config)
            ))
        except Exception as e:
            print(f"   警告: 无法初始化 WandB: {e}")
    
    # 创建训练器
    trainer = pl.Trainer(
        max_epochs=config.training.epochs,
        accelerator=config.training.accelerator,
        devices=config.training.devices,
        callbacks=callbacks,
        logger=loggers,
        gradient_clip_val=config.training.gradient_clip_val,
        accumulate_grad_batches=config.training.get('accumulate_grad_batches', 1),
        precision=config.training.get('precision', '32'),
        deterministic=False,
        benchmark=True,
        log_every_n_steps=10
    )
    
    # 开始训练
    print("\n🚀 开始训练...")
    trainer.fit(lightning_module, train_loader, val_loader)
    
    # 测试
    print("\n📊 测试模型...")
    trainer.test(lightning_module, test_loader)
    
    print("\n✅ 训练完成!")
    print(f"   最佳模型: {callbacks[0].best_model_path}")
    
    return trainer


def resume_training(config: DictConfig, checkpoint_path: str):
    """从检查点恢复训练"""
    print(f"\n📂 从检查点恢复: {checkpoint_path}")
    
    # 创建模型
    model = create_model(config)
    lightning_module = PrecipitationLightningModule.load_from_checkpoint(
        checkpoint_path, model=model, config=config
    )
    
    # 创建数据集
    train_loader, val_loader, test_loader = create_datasets(config)
    
    # 创建训练器
    trainer = pl.Trainer(
        max_epochs=config.training.epochs,
        accelerator=config.training.accelerator,
        devices=config.training.devices
    )
    
    # 继续训练
    trainer.fit(lightning_module, train_loader, val_loader)
    
    return trainer


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='LoongClaw 降水预报模型训练')
    parser.add_argument('--config', type=str, default='configs/model.yaml',
                        help='配置文件路径')
    parser.add_argument('--resume', type=str, default=None,
                        help='从检查点恢复训练')
    args = parser.parse_args()
    
    # 加载配置
    config = OmegaConf.load(args.config)
    
    # 更新项目名称
    config.project_name = "LoongClaw-Railway-Forecast"
    
    if args.resume:
        resume_training(config, args.resume)
    else:
        train(config)
