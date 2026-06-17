"""
数据预处理模块
负责数据清洗、质量控制、标准化
"""

import numpy as np
import pandas as pd
import xarray as xr
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """数据预处理器"""
    
    def __init__(self, config: dict = None):
        """
        初始化预处理器
        
        Args:
            config: 配置字典，包含缺失值阈值、异常值范围等
        """
        self.config = config or {}
        self.missing_threshold = self.config.get('missing_threshold', 0.3)
        self.outlier_method = self.config.get('outlier_method', 'iqr')
        self.stats = {}  # 存储统计信息
    
    def load_rainfall_data(self, filepath: str, 
                           time_col: str = 'timestamp',
                           station_col: str = 'station_id',
                           value_col: str = 'precipitation') -> pd.DataFrame:
        """
        加载铁路雨量计数据
        
        Args:
            filepath: 数据文件路径 (.csv, .xlsx, .parquet)
            time_col: 时间列名
            station_col: 站点列名
            value_col: 降水量列名
            
        Returns:
            DataFrame包含时间戳、站点ID、降水量等
        """
        logger.info(f"加载数据: {filepath}")
        
        filepath = Path(filepath)
        
        if filepath.suffix == '.csv':
            df = pd.read_csv(filepath)
        elif filepath.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        elif filepath.suffix == '.parquet':
            df = pd.read_parquet(filepath)
        else:
            raise ValueError(f"不支持的文件格式: {filepath.suffix}")
        
        # 标准化列名
        df.columns = df.columns.str.lower().str.strip()
        
        # 转换时间列
        if time_col in df.columns:
            df[time_col] = pd.to_datetime(df[time_col])
            df = df.sort_values(time_col)
        
        logger.info(f"数据形状: {df.shape}")
        logger.info(f"时间范围: {df[time_col].min()} 至 {df[time_col].max()}")
        logger.info(f"站点数量: {df[station_col].nunique()}")
        
        return df
    
    def quality_control(self, data: pd.DataFrame, 
                        value_col: str = 'precipitation',
                        station_col: str = 'station_id') -> pd.DataFrame:
        """
        数据质量控制
        
        Args:
            data: 原始数据
            value_col: 数值列名
            station_col: 站点列名
            
        Returns:
            质量控制后的数据
        """
        logger.info("开始质量控制...")
        original_len = len(data)
        
        # 1. 缺失值检测
        data = self._detect_missing(data, value_col)
        
        # 2. 异常值检测
        data = self._remove_outliers(data, value_col, station_col)
        
        # 3. 一致性检验
        data = self._consistency_check(data, value_col, station_col)
        
        # 4. 添加质量标记
        data = self._add_quality_flag(data, value_col)
        
        # 统计信息
        self.stats['quality_control'] = {
            'original_count': original_len,
            'final_count': len(data),
            'removed_count': original_len - len(data),
            'removed_ratio': (original_len - len(data)) / original_len
        }
        
        logger.info(f"质量控制完成: {original_len} -> {len(data)} 条记录")
        
        return data
    
    def _detect_missing(self, data: pd.DataFrame, value_col: str) -> pd.DataFrame:
        """检测并标记缺失值"""
        missing_count = data[value_col].isna().sum()
        missing_ratio = missing_count / len(data)
        
        logger.info(f"缺失值: {missing_count} ({missing_ratio:.2%})")
        
        self.stats['missing'] = {
            'count': missing_count,
            'ratio': missing_ratio
        }
        
        # 如果缺失比例超过阈值，发出警告
        if missing_ratio > self.missing_threshold:
            logger.warning(f"缺失值比例 {missing_ratio:.2%} 超过阈值 {self.missing_threshold:.2%}")
        
        return data
    
    def _remove_outliers(self, data: pd.DataFrame, 
                         value_col: str,
                         station_col: str) -> pd.DataFrame:
        """去除异常值"""
        if self.outlier_method == 'iqr':
            return self._remove_outliers_iqr(data, value_col, station_col)
        elif self.outlier_method == 'zscore':
            return self._remove_outliers_zscore(data, value_col, station_col)
        else:
            return data
    
    def _remove_outliers_iqr(self, data: pd.DataFrame,
                              value_col: str,
                              station_col: str) -> pd.DataFrame:
        """使用IQR方法去除异常值"""
        outlier_count = 0
        
        # 按站点分组处理
        for station in data[station_col].unique():
            mask = data[station_col] == station
            station_data = data.loc[mask, value_col]
            
            Q1 = station_data.quantile(0.25)
            Q3 = station_data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # 标记异常值（不删除，用NaN替代）
            outlier_mask = mask & ((data[value_col] < lower_bound) | (data[value_col] > upper_bound))
            outlier_count += outlier_mask.sum()
            data.loc[outlier_mask, value_col] = np.nan
        
        logger.info(f"IQR异常值检测: 发现 {outlier_count} 个异常值")
        
        self.stats['outliers'] = {
            'method': 'iqr',
            'count': outlier_count
        }
        
        return data
    
    def _remove_outliers_zscore(self, data: pd.DataFrame,
                                  value_col: str,
                                  station_col: str) -> pd.DataFrame:
        """使用Z-score方法去除异常值"""
        outlier_count = 0
        threshold = 3.0
        
        for station in data[station_col].unique():
            mask = data[station_col] == station
            station_data = data.loc[mask, value_col]
            
            mean = station_data.mean()
            std = station_data.std()
            
            if std > 0:
                z_scores = np.abs((station_data - mean) / std)
                outlier_mask = mask & (z_scores > threshold)
                outlier_count += outlier_mask.sum()
                data.loc[outlier_mask, value_col] = np.nan
        
        logger.info(f"Z-score异常值检测: 发现 {outlier_count} 个异常值")
        
        self.stats['outliers'] = {
            'method': 'zscore',
            'count': outlier_count
        }
        
        return data
    
    def _consistency_check(self, data: pd.DataFrame,
                           value_col: str,
                           station_col: str) -> pd.DataFrame:
        """一致性检验"""
        # 1. 降水量非负检查
        negative_count = (data[value_col] < 0).sum()
        if negative_count > 0:
            logger.warning(f"发现 {negative_count} 条负值记录，已设为NaN")
            data.loc[data[value_col] < 0, value_col] = np.nan
        
        # 2. 时间序列连续性检查
        # TODO: 实现更复杂的一致性检查
        
        return data
    
    def _add_quality_flag(self, data: pd.DataFrame, value_col: str) -> pd.DataFrame:
        """添加质量标记"""
        # 0: 优质数据, 1: 插值数据, 2: 可疑数据, 3: 缺失数据
        data['quality_flag'] = 0
        
        # 标记缺失值
        data.loc[data[value_col].isna(), 'quality_flag'] = 3
        
        return data
    
    def normalize(self, data: np.ndarray, method: str = 'minmax') -> Tuple[np.ndarray, dict]:
        """
        数据标准化
        
        Args:
            data: 输入数据
            method: 标准化方法 ('minmax', 'zscore')
            
        Returns:
            标准化后的数据和参数
        """
        if method == 'minmax':
            data_min = np.nanmin(data)
            data_max = np.nanmax(data)
            normalized = (data - data_min) / (data_max - data_min + 1e-8)
            params = {'min': data_min, 'max': data_max}
        elif method == 'zscore':
            data_mean = np.nanmean(data)
            data_std = np.nanstd(data)
            normalized = (data - data_mean) / (data_std + 1e-8)
            params = {'mean': data_mean, 'std': data_std}
        else:
            raise ValueError(f"未知的标准化方法: {method}")
        
        return normalized, params
    
    def denormalize(self, data: np.ndarray, params: dict, method: str = 'minmax') -> np.ndarray:
        """反标准化"""
        if method == 'minmax':
            return data * (params['max'] - params['min']) + params['min']
        elif method == 'zscore':
            return data * params['std'] + params['mean']
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.stats


class RadarProcessor:
    """雷达数据处理"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def load_radar_data(self, filepath: str) -> xr.Dataset:
        """
        加载雷达拼图数据
        
        Args:
            filepath: 数据文件路径 (.nc, .grb, .bin)
            
        Returns:
            xarray Dataset
        """
        logger.info(f"加载雷达数据: {filepath}")
        
        filepath = Path(filepath)
        
        if filepath.suffix == '.nc':
            ds = xr.open_dataset(filepath)
        elif filepath.suffix in ['.grb', '.grib', '.grib2']:
            ds = xr.open_dataset(filepath, engine='cfgrib')
        else:
            raise ValueError(f"不支持的文件格式: {filepath.suffix}")
        
        logger.info(f"雷达数据维度: {dict(ds.dims)}")
        
        return ds
    
    def extract_features(self, radar_data: xr.Dataset,
                         reflectivity_var: str = 'reflectivity') -> dict:
        """
        提取雷达特征
        
        Args:
            radar_data: 雷达数据集
            reflectivity_var: 反射率变量名
            
        Returns:
            包含回波强度、回波顶高、VIL等特征的字典
        """
        features = {}
        
        # 获取反射率数据
        if reflectivity_var in radar_data:
            ref = radar_data[reflectivity_var]
            
            # 基本统计特征
            features['reflectivity_mean'] = ref.mean().values
            features['reflectivity_max'] = ref.max().values
            features['reflectivity_std'] = ref.std().values
            
            # 回波面积（超过阈值的像素数）
            thresholds = [20, 30, 40, 50]  # dBZ
            for thresh in thresholds:
                features[f'echo_area_{thresh}dBZ'] = (ref > thresh).sum().values
        
        logger.info(f"提取了 {len(features)} 个雷达特征")
        
        return features
    
    def calculate_vil(self, radar_data: xr.Dataset) -> np.ndarray:
        """
        计算垂直积分液态水含量 (VIL)
        
        VIL = 3.44 * 10^-6 * Z^(4/7) 对垂直方向积分
        
        Args:
            radar_data: 包含三维反射率的数据集
            
        Returns:
            VIL数组 (kg/m²)
        """
        # TODO: 实现VIL计算
        pass
    
    def calculate_echo_top(self, radar_data: xr.Dataset,
                           threshold: float = 18.0) -> np.ndarray:
        """
        计算回波顶高
        
        Args:
            radar_data: 包含三维反射率的数据集
            threshold: 回波阈值 (dBZ)
            
        Returns:
            回波顶高数组 (km)
        """
        # TODO: 实现回波顶高计算
        pass


class ERA5Processor:
    """ERA5再分析数据处理"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.default_variables = [
            't2m',    # 2米温度
            'd2m',    # 2米露点温度
            'u10',    # 10米u风
            'v10',    # 10米v风
            'sp',     # 地面气压
            'tp',     # 总降水量
            'cape',   # 对流有效位能
            'tcwv',   # 总柱水汽
        ]
    
    def load_era5(self, filepath: str) -> xr.Dataset:
        """
        加载ERA5数据
        
        Args:
            filepath: 数据文件路径
            
        Returns:
            xarray Dataset
        """
        logger.info(f"加载ERA5数据: {filepath}")
        
        ds = xr.open_dataset(filepath)
        
        # 转换时间维度
        if 'time' in ds.coords:
            ds['time'] = pd.to_datetime(ds['time'].values)
        
        logger.info(f"ERA5数据维度: {dict(ds.dims)}")
        logger.info(f"变量: {list(ds.data_vars)}")
        
        return ds
    
    def process(self, data: xr.Dataset,
                target_resolution: float = None) -> xr.Dataset:
        """
        处理ERA5数据
        
        Args:
            data: 原始ERA5数据
            target_resolution: 目标分辨率（度）
            
        Returns:
            处理后的数据
        """
        # 1. 单位转换
        data = self._convert_units(data)
        
        # 2. 插值到目标分辨率
        if target_resolution:
            data = self._interpolate(data, target_resolution)
        
        # 3. 计算派生变量
        data = self._compute_derived_vars(data)
        
        return data
    
    def _convert_units(self, data: xr.Dataset) -> xr.Dataset:
        """单位转换"""
        # 温度从K转换为°C
        if 't2m' in data:
            data['t2m_celsius'] = data['t2m'] - 273.15
        
        if 'd2m' in data:
            data['d2m_celsius'] = data['d2m'] - 273.15
        
        # 降水量从m转换为mm
        if 'tp' in data:
            data['tp_mm'] = data['tp'] * 1000
        
        # 气压从Pa转换为hPa
        if 'sp' in data:
            data['sp_hpa'] = data['sp'] / 100
        
        return data
    
    def _interpolate(self, data: xr.Dataset, 
                     target_resolution: float) -> xr.Dataset:
        """插值到目标分辨率"""
        # TODO: 实现插值
        return data
    
    def _compute_derived_vars(self, data: xr.Dataset) -> xr.Dataset:
        """计算派生变量"""
        # 计算相对湿度
        if 't2m' in data and 'd2m' in data:
            # 使用Magnus公式
            t = data['t2m'] - 273.15  # °C
            td = data['d2m'] - 273.15  # °C
            
            # 饱和水汽压
            es = 6.112 * np.exp((17.67 * t) / (t + 243.5))
            e = 6.112 * np.exp((17.67 * td) / (td + 243.5))
            
            # 相对湿度
            data['rh'] = 100 * e / es
        
        # 计算风速
        if 'u10' in data and 'v10' in data:
            data['wind_speed'] = np.sqrt(data['u10']**2 + data['v10']**2)
            data['wind_direction'] = np.arctan2(data['v10'], data['u10']) * 180 / np.pi
        
        return data
    
    def extract_for_training(self, data: xr.Dataset,
                             time_range: Tuple[str, str],
                             bbox: Tuple[float, float, float, float]) -> np.ndarray:
        """
        提取训练数据
        
        Args:
            data: ERA5数据集
            time_range: 时间范围
            bbox: 边界框 (lat_min, lat_max, lon_min, lon_max)
            
        Returns:
            训练数据数组
        """
        # 选择时间范围
        data = data.sel(time=slice(time_range[0], time_range[1]))
        
        # 选择空间范围
        lat_min, lat_max, lon_min, lon_max = bbox
        data = data.sel(
            latitude=slice(lat_max, lat_min),
            longitude=slice(lon_min, lon_max)
        )
        
        return data


class DataPipeline:
    """数据处理流水线"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.preprocessor = DataPreprocessor(config)
        self.radar_processor = RadarProcessor(config)
        self.era5_processor = ERA5Processor(config)
    
    def run(self, rainfall_path: str = None,
            radar_path: str = None,
            era5_path: str = None,
            output_path: str = None) -> dict:
        """
        运行数据处理流水线
        
        Args:
            rainfall_path: 雨量计数据路径
            radar_path: 雷达数据路径
            era5_path: ERA5数据路径
            output_path: 输出路径
            
        Returns:
            处理结果
        """
        results = {}
        
        # 1. 处理雨量计数据
        if rainfall_path:
            logger.info("=" * 50)
            logger.info("处理雨量计数据")
            rainfall_data = self.preprocessor.load_rainfall_data(rainfall_path)
            rainfall_data = self.preprocessor.quality_control(rainfall_data)
            results['rainfall'] = rainfall_data
        
        # 2. 处理雷达数据
        if radar_path:
            logger.info("=" * 50)
            logger.info("处理雷达数据")
            radar_data = self.radar_processor.load_radar_data(radar_path)
            radar_features = self.radar_processor.extract_features(radar_data)
            results['radar'] = {'data': radar_data, 'features': radar_features}
        
        # 3. 处理ERA5数据
        if era5_path:
            logger.info("=" * 50)
            logger.info("处理ERA5数据")
            era5_data = self.era5_processor.load_era5(era5_path)
            era5_data = self.era5_processor.process(era5_data)
            results['era5'] = era5_data
        
        # 4. 保存结果
        if output_path:
            self._save_results(results, output_path)
        
        return results
    
    def _save_results(self, results: dict, output_path: str):
        """保存处理结果"""
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for name, data in results.items():
            if isinstance(data, pd.DataFrame):
                data.to_parquet(output_path / f"{name}.parquet")
            elif isinstance(data, xr.Dataset):
                data.to_netcdf(output_path / f"{name}.nc")
        
        logger.info(f"结果已保存到: {output_path}")


if __name__ == "__main__":
    # 测试数据预处理器
    preprocessor = DataPreprocessor()
    
    # 创建测试数据
    np.random.seed(42)
    test_data = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=1000, freq='H'),
        'station_id': np.random.choice(['S001', 'S002', 'S003'], 1000),
        'precipitation': np.random.exponential(2, 1000)
    })
    
    # 添加一些异常值和缺失值
    test_data.loc[100:110, 'precipitation'] = 100  # 异常值
    test_data.loc[200:220, 'precipitation'] = np.nan  # 缺失值
    test_data.loc[300, 'precipitation'] = -5  # 负值
    
    # 质量控制
    cleaned_data = preprocessor.quality_control(test_data)
    
    print("\n统计信息:")
    print(preprocessor.get_stats())
