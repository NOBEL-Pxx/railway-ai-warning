"""
评估指标模块
包含降水预报专用的评估指标
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ContingencyTable:
    """列联表"""
    hits: float = 0.0          # 命中
    misses: float = 0.0        # 漏报
    false_alarms: float = 0.0  # 空报
    correct_negatives: float = 0.0  # 正确否定
    
    def total(self) -> float:
        return self.hits + self.misses + self.false_alarms + self.correct_negatives


class PrecipitationMetrics:
    """
    降水预报评估指标
    
    包含:
    - TS (Threat Score) / CSI (Critical Success Index)
    - POD (Probability of Detection)
    - FAR (False Alarm Rate)
    - Bias (频率偏差)
    - HSS (Heidke Skill Score)
    - ETS (Equitable Threat Score)
    - MAE, RMSE
    """
    
    def __init__(self, thresholds: List[float] = None):
        """
        Args:
            thresholds: 降水阈值列表 (mm/h)
        """
        self.thresholds = thresholds or [0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 20.0, 50.0]
        
        # 每个阈值的列联表
        self.tables: Dict[float, ContingencyTable] = {
            thresh: ContingencyTable() for thresh in self.thresholds
        }
        
        # 连续指标累积
        self.mae_sum = 0.0
        self.mse_sum = 0.0
        self.count = 0
    
    def update(self, prediction: torch.Tensor, target: torch.Tensor):
        """
        更新指标
        
        Args:
            prediction: 预测值 (任意形状)
            target: 真实值
        """
        # 转换为numpy
        if isinstance(prediction, torch.Tensor):
            prediction = prediction.detach().cpu().numpy()
        if isinstance(target, torch.Tensor):
            target = target.detach().cpu().numpy()
        
        # 展平
        prediction = prediction.flatten()
        target = target.flatten()
        
        # 更新连续指标
        self.mae_sum += np.abs(prediction - target).sum()
        self.mse_sum += ((prediction - target) ** 2).sum()
        self.count += len(target)
        
        # 更新列联表
        for thresh in self.thresholds:
            pred_binary = prediction > thresh
            target_binary = target > thresh
            
            table = self.tables[thresh]
            table.hits += np.sum(pred_binary & target_binary)
            table.misses += np.sum(~pred_binary & target_binary)
            table.false_alarms += np.sum(pred_binary & ~target_binary)
            table.correct_negatives += np.sum(~pred_binary & ~target_binary)
    
    def compute(self) -> Dict[str, Dict[str, float]]:
        """
        计算所有指标
        
        Returns:
            指标字典 {threshold: {metric: value}}
        """
        results = {}
        
        for thresh, table in self.tables.items():
            metrics = self._compute_categorical_metrics(table)
            results[f'{thresh}mm'] = metrics
        
        # 添加连续指标
        results['continuous'] = {
            'mae': self.mae_sum / (self.count + 1e-8),
            'rmse': np.sqrt(self.mse_sum / (self.count + 1e-8)),
            'mse': self.mse_sum / (self.count + 1e-8)
        }
        
        return results
    
    def _compute_categorical_metrics(self, table: ContingencyTable) -> Dict[str, float]:
        """计算分类指标"""
        h = table.hits
        m = table.misses
        f = table.false_alarms
        c = table.correct_negatives
        total = table.total()
        
        # TS / CSI
        ts = h / (h + m + f + 1e-8)
        
        # POD (命中率)
        pod = h / (h + m + 1e-8)
        
        # FAR (空报率)
        far = f / (h + f + 1e-8)
        
        # Bias (频率偏差)
        bias = (h + f) / (h + m + 1e-8)
        
        # HSS (Heidke Skill Score)
        expected = ((h + f) * (h + m) + (c + m) * (c + f)) / (total + 1e-8)
        hss = (h + c - expected) / (total - expected + 1e-8)
        
        # ETS (Equitable Threat Score)
        hits_random = (h + m) * (h + f) / (total + 1e-8)
        ets = (h - hits_random) / (h + m + f - hits_random + 1e-8)
        
        # Accuracy
        accuracy = (h + c) / (total + 1e-8)
        
        # F1 Score
        precision = h / (h + f + 1e-8)
        recall = pod
        f1 = 2 * precision * recall / (precision + recall + 1e-8)
        
        return {
            'ts': ts,
            'csi': ts,
            'pod': pod,
            'far': far,
            'bias': bias,
            'hss': hss,
            'ets': ets,
            'accuracy': accuracy,
            'f1': f1,
            'hits': h,
            'misses': m,
            'false_alarms': f,
            'correct_negatives': c
        }
    
    def reset(self):
        """重置所有指标"""
        for thresh in self.thresholds:
            self.tables[thresh] = ContingencyTable()
        self.mae_sum = 0.0
        self.mse_sum = 0.0
        self.count = 0
    
    def summary(self) -> str:
        """生成摘要字符串"""
        results = self.compute()
        
        lines = ["=" * 70]
        lines.append("降水预报评估指标")
        lines.append("=" * 70)
        
        # 分类指标
        lines.append("\n分类指标 (按阈值):")
        lines.append("-" * 70)
        header = f"{'阈值':>8} {'TS':>8} {'POD':>8} {'FAR':>8} {'Bias':>8} {'ETS':>8}"
        lines.append(header)
        lines.append("-" * 70)
        
        for thresh_str, metrics in results.items():
            if thresh_str == 'continuous':
                continue
            thresh = thresh_str.replace('mm', '')
            line = f"{thresh:>8} {metrics['ts']:>8.4f} {metrics['pod']:>8.4f} " \
                   f"{metrics['far']:>8.4f} {metrics['bias']:>8.4f} {metrics['ets']:>8.4f}"
            lines.append(line)
        
        # 连续指标
        lines.append("\n连续指标:")
        lines.append("-" * 70)
        cont = results.get('continuous', {})
        lines.append(f"  MAE:  {cont.get('mae', 0):.4f}")
        lines.append(f"  RMSE: {cont.get('rmse', 0):.4f}")
        
        return "\n".join(lines)


class SpatialMetrics:
    """
    空间评估指标
    
    包含:
    - 空间相关系数
    - 结构相似性
    - 尺度分离指标
    """
    
    def __init__(self):
        self.correlations = []
        self.ssim_values = []
    
    def update(self, prediction: torch.Tensor, target: torch.Tensor):
        """更新空间指标"""
        if isinstance(prediction, torch.Tensor):
            prediction = prediction.detach().cpu().numpy()
        if isinstance(target, torch.Tensor):
            target = target.detach().cpu().numpy()
        
        # 对每个样本计算
        if prediction.ndim >= 3:
            for i in range(prediction.shape[0]):
                self._update_single(prediction[i], target[i])
        else:
            self._update_single(prediction, target)
    
    def _update_single(self, pred: np.ndarray, target: np.ndarray):
        """更新单个样本"""
        # 展平
        pred_flat = pred.flatten()
        target_flat = target.flatten()
        
        # 相关系数
        if np.std(pred_flat) > 1e-8 and np.std(target_flat) > 1e-8:
            corr = np.corrcoef(pred_flat, target_flat)[0, 1]
            self.correlations.append(corr)
        
        # SSIM (简化版)
        ssim = self._compute_ssim(pred, target)
        self.ssim_values.append(ssim)
    
    def _compute_ssim(self, pred: np.ndarray, target: np.ndarray, 
                      window_size: int = 11) -> float:
        """计算SSIM"""
        from scipy.ndimage import uniform_filter
        
        # 确保是2D
        while pred.ndim > 2:
            pred = pred[0]
        while target.ndim > 2:
            target = target[0]
        
        C1 = 0.01 ** 2
        C2 = 0.03 ** 2
        
        mu1 = uniform_filter(pred, size=window_size)
        mu2 = uniform_filter(target, size=window_size)
        
        sigma1_sq = uniform_filter(pred ** 2, size=window_size) - mu1 ** 2
        sigma2_sq = uniform_filter(target ** 2, size=window_size) - mu2 ** 2
        sigma12 = uniform_filter(pred * target, size=window_size) - mu1 * mu2
        
        ssim = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / \
               ((mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2))
        
        return ssim.mean()
    
    def compute(self) -> Dict[str, float]:
        """计算空间指标"""
        return {
            'spatial_correlation': np.mean(self.correlations) if self.correlations else 0.0,
            'ssim': np.mean(self.ssim_values) if self.ssim_values else 0.0
        }
    
    def reset(self):
        """重置"""
        self.correlations = []
        self.ssim_values = []


class TemporalMetrics:
    """
    时间评估指标
    
    包含:
    - 时间相关系数
    - 预报时效评分
    - 时间一致性
    """
    
    def __init__(self, forecast_steps: int = 6):
        """
        Args:
            forecast_steps: 预报步数
        """
        self.forecast_steps = forecast_steps
        self.step_metrics = [PrecipitationMetrics() for _ in range(forecast_steps)]
    
    def update(self, prediction: torch.Tensor, target: torch.Tensor):
        """
        更新时间指标
        
        Args:
            prediction: (B, T, H, W) 或 (B, T, C, H, W)
            target: (B, T, H, W)
        """
        if isinstance(prediction, torch.Tensor):
            prediction = prediction.detach().cpu().numpy()
        if isinstance(target, torch.Tensor):
            target = target.detach().cpu().numpy()
        
        # 确保维度正确
        if prediction.ndim == 4:
            # (B, T, H, W)
            pass
        elif prediction.ndim == 5:
            # (B, T, C, H, W) -> (B, T, H, W)
            prediction = prediction[:, :, 0]
        
        # 对每个时间步更新
        for t in range(min(prediction.shape[1], self.forecast_steps)):
            self.step_metrics[t].update(prediction[:, t], target[:, t])
    
    def compute(self) -> Dict[str, Dict[str, float]]:
        """计算时间指标"""
        results = {}
        
        for t, metrics in enumerate(self.step_metrics):
            step_results = metrics.compute()
            results[f'step_{t+1}'] = step_results
        
        # 计算平均
        avg_ts = np.mean([r['0.1mm']['ts'] for r in results.values()])
        avg_pod = np.mean([r['0.1mm']['pod'] for r in results.values()])
        
        results['average'] = {
            'ts': avg_ts,
            'pod': avg_pod
        }
        
        return results
    
    def reset(self):
        """重置"""
        for metrics in self.step_metrics:
            metrics.reset()
    
    def summary(self) -> str:
        """生成摘要"""
        results = self.compute()
        
        lines = ["=" * 50]
        lines.append("时间维评估指标")
        lines.append("=" * 50)
        
        header = f"{'步数':>6} {'TS':>8} {'POD':>8} {'FAR':>8}"
        lines.append(header)
        lines.append("-" * 50)
        
        for t in range(self.forecast_steps):
            key = f'step_{t+1}'
            if key in results:
                m = results[key]['0.1mm']
                line = f"{t+1:>6} {m['ts']:>8.4f} {m['pod']:>8.4f} {m['far']:>8.4f}"
                lines.append(line)
        
        return "\n".join(lines)


class ComprehensiveEvaluator:
    """
    综合评估器
    整合所有评估指标
    """
    
    def __init__(self, 
                 thresholds: List[float] = None,
                 forecast_steps: int = 6):
        """
        Args:
            thresholds: 降水阈值
            forecast_steps: 预报步数
        """
        self.precip_metrics = PrecipitationMetrics(thresholds)
        self.spatial_metrics = SpatialMetrics()
        self.temporal_metrics = TemporalMetrics(forecast_steps)
        
        self.thresholds = thresholds or [0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 20.0]
        self.forecast_steps = forecast_steps
    
    def update(self, prediction: torch.Tensor, target: torch.Tensor):
        """更新所有指标"""
        self.precip_metrics.update(prediction, target)
        self.spatial_metrics.update(prediction, target)
        
        if prediction.dim() >= 3 and prediction.shape[1] > 1:
            self.temporal_metrics.update(prediction, target)
    
    def compute(self) -> Dict[str, any]:
        """计算所有指标"""
        return {
            'precipitation': self.precip_metrics.compute(),
            'spatial': self.spatial_metrics.compute(),
            'temporal': self.temporal_metrics.compute() if self.forecast_steps > 1 else None
        }
    
    def reset(self):
        """重置所有指标"""
        self.precip_metrics.reset()
        self.spatial_metrics.reset()
        self.temporal_metrics.reset()
    
    def summary(self) -> str:
        """生成完整摘要"""
        lines = [self.precip_metrics.summary()]
        
        spatial = self.spatial_metrics.compute()
        lines.append("\n空间指标:")
        lines.append(f"  空间相关系数: {spatial['spatial_correlation']:.4f}")
        lines.append(f"  SSIM: {spatial['ssim']:.4f}")
        
        if self.forecast_steps > 1:
            lines.append("\n" + self.temporal_metrics.summary())
        
        return "\n".join(lines)


def compute_skill_score(prediction: np.ndarray, 
                        target: np.ndarray,
                        climatology: np.ndarray = None,
                        reference: np.ndarray = None) -> Dict[str, float]:
    """
    计算技巧评分
    
    Args:
        prediction: 预测值
        target: 真实值
        climatology: 气候态 (可选)
        reference: 参考预报 (可选)
        
    Returns:
        技巧评分字典
    """
    # 基础误差
    mse = np.mean((prediction - target) ** 2)
    mae = np.mean(np.abs(prediction - target))
    
    results = {
        'mse': mse,
        'mae': mae,
        'rmse': np.sqrt(mse)
    }
    
    # 相对于气候态的技巧
    if climatology is not None:
        mse_clim = np.mean((climatology - target) ** 2)
        results['skill_vs_climatology'] = 1 - mse / (mse_clim + 1e-8)
    
    # 相对于参考预报的技巧
    if reference is not None:
        mse_ref = np.mean((reference - target) ** 2)
        results['skill_vs_reference'] = 1 - mse / (mse_ref + 1e-8)
    
    return results


if __name__ == "__main__":
    print("测试评估指标模块")
    
    # 创建测试数据
    batch_size = 4
    time_steps = 6
    height, width = 64, 64
    
    # 模拟降水数据 (非负，有偏分布)
    target = np.random.exponential(1.0, (batch_size, time_steps, height, width))
    prediction = target + np.random.randn(batch_size, time_steps, height, width) * 0.5
    prediction = np.maximum(prediction, 0)  # 确保非负
    
    prediction = torch.from_numpy(prediction).float()
    target = torch.from_numpy(target).float()
    
    # 测试降水指标
    print("\n1. 降水指标:")
    precip_metrics = PrecipitationMetrics()
    precip_metrics.update(prediction, target)
    print(precip_metrics.summary())
    
    # 测试空间指标
    print("\n2. 空间指标:")
    spatial_metrics = SpatialMetrics()
    spatial_metrics.update(prediction, target)
    print(spatial_metrics.compute())
    
    # 测试时间指标
    print("\n3. 时间指标:")
    temporal_metrics = TemporalMetrics(forecast_steps=6)
    temporal_metrics.update(prediction, target)
    print(temporal_metrics.summary())
    
    # 测试综合评估器
    print("\n4. 综合评估:")
    evaluator = ComprehensiveEvaluator(forecast_steps=6)
    evaluator.update(prediction, target)
    print(evaluator.summary())
