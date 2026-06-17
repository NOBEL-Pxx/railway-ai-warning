"""
损失函数模块
包含降水预报专用的损失函数
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, List, Tuple
import numpy as np


class WeightedMSELoss(nn.Module):
    """
    加权均方误差损失
    对高降水区域赋予更高权重
    """
    
    def __init__(self, 
                 thresholds: List[float] = None,
                 weights: List[float] = None,
                 reduction: str = 'mean'):
        """
        Args:
            thresholds: 降水阈值列表 (mm/h)
            weights: 对应的权重
            reduction: 'mean', 'sum', 'none'
        """
        super().__init__()
        self.thresholds = thresholds or [0.1, 1.0, 5.0, 10.0, 20.0]
        self.weights = weights or [1.0, 2.0, 4.0, 8.0, 16.0]
        self.reduction = reduction
        
        assert len(self.thresholds) == len(self.weights)
    
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor) -> torch.Tensor:
        """计算加权MSE损失"""
        # 基础MSE
        mse = (prediction - target) ** 2
        
        # 根据目标值分配权重
        weight_map = torch.ones_like(target)
        for thresh, weight in zip(self.thresholds, self.weights):
            weight_map = torch.where(target > thresh, 
                                     torch.tensor(weight, device=target.device), 
                                     weight_map)
        
        # 加权
        weighted_mse = mse * weight_map
        
        if self.reduction == 'mean':
            return weighted_mse.mean()
        elif self.reduction == 'sum':
            return weighted_mse.sum()
        else:
            return weighted_mse


class FocalLoss(nn.Module):
    """
    Focal Loss
    解决降水预报中的类别不平衡问题
    """
    
    def __init__(self, 
                 alpha: float = 0.25,
                 gamma: float = 2.0,
                 threshold: float = 0.1,
                 reduction: str = 'mean'):
        """
        Args:
            alpha: 正样本权重
            gamma: 聚焦参数
            threshold: 降水阈值
            reduction: 归约方式
        """
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.threshold = threshold
        self.reduction = reduction
    
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor) -> torch.Tensor:
        """计算Focal Loss"""
        # 二值化
        pred_binary = (prediction > self.threshold).float()
        target_binary = (target > self.threshold).float()
        
        # BCE
        bce = F.binary_cross_entropy_with_logits(
            prediction, target_binary, reduction='none'
        )
        
        # Focal权重
        pt = torch.exp(-bce)
        focal_weight = (1 - pt) ** self.gamma
        
        # Alpha平衡
        alpha_weight = torch.where(
            target_binary == 1,
            torch.tensor(self.alpha, device=target.device),
            torch.tensor(1 - self.alpha, device=target.device)
        )
        
        loss = alpha_weight * focal_weight * bce
        
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:
            return loss


class BalancedLoss(nn.Module):
    """
    平衡损失函数
    结合MSE和分类损失
    """
    
    def __init__(self, 
                 mse_weight: float = 1.0,
                 focal_weight: float = 0.5,
                 threshold: float = 0.1):
        """
        Args:
            mse_weight: MSE损失权重
            focal_weight: Focal损失权重
            threshold: 降水阈值
        """
        super().__init__()
        self.mse_weight = mse_weight
        self.focal_weight = focal_weight
        self.threshold = threshold
        
        self.mse = nn.MSELoss()
        self.focal = FocalLoss(threshold=threshold)
    
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor) -> Tuple[torch.Tensor, dict]:
        """计算平衡损失"""
        mse_loss = self.mse(prediction, target)
        focal_loss = self.focal(prediction, target)
        
        total_loss = self.mse_weight * mse_loss + self.focal_weight * focal_loss
        
        return total_loss, {
            'mse': mse_loss.item(),
            'focal': focal_loss.item()
        }


class SSIMLoss(nn.Module):
    """
    SSIM损失
    保持降水场的空间结构
    """
    
    def __init__(self, window_size: int = 11, channel: int = 1):
        """
        Args:
            window_size: 窗口大小
            channel: 通道数
        """
        super().__init__()
        self.window_size = window_size
        self.channel = channel
        
        # 创建高斯窗口
        self.window = self._create_window(window_size, channel)
    
    def _create_window(self, window_size: int, channel: int) -> torch.Tensor:
        """创建高斯窗口"""
        sigma = 1.5
        gauss = torch.Tensor([
            np.exp(-(x - window_size // 2) ** 2 / float(2 * sigma ** 2))
            for x in range(window_size)
        ])
        gauss = gauss / gauss.sum()
        
        window_1d = gauss.unsqueeze(1)
        window_2d = window_1d.mm(window_1d.t()).float().unsqueeze(0).unsqueeze(0)
        window = window_2d.expand(channel, 1, window_size, window_size).contiguous()
        
        return window
    
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor) -> torch.Tensor:
        """计算SSIM损失"""
        channel = prediction.shape[1] if prediction.dim() == 4 else 1
        
        if prediction.dim() == 3:
            prediction = prediction.unsqueeze(1)
            target = target.unsqueeze(1)
        
        window = self.window.to(prediction.device).type_as(prediction)
        
        if channel != self.channel:
            window = self._create_window(self.window_size, channel).to(prediction.device)
        
        mu1 = F.conv2d(prediction, window, padding=self.window_size // 2, groups=channel)
        mu2 = F.conv2d(target, window, padding=self.window_size // 2, groups=channel)
        
        mu1_sq = mu1.pow(2)
        mu2_sq = mu2.pow(2)
        mu1_mu2 = mu1 * mu2
        
        sigma1_sq = F.conv2d(prediction * prediction, window, padding=self.window_size // 2, groups=channel) - mu1_sq
        sigma2_sq = F.conv2d(target * target, window, padding=self.window_size // 2, groups=channel) - mu2_sq
        sigma12 = F.conv2d(prediction * target, window, padding=self.window_size // 2, groups=channel) - mu1_mu2
        
        C1 = 0.01 ** 2
        C2 = 0.03 ** 2
        
        ssim = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
               ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
        
        return 1 - ssim.mean()


class CombinedLoss(nn.Module):
    """
    组合损失函数
    整合多种损失用于降水预报
    """
    
    def __init__(self, 
                 mse_weight: float = 1.0,
                 weighted_mse_weight: float = 0.5,
                 focal_weight: float = 0.3,
                 ssim_weight: float = 0.2,
                 smoothness_weight: float = 0.1):
        """
        Args:
            mse_weight: MSE权重
            weighted_mse_weight: 加权MSE权重
            focal_weight: Focal损失权重
            ssim_weight: SSIM损失权重
            smoothness_weight: 平滑损失权重
        """
        super().__init__()
        
        self.mse_weight = mse_weight
        self.weighted_mse_weight = weighted_mse_weight
        self.focal_weight = focal_weight
        self.ssim_weight = ssim_weight
        self.smoothness_weight = smoothness_weight
        
        # 损失函数
        self.mse = nn.MSELoss()
        self.weighted_mse = WeightedMSELoss()
        self.focal = FocalLoss()
        self.ssim = SSIMLoss()
    
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor) -> Tuple[torch.Tensor, dict]:
        """计算组合损失"""
        losses = {}
        
        # MSE
        if self.mse_weight > 0:
            losses['mse'] = self.mse(prediction, target)
        
        # 加权MSE
        if self.weighted_mse_weight > 0:
            losses['weighted_mse'] = self.weighted_mse(prediction, target)
        
        # Focal
        if self.focal_weight > 0:
            losses['focal'] = self.focal(prediction, target)
        
        # SSIM
        if self.ssim_weight > 0:
            losses['ssim'] = self.ssim(prediction, target)
        
        # 平滑损失
        if self.smoothness_weight > 0:
            losses['smoothness'] = self._smoothness_loss(prediction)
        
        # 总损失
        total_loss = (
            self.mse_weight * losses.get('mse', 0) +
            self.weighted_mse_weight * losses.get('weighted_mse', 0) +
            self.focal_weight * losses.get('focal', 0) +
            self.ssim_weight * losses.get('ssim', 0) +
            self.smoothness_weight * losses.get('smoothness', 0)
        )
        
        # 转换为标量
        losses = {k: v.item() if isinstance(v, torch.Tensor) else v 
                  for k, v in losses.items()}
        
        return total_loss, losses
    
    def _smoothness_loss(self, x: torch.Tensor) -> torch.Tensor:
        """平滑损失"""
        dx = x[:, :, :, 1:] - x[:, :, :, :-1]
        dy = x[:, :, 1:, :] - x[:, :, :-1, :]
        return (dx ** 2).mean() + (dy ** 2).mean()


class PrecipitationLoss(nn.Module):
    """
    降水预报专用损失函数
    针对短临降水预报特点设计
    """
    
    def __init__(self, 
                 config: dict = None,
                 use_physics: bool = False):
        """
        Args:
            config: 配置字典
            use_physics: 是否使用物理约束
        """
        super().__init__()
        
        config = config or {}
        
        # 基础损失
        self.combined_loss = CombinedLoss(
            mse_weight=config.get('mse_weight', 1.0),
            weighted_mse_weight=config.get('weighted_mse_weight', 0.5),
            focal_weight=config.get('focal_weight', 0.3),
            ssim_weight=config.get('ssim_weight', 0.2),
            smoothness_weight=config.get('smoothness_weight', 0.1)
        )
        
        # 非负约束
        self.non_negative_weight = config.get('non_negative_weight', 0.1)
        
        # 物理约束
        self.use_physics = use_physics
        if use_physics:
            from src.models.physics import PhysicsConstraintLoss
            self.physics_loss = PhysicsConstraintLoss()
    
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor,
                wind_u: torch.Tensor = None,
                wind_v: torch.Tensor = None) -> Tuple[torch.Tensor, dict]:
        """
        计算降水预报损失
        
        Args:
            prediction: 预测降水
            target: 真实降水
            wind_u: u风场 (可选，用于物理约束)
            wind_v: v风场 (可选)
            
        Returns:
            (总损失, 损失分量字典)
        """
        # 组合损失
        total_loss, losses = self.combined_loss(prediction, target)
        
        # 非负约束
        if self.non_negative_weight > 0:
            non_negative = F.relu(-prediction).mean()
            losses['non_negative'] = non_negative.item()
            total_loss = total_loss + self.non_negative_weight * non_negative
        
        # 物理约束
        if self.use_physics and wind_u is not None:
            physics_loss, physics_losses = self.physics_loss(
                prediction, target, wind_u, wind_v
            )
            losses.update({f'physics_{k}': v for k, v in physics_losses.items()})
            total_loss = total_loss + 0.1 * physics_loss
        
        return total_loss, losses


if __name__ == "__main__":
    # 测试损失函数
    print("测试损失函数模块")
    
    batch_size = 4
    time_steps = 6
    height, width = 64, 64
    
    prediction = torch.randn(batch_size, time_steps, height, width) * 10
    target = torch.randn(batch_size, time_steps, height, width) * 10
    target = F.relu(target)  # 确保非负
    
    # 测试各种损失
    print("\n1. 加权MSE:")
    weighted_mse = WeightedMSELoss()
    loss = weighted_mse(prediction, target)
    print(f"   Loss: {loss.item():.4f}")
    
    print("\n2. Focal Loss:")
    focal = FocalLoss()
    loss = focal(prediction, target)
    print(f"   Loss: {loss.item():.4f}")
    
    print("\n3. SSIM Loss:")
    ssim = SSIMLoss()
    loss = ssim(prediction, target)
    print(f"   Loss: {loss.item():.4f}")
    
    print("\n4. 组合损失:")
    combined = CombinedLoss()
    loss, losses = combined(prediction, target)
    print(f"   Total: {loss.item():.4f}")
    for k, v in losses.items():
        print(f"   {k}: {v:.4f}")
    
    print("\n5. 降水专用损失:")
    precip_loss = PrecipitationLoss()
    loss, losses = precip_loss(prediction, target)
    print(f"   Total: {loss.item():.4f}")
    for k, v in losses.items():
        print(f"   {k}: {v:.4f}")
