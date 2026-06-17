#!/usr/bin/env python
"""
ERA5 数据下载脚本
使用 CDS API 下载 ERA5 再分析数据

使用前需要:
1. 注册 CDS 账号: https://cds.climate.copernicus.eu/
2. 获取 API Key: https://cds.climate.copernicus.eu/api-how-to
3. 配置 ~/.cdsapirc 文件
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_cdsapi():
    """检查 cdsapi 是否安装"""
    try:
        import cdsapi
        return True
    except ImportError:
        logger.error("cdsapi 未安装，请运行: pip install cdsapi")
        return False


def download_era5_single_level(
    variables: List[str],
    start_date: str,
    end_date: str,
    bbox: Tuple[float, float, float, float],
    output_path: str,
    time_resolution: str = 'hourly',
    pressure_level: str = 'surface'
) -> str:
    """
    下载 ERA5 单层数据
    
    Args:
        variables: 变量列表
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        bbox: 边界框 (lat_min, lat_max, lon_min, lon_max)
        output_path: 输出路径
        time_resolution: 时间分辨率 ('hourly', 'monthly')
        pressure_level: 气压层 ('surface', 'pressure-levels')
        
    Returns:
        输出文件路径
    """
    import cdsapi
    
    c = cdsapi.Client()
    
    # 解析日期
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    years = list(range(start.year, end.year + 1))
    months = list(range(1, 13))
    days = [f'{d:02d}' for d in range(1, 32)]
    hours = [f'{h:02d}:00' for h in range(24)]
    
    # 边界框
    lat_min, lat_max, lon_min, lon_max = bbox
    area = [lat_max, lon_min, lat_min, lon_max]
    
    # 数据集名称
    if time_resolution == 'hourly':
        dataset = 'reanalysis-era5-single-levels'
        product_type = 'reanalysis'
    else:
        dataset = 'reanalysis-era5-single-levels-monthly-means'
        product_type = 'monthly_averaged_reanalysis'
    
    # 构建请求
    request = {
        'product_type': product_type,
        'variable': variables,
        'year': years,
        'month': months,
        'day': days,
        'time': hours,
        'area': area,
        'format': 'netcdf',
    }
    
    # 输出文件
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f'era5_{start_date}_{end_date}.nc'
    
    logger.info(f"开始下载 ERA5 数据...")
    logger.info(f"  变量: {variables}")
    logger.info(f"  时间: {start_date} 至 {end_date}")
    logger.info(f"  区域: {area}")
    logger.info(f"  输出: {output_file}")
    
    try:
        c.retrieve(dataset, request, str(output_file))
        logger.info(f"下载完成: {output_file}")
        return str(output_file)
    except Exception as e:
        logger.error(f"下载失败: {e}")
        raise


def download_era5_pressure_levels(
    variables: List[str],
    pressure_levels: List[int],
    start_date: str,
    end_date: str,
    bbox: Tuple[float, float, float, float],
    output_path: str
) -> str:
    """
    下载 ERA5 气压层数据
    
    Args:
        variables: 变量列表
        pressure_levels: 气压层列表 (hPa)
        start_date: 开始日期
        end_date: 结束日期
        bbox: 边界框
        output_path: 输出路径
        
    Returns:
        输出文件路径
    """
    import cdsapi
    
    c = cdsapi.Client()
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    years = list(range(start.year, end.year + 1))
    months = list(range(1, 13))
    days = [f'{d:02d}' for d in range(1, 32)]
    hours = [f'{h:02d}:00' for h in range(24)]
    
    lat_min, lat_max, lon_min, lon_max = bbox
    area = [lat_max, lon_min, lat_min, lon_max]
    
    request = {
        'product_type': 'reanalysis',
        'variable': variables,
        'pressure_level': [str(pl) for pl in pressure_levels],
        'year': years,
        'month': months,
        'day': days,
        'time': hours,
        'area': area,
        'format': 'netcdf',
    }
    
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f'era5_pressure_{start_date}_{end_date}.nc'
    
    logger.info(f"开始下载 ERA5 气压层数据...")
    
    try:
        c.retrieve('reanalysis-era5-pressure-levels', request, str(output_file))
        logger.info(f"下载完成: {output_file}")
        return str(output_file)
    except Exception as e:
        logger.error(f"下载失败: {e}")
        raise


def download_for_railway_project(
    output_path: str = 'data/external/era5',
    start_year: int = 2015,
    end_year: int = 2024,
    bbox: Tuple[float, float, float, float] = (32.0, 42.0, 100.0, 110.0)
):
    """
    下载铁路项目所需的 ERA5 数据
    
    默认覆盖西北地区铁路沿线 (甘肃、青海、宁夏)
    
    Args:
        output_path: 输出路径
        start_year: 开始年份
        end_year: 结束年份
        bbox: 边界框 (lat_min, lat_max, lon_min, lon_max)
    """
    # 常用变量
    surface_variables = [
        '2m_temperature',           # t2m - 2米温度
        '2m_dewpoint_temperature',  # d2m - 2米露点温度
        '10m_u_component_of_wind',  # u10 - 10米u风
        '10m_v_component_of_wind',  # v10 - 10米v风
        'surface_pressure',         # sp - 地面气压
        'total_precipitation',      # tp - 总降水量
        'convective_available_potential_energy',  # cape - 对流有效位能
        'total_column_water_vapour',  # tcwv - 总柱水汽
        'mean_sea_level_pressure',    # msl - 海平面气压
        'relative_humidity',          # rh - 相对湿度
    ]
    
    # 按年份下载
    for year in range(start_year, end_year + 1):
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        logger.info(f"\n{'='*50}")
        logger.info(f"下载 {year} 年数据")
        logger.info(f"{'='*50}")
        
        try:
            download_era5_single_level(
                variables=surface_variables,
                start_date=start_date,
                end_date=end_date,
                bbox=bbox,
                output_path=output_path
            )
        except Exception as e:
            logger.error(f"{year} 年数据下载失败: {e}")
            continue
    
    logger.info("\n所有年份下载完成!")


def main():
    parser = argparse.ArgumentParser(description='ERA5 数据下载脚本')
    parser.add_argument('--output', '-o', type=str, default='data/external/era5',
                       help='输出路径')
    parser.add_argument('--start-year', type=int, default=2015,
                       help='开始年份')
    parser.add_argument('--end-year', type=int, default=2024,
                       help='结束年份')
    parser.add_argument('--lat-min', type=float, default=32.0,
                       help='最小纬度')
    parser.add_argument('--lat-max', type=float, default=42.0,
                       help='最大纬度')
    parser.add_argument('--lon-min', type=float, default=100.0,
                       help='最小经度')
    parser.add_argument('--lon-max', type=float, default=110.0,
                       help='最大经度')
    parser.add_argument('--variables', '-v', type=str, nargs='+',
                       default=['2m_temperature', 'total_precipitation'],
                       help='变量列表')
    parser.add_argument('--single', action='store_true',
                       help='只下载单年数据')
    
    args = parser.parse_args()
    
    if not check_cdsapi():
        sys.exit(1)
    
    bbox = (args.lat_min, args.lat_max, args.lon_min, args.lon_max)
    
    if args.single:
        # 下载单年数据
        start_date = f'{args.start_year}-01-01'
        end_date = f'{args.start_year}-12-31'
        
        download_era5_single_level(
            variables=args.variables,
            start_date=start_date,
            end_date=end_date,
            bbox=bbox,
            output_path=args.output
        )
    else:
        # 下载多年数据
        download_for_railway_project(
            output_path=args.output,
            start_year=args.start_year,
            end_year=args.end_year,
            bbox=bbox
        )


if __name__ == '__main__':
    main()
