"""
单元测试
"""

import pytest
import torch
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.mamba_swin_unet import MambaSwinUNetSTA, MambaBlock, SwinTransformerBlock
from src.models.router import DynamicRouter, WeatherContext
from src.utils.common import compute_metrics, normalize_data, denormalize_data


class TestMambaBlock:
    """测试Mamba模块"""
    
    def test_forward(self):
        model = MambaBlock(d_model=64)
        x = torch.randn(2, 100, 64)
        out = model(x)
        assert out.shape == x.shape


class TestSwinTransformerBlock:
    """测试Swin Transformer模块"""
    
    def test_forward(self):
        model = SwinTransformerBlock(dim=64, window_size=7)
        x = torch.randn(2, 14, 14, 64)
        out = model(x)
        assert out.shape == x.shape


class TestMambaSwinUNetSTA:
    """测试完整模型"""
    
    def test_forward(self):
        model = MambaSwinUNetSTA(in_channels=1, out_channels=1, time_steps=6)
        x = torch.randn(2, 6, 1, 64, 64)
        out = model(x)
        assert out.shape == (2, 1, 64, 64)
    
    def test_parameters_count(self):
        model = MambaSwinUNetSTA(base_channels=32)
        num_params = sum(p.numel() for p in model.parameters())
        assert num_params > 0


class TestDynamicRouter:
    """测试动态路由"""
    
    def test_weight_prediction(self):
        router = DynamicRouter()
        context = WeatherContext(
            convection_intensity=0.8,
            stability_index=0.3,
            system_speed=30.0,
            precipitation_intensity=50.0,
            terrain_complexity=0.7
        )
        weights = router(context)
        assert weights.shape == (4,)
        assert torch.allclose(weights.sum(), torch.tensor(1.0), atol=1e-5)


class TestMetrics:
    """测试评估指标"""
    
    def test_compute_metrics(self):
        prediction = np.array([[1, 2], [3, 4]])
        target = np.array([[1, 2], [3, 4]])
        metrics = compute_metrics(prediction, target, threshold=0.5)
        
        assert 'ts' in metrics
        assert 'pod' in metrics
        assert 'far' in metrics
        assert 0 <= metrics['ts'] <= 1
    
    def test_perfect_prediction(self):
        prediction = np.ones((10, 10))
        target = np.ones((10, 10))
        metrics = compute_metrics(prediction, target, threshold=0.5)
        
        assert metrics['ts'] == 1.0
        assert metrics['pod'] == 1.0
        assert metrics['far'] == 0.0


class TestNormalization:
    """测试数据标准化"""
    
    def test_minmax_normalization(self):
        data = np.array([0, 1, 2, 3, 4, 5])
        normalized, params = normalize_data(data, method='minmax')
        
        assert params['min'] == 0
        assert params['max'] == 5
        assert np.allclose(normalized.min(), 0)
        assert np.allclose(normalized.max(), 1)
    
    def test_denormalization(self):
        data = np.array([0, 1, 2, 3, 4, 5], dtype=float)
        normalized, params = normalize_data(data, method='minmax')
        recovered = denormalize_data(normalized, params, method='minmax')
        
        assert np.allclose(data, recovered)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
