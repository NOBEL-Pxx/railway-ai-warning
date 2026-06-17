"""
工具函数模块
"""

import os
import yaml
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_path, 'r') as f:
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            return yaml.safe_load(f)
        elif config_path.endswith('.json'):
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_path}")


def save_config(config: Dict[str, Any], save_path: str):
    """保存配置文件"""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, 'w') as f:
        if save_path.endswith('.yaml') or save_path.endswith('.yml'):
            yaml.dump(config, f, default_flow_style=False)
        elif save_path.endswith('.json'):
            json.dump(config, f, indent=2)
        else:
            raise ValueError(f"Unsupported config format: {save_path}")


def ensure_dir(path: str):
    """确保目录存在"""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_timestamp() -> str:
    """获取时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def compute_metrics(prediction: np.ndarray, 
                    target: np.ndarray,
                    threshold: float = 0.1) -> Dict[str, float]:
    """
    计算评估指标
    
    Args:
        prediction: 预测值
        target: 真实值
        threshold: 阈值
        
    Returns:
        指标字典
    """
    pred_binary = (prediction > threshold).astype(float)
    target_binary = (target > threshold).astype(float)
    
    hits = (pred_binary * target_binary).sum()
    false_alarms = (pred_binary * (1 - target_binary)).sum()
    misses = ((1 - pred_binary) * target_binary).sum()
    correct_negatives = ((1 - pred_binary) * (1 - target_binary)).sum()
    
    # TS (Threat Score)
    ts = hits / (hits + false_alarms + misses + 1e-8)
    
    # POD (Probability of Detection)
    pod = hits / (hits + misses + 1e-8)
    
    # FAR (False Alarm Rate)
    far = false_alarms / (hits + false_alarms + 1e-8)
    
    # CSI (Critical Success Index)
    csi = hits / (hits + false_alarms + misses + 1e-8)
    
    # Bias
    bias = (hits + false_alarms) / (hits + misses + 1e-8)
    
    # Accuracy
    accuracy = (hits + correct_negatives) / (hits + false_alarms + misses + correct_negatives + 1e-8)
    
    return {
        'ts': ts,
        'pod': pod,
        'far': far,
        'csi': csi,
        'bias': bias,
        'accuracy': accuracy
    }


def compute_spatial_correlation(prediction: np.ndarray, 
                                target: np.ndarray) -> float:
    """计算空间相关系数"""
    pred_flat = prediction.flatten()
    target_flat = target.flatten()
    
    correlation = np.corrcoef(pred_flat, target_flat)[0, 1]
    return correlation


def normalize_data(data: np.ndarray, 
                   method: str = 'minmax',
                   params: Dict[str, float] = None) -> Tuple[np.ndarray, Dict]:
    """
    数据标准化
    
    Args:
        data: 输入数据
        method: 标准化方法
        params: 标准化参数（如果提供则使用，否则计算）
        
    Returns:
        (标准化后的数据, 参数字典)
    """
    if params is None:
        if method == 'minmax':
            data_min = np.nanmin(data)
            data_max = np.nanmax(data)
            params = {'min': data_min, 'max': data_max}
        elif method == 'zscore':
            data_mean = np.nanmean(data)
            data_std = np.nanstd(data)
            params = {'mean': data_mean, 'std': data_std}
        else:
            raise ValueError(f"Unknown normalization method: {method}")
    
    if method == 'minmax':
        normalized = (data - params['min']) / (params['max'] - params['min'] + 1e-8)
    elif method == 'zscore':
        normalized = (data - params['mean']) / (params['std'] + 1e-8)
    
    return normalized, params


def denormalize_data(data: np.ndarray, 
                     params: Dict[str, float],
                     method: str = 'minmax') -> np.ndarray:
    """数据反标准化"""
    if method == 'minmax':
        return data * (params['max'] - params['min']) + params['min']
    elif method == 'zscore':
        return data * params['std'] + params['mean']


def split_data(data: np.ndarray, 
               train_ratio: float = 0.7,
               val_ratio: float = 0.15,
               test_ratio: float = 0.15,
               shuffle: bool = True,
               seed: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    划分数据集
    
    Args:
        data: 输入数据
        train_ratio: 训练集比例
        val_ratio: 验证集比例
        test_ratio: 测试集比例
        shuffle: 是否打乱
        seed: 随机种子
        
    Returns:
        (train_data, val_data, test_data)
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6
    
    n_samples = len(data)
    indices = np.arange(n_samples)
    
    if shuffle:
        np.random.seed(seed)
        np.random.shuffle(indices)
    
    train_end = int(n_samples * train_ratio)
    val_end = train_end + int(n_samples * val_ratio)
    
    train_indices = indices[:train_end]
    val_indices = indices[train_end:val_end]
    test_indices = indices[val_end:]
    
    return data[train_indices], data[val_indices], data[test_indices]


class EarlyStopping:
    """早停机制"""
    
    def __init__(self, patience: int = 10, min_delta: float = 0.0, mode: str = 'min'):
        """
        Args:
            patience: 容忍轮数
            min_delta: 最小改进
            mode: 'min' 或 'max'
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        
    def __call__(self, score: float) -> bool:
        """
        检查是否应该早停
        
        Args:
            score: 当前分数
            
        Returns:
            是否应该早停
        """
        if self.best_score is None:
            self.best_score = score
            return False
        
        if self.mode == 'min':
            improved = score < self.best_score - self.min_delta
        else:
            improved = score > self.best_score + self.min_delta
        
        if improved:
            self.best_score = score
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        
        return self.early_stop


class AverageMeter:
    """计算并存储平均值"""
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
        
    def update(self, val: float, n: int = 1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
