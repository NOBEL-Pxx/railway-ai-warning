"""
缺失值插补算法模块
"""

import numpy as np
import pandas as pd
from typing import Optional, List
from scipy.interpolate import interp1d, griddata
from sklearn.impute import KNNImputer


class MissingValueImputer:
    """缺失值插补器"""
    
    def __init__(self, method: str = 'linear'):
        """
        Args:
            method: 插补方法 ('linear', 'spline', 'knn', 'random_forest')
        """
        self.method = method
    
    def impute_timeseries(self, data: pd.Series) -> pd.Series:
        """
        时间序列插补
        
        Args:
            data: 带缺失值的时间序列
            
        Returns:
            插补后的时间序列
        """
        if self.method in ['linear', 'spline']:
            return data.interpolate(method=self.method)
        elif self.method == 'knn':
            imputer = KNNImputer(n_neighbors=5)
            values = imputer.fit_transform(data.values.reshape(-1, 1))
            return pd.Series(values.flatten(), index=data.index)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def impute_spatial(self, data: np.ndarray, 
                       lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
        """
        空间插补
        
        Args:
            data: 2D数组，缺失值为np.nan
            lats: 纬度网格
            lons: 经度网格
            
        Returns:
            插补后的数据
        """
        # 找到有效点和缺失点
        mask = ~np.isnan(data)
        points_valid = np.column_stack([lats[mask], lons[mask]])
        values_valid = data[mask]
        
        points_missing = np.column_stack([lats[~mask], lons[~mask]])
        
        # 使用griddata插值
        interpolated = griddata(points_valid, values_valid, points_missing, 
                               method='linear')
        
        result = data.copy()
        result[~mask] = interpolated
        
        return result
    
    def impute_spatiotemporal(self, data: np.ndarray) -> np.ndarray:
        """
        时空联合插补
        
        Args:
            data: 3D数组 (time, lat, lon)
            
        Returns:
            插补后的数据
        """
        # TODO: 实现时空联合插补
        # 可以使用DINEOF等方法
        return data


class SmartImputer:
    """智能插补器 - 根据缺失模式自动选择插补方法"""
    
    def __init__(self):
        self.imputer = None
    
    def analyze_missing_pattern(self, data: pd.DataFrame) -> dict:
        """
        分析缺失模式
        
        Returns:
            缺失模式统计
        """
        total_cells = data.size
        missing_cells = data.isnull().sum().sum()
        missing_ratio = missing_cells / total_cells
        
        # 检测缺失类型：随机缺失 vs 连续缺失
        missing_streaks = self._detect_streaks(data)
        
        return {
            'missing_ratio': missing_ratio,
            'max_streak': max(missing_streaks) if missing_streaks else 0,
            'missing_streaks': missing_streaks
        }
    
    def _detect_streaks(self, data: pd.DataFrame) -> List[int]:
        """检测连续缺失的长度"""
        streaks = []
        for col in data.columns:
            is_missing = data[col].isnull()
            streak_lengths = is_missing.astype(int).groupby(
                (is_missing != is_missing.shift()).cumsum()
            ).sum()
            streaks.extend(streak_lengths[streak_lengths > 0].tolist())
        return streaks
    
    def auto_impute(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        自动选择插补方法
        """
        pattern = self.analyze_missing_pattern(data)
        
        if pattern['missing_ratio'] < 0.05:
            # 少量随机缺失：线性插值
            self.imputer = MissingValueImputer(method='linear')
        elif pattern['max_streak'] < 6:
            # 中等连续缺失：样条插值
            self.imputer = MissingValueImputer(method='spline')
        else:
            # 大量连续缺失：KNN
            self.imputer = MissingValueImputer(method='knn')
        
        return data.apply(lambda col: self.imputer.impute_timeseries(col))
