"""
特征工程模块
地形因子计算、雷达特征提取、时序特征构建
"""

import numpy as np
import pandas as pd
import xarray as xr
from typing import Tuple, Dict, List, Optional, Any
from scipy import ndimage
from scipy.ndimage import sobel, uniform_filter
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TerrainFeatureExtractor:
    """地形特征提取器"""
    
    def __init__(self, dem_data: np.ndarray = None, resolution: float = 30.0):
        """
        Args:
            dem_data: DEM高程数据 (2D array)
            resolution: 空间分辨率 (米)
        """
        self.dem = dem_data
        self.resolution = resolution
        self.features = {}
    
    def load_dem(self, filepath: str) -> np.ndarray:
        """
        加载DEM数据
        
        Args:
            filepath: DEM文件路径 (.tif, .nc)
            
        Returns:
            DEM数组
        """
        logger.info(f"加载DEM数据: {filepath}")
        
        filepath = Path(filepath)
        
        if filepath.suffix in ['.tif', '.tiff']:
            import rasterio
            with rasterio.open(filepath) as src:
                self.dem = src.read(1)
                self.resolution = src.res[0]
        elif filepath.suffix == '.nc':
            ds = xr.open_dataset(filepath)
            var_name = 'elevation' if 'elevation' in ds else 'z'
            self.dem = ds[var_name].values
        else:
            raise ValueError(f"不支持的文件格式: {filepath.suffix}")
        
        logger.info(f"DEM形状: {self.dem.shape}")
        logger.info(f"高程范围: {np.nanmin(self.dem):.1f} - {np.nanmax(self.dem):.1f} m")
        
        return self.dem
    
    def calculate_slope(self) -> np.ndarray:
        """计算坡度 (度)"""
        if self.dem is None:
            raise ValueError("请先加载DEM数据")
        
        dz_dx = sobel(self.dem, axis=1) / (8 * self.resolution)
        dz_dy = sobel(self.dem, axis=0) / (8 * self.resolution)
        
        slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
        slope_deg = np.degrees(slope_rad)
        
        self.features['slope'] = slope_deg
        logger.info(f"坡度范围: {np.nanmin(slope_deg):.2f}° - {np.nanmax(slope_deg):.2f}°")
        
        return slope_deg
    
    def calculate_aspect(self) -> np.ndarray:
        """计算坡向 (度, 0-360)"""
        if self.dem is None:
            raise ValueError("请先加载DEM数据")
        
        dz_dx = sobel(self.dem, axis=1) / (8 * self.resolution)
        dz_dy = sobel(self.dem, axis=0) / (8 * self.resolution)
        
        aspect = np.degrees(np.arctan2(dz_dy, dz_dx))
        aspect = np.where(aspect < 0, 90 - aspect, 360 - aspect + 90)
        aspect = aspect % 360
        
        self.features['aspect'] = aspect
        return aspect
    
    def calculate_flow_accumulation(self) -> np.ndarray:
        """计算汇流累积量 (D8算法)"""
        if self.dem is None:
            raise ValueError("请先加载DEM数据")
        
        rows, cols = self.dem.shape
        flow_acc = np.ones((rows, cols), dtype=np.float32)
        
        di = [0, 1, 1, 1, 0, -1, -1, -1]
        dj = [1, 1, 0, -1, -1, -1, 0, 1]
        
        flow_dir = np.zeros((rows, cols), dtype=np.int8)
        
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if np.isnan(self.dem[i, j]):
                    continue
                
                max_drop = 0
                max_dir = -1
                
                for k in range(8):
                    ni, nj = i + di[k], j + dj[k]
                    if 0 <= ni < rows and 0 <= nj < cols:
                        drop = self.dem[i, j] - self.dem[ni, nj]
                        if drop > max_drop:
                            max_drop = drop
                            max_dir = k
                
                flow_dir[i, j] = max_dir
        
        for _ in range(10):
            new_flow_acc = flow_acc.copy()
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    if flow_dir[i, j] >= 0:
                        ni = i + di[flow_dir[i, j]]
                        nj = j + dj[flow_dir[i, j]]
                        if 0 <= ni < rows and 0 <= nj < cols:
                            new_flow_acc[ni, nj] += flow_acc[i, j]
            flow_acc = new_flow_acc
        
        self.features['flow_accumulation'] = flow_acc
        return flow_acc
    
    def calculate_curvature(self) -> Tuple[np.ndarray, np.ndarray]:
        """计算曲率 (剖面曲率, 平面曲率)"""
        if self.dem is None:
            raise ValueError("请先加载DEM数据")
        
        d2z_dx2 = sobel(sobel(self.dem, axis=1), axis=1) / (64 * self.resolution**2)
        d2z_dy2 = sobel(sobel(self.dem, axis=0), axis=0) / (64 * self.resolution**2)
        d2z_dxdy = sobel(sobel(self.dem, axis=1), axis=0) / (64 * self.resolution**2)
        
        profile_curv = d2z_dx2 + d2z_dy2
        plan_curv = d2z_dxdy
        
        self.features['profile_curvature'] = profile_curv
        self.features['plan_curvature'] = plan_curv
        
        return profile_curv, plan_curv
    
    def calculate_twi(self) -> np.ndarray:
        """计算地形湿度指数 (TWI)"""
        if 'slope' not in self.features:
            self.calculate_slope()
        if 'flow_accumulation' not in self.features:
            self.calculate_flow_accumulation()
        
        slope = self.features['slope']
        flow_acc = self.features['flow_accumulation']
        
        slope_rad = np.radians(slope + 0.001)
        twi = np.log((flow_acc + 1) / np.tan(slope_rad))
        
        self.features['twi'] = twi
        return twi
    
    def extract_all_features(self) -> Dict[str, np.ndarray]:
        """提取所有地形特征"""
        logger.info("提取所有地形特征...")
        
        self.features['elevation'] = self.dem
        self.calculate_slope()
        self.calculate_aspect()
        self.calculate_flow_accumulation()
        self.calculate_curvature()
        self.calculate_twi()
        
        logger.info(f"提取了 {len(self.features)} 个地形特征")
        return self.features


class RadarFeatureExtractor:
    """雷达特征提取器"""
    
    def __init__(self, radar_data: np.ndarray = None):
        self.radar = radar_data
        self.features = {}
    
    def load_radar(self, filepath: str) -> np.ndarray:
        """加载雷达数据"""
        logger.info(f"加载雷达数据: {filepath}")
        
        ds = xr.open_dataset(filepath)
        
        var_names = ['reflectivity', 'dBZ', 'REF', 'dbz']
        var_name = None
        for vn in var_names:
            if vn in ds:
                var_name = vn
                break
        
        if var_name is None:
            raise ValueError(f"找不到反射率变量，可用变量: {list(ds.data_vars)}")
        
        self.radar = ds[var_name].values
        logger.info(f"雷达数据形状: {self.radar.shape}")
        
        return self.radar
    
    def extract_echo_intensity(self, threshold: float = 10.0) -> Dict[str, float]:
        """提取回波强度统计特征"""
        if self.radar is None:
            raise ValueError("请先加载雷达数据")
        
        data = self.radar[-1] if self.radar.ndim == 3 else self.radar
        
        valid_mask = data > threshold
        valid_data = data[valid_mask]
        
        features = {
            'echo_mean': np.mean(valid_data) if len(valid_data) > 0 else 0,
            'echo_max': np.max(valid_data) if len(valid_data) > 0 else 0,
            'echo_std': np.std(valid_data) if len(valid_data) > 0 else 0,
            'echo_coverage': np.sum(valid_mask) / valid_mask.size,
        }
        
        self.features.update(features)
        return features
    
    def detect_convective_cells(self, threshold: float = 40.0,
                                 min_size: int = 10) -> np.ndarray:
        """检测对流单体"""
        if self.radar is None:
            raise ValueError("请先加载雷达数据")
        
        data = self.radar[-1] if self.radar.ndim == 3 else self.radar
        
        convective_mask = data > threshold
        labeled, num_features = ndimage.label(convective_mask)
        
        for i in range(1, num_features + 1):
            if np.sum(labeled == i) < min_size:
                labeled[labeled == i] = 0
        
        labeled, num_features = ndimage.label(labeled > 0)
        
        logger.info(f"检测到 {num_features} 个对流单体")
        
        self.features['convective_cells'] = labeled
        self.features['num_convective_cells'] = num_features
        
        return labeled
    
    def extract_all_features(self) -> Dict[str, Any]:
        """提取所有雷达特征"""
        logger.info("提取所有雷达特征...")
        
        self.extract_echo_intensity()
        self.detect_convective_cells()
        
        logger.info(f"提取了 {len(self.features)} 个雷达特征")
        return self.features


class TemporalFeatureBuilder:
    """时序特征构建器"""
    
    def __init__(self, window_size: int = 6):
        self.window_size = window_size
    
    def build_features(self, data: np.ndarray) -> np.ndarray:
        """构建时序特征"""
        if data.ndim == 3:
            T, H, W = data.shape
        elif data.ndim == 4:
            T, C, H, W = data.shape
            data = data.reshape(T, -1, H, W)
        else:
            raise ValueError(f"不支持的数据维度: {data.ndim}")
        
        features = []
        
        for t in range(self.window_size, T):
            window = data[t-self.window_size:t]
            
            feat_mean = np.mean(window, axis=0)
            feat_std = np.std(window, axis=0)
            feat_max = np.max(window, axis=0)
            feat_min = np.min(window, axis=0)
            feat_range = feat_max - feat_min
            feat_trend = window[-1] - window[0]
            
            diffs = np.diff(window, axis=0)
            feat_change_rate = np.mean(np.abs(diffs), axis=0)
            
            feat = np.stack([feat_mean, feat_std, feat_max, feat_min,
                           feat_range, feat_trend, feat_change_rate], axis=0)
            features.append(feat)
        
        return np.array(features)
    
    def build_training_data(self, data: np.ndarray,
                            forecast_steps: int = 6) -> Tuple[np.ndarray, np.ndarray]:
        """构建训练用的特征和目标"""
        T, H, W = data.shape
        
        X, y = [], []
        
        for t in range(self.window_size, T - forecast_steps):
            window = data[t-self.window_size:t]
            target = data[t:t+forecast_steps]
            
            X.append(window)
            y.append(target)
        
        return np.array(X), np.array(y)


if __name__ == "__main__":
    # 测试地形特征提取
    print("测试地形特征提取...")
    
    test_dem = np.random.rand(100, 100) * 1000
    test_dem[30:70, 30:70] += 500
    
    extractor = TerrainFeatureExtractor(test_dem, resolution=30.0)
    features = extractor.extract_all_features()
    
    print(f"\n提取的特征:")
    for name, data in features.items():
        print(f"  {name}: shape={data.shape}, range=[{data.min():.2f}, {data.max():.2f}]")
