#!/usr/bin/env python
"""
DEM 数据下载和处理脚本
支持 SRTM 和 ASTER GDEM 数据

SRTM 数据下载:
1. 注册 NASA EarthData 账号: https://urs.earthdata.nasa.gov/
2. 访问 SRTM 数据: https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/
3. 下载对应区域的 .hgt 文件

ASTER GDEM 数据下载:
1. 注册 NASA EarthData 账号
2. 访问: https://search.earthdata.nasa.gov/
3. 搜索 "ASTER GDEM"
"""

import os
import sys
from pathlib import Path
from typing import Tuple, List, Optional
import argparse
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_dependencies():
    """检查依赖"""
    missing = []
    
    try:
        import rasterio
    except ImportError:
        missing.append('rasterio')
    
    try:
        import xarray
    except ImportError:
        missing.append('xarray')
    
    if missing:
        logger.error(f"缺少依赖: {', '.join(missing)}")
        logger.error(f"请运行: pip install {' '.join(missing)}")
        return False
    
    return True


def read_srtm_hgt(filepath: str) -> np.ndarray:
    """
    读取 SRTM .hgt 文件
    
    SRTM1: 3601x3601 像素, 30m 分辨率
    SRTM3: 1201x1201 像素, 90m 分辨率
    
    Args:
        filepath: .hgt 文件路径
        
    Returns:
        高程数组
    """
    filepath = Path(filepath)
    
    # 确定文件大小
    file_size = filepath.stat().st_size
    
    if file_size == 3601 * 3601 * 2:
        # SRTM1 (30m)
        shape = (3601, 3601)
        resolution = 30 / 111320  # 度
    elif file_size == 1201 * 1201 * 2:
        # SRTM3 (90m)
        shape = (1201, 1201)
        resolution = 90 / 111320
    else:
        raise ValueError(f"未知的 SRTM 文件大小: {file_size}")
    
    # 读取数据 (大端序, 16位有符号整数)
    data = np.fromfile(filepath, dtype='>i2')
    data = data.reshape(shape).astype(np.float32)
    
    # 无效值处理
    data[data < -1000] = np.nan
    
    logger.info(f"读取 SRTM 文件: {filepath.name}")
    logger.info(f"  形状: {shape}")
    logger.info(f"  高程范围: {np.nanmin(data):.1f} - {np.nanmax(data):.1f} m")
    
    return data


def parse_srtm_filename(filename: str) -> Tuple[float, float]:
    """
    解析 SRTM 文件名获取经纬度
    
    文件名格式: N36E103.hgt (北纬36度, 东经103度)
    
    Args:
        filename: 文件名
        
    Returns:
        (纬度, 经度)
    """
    filename = Path(filename).stem
    
    # 解析纬度
    if filename[0] == 'N':
        lat = int(filename[1:3])
    elif filename[0] == 'S':
        lat = -int(filename[1:3])
    else:
        raise ValueError(f"无法解析纬度: {filename}")
    
    # 解析经度
    if filename[3] == 'E':
        lon = int(filename[4:7])
    elif filename[3] == 'W':
        lon = -int(filename[4:7])
    else:
        raise ValueError(f"无法解析经度: {filename}")
    
    return lat, lon


def merge_srtm_tiles(tile_dir: str, output_path: str):
    """
    合并多个 SRTM 瓦片
    
    Args:
        tile_dir: 瓦片目录
        output_path: 输出文件路径
    """
    import rasterio
    from rasterio.merge import merge
    
    tile_dir = Path(tile_dir)
    hgt_files = list(tile_dir.glob('*.hgt'))
    
    if not hgt_files:
        logger.error(f"未找到 .hgt 文件: {tile_dir}")
        return
    
    logger.info(f"找到 {len(hgt_files)} 个瓦片文件")
    
    # 读取所有瓦片
    datasets = []
    for hgt_file in hgt_files:
        # 转换为 GeoTIFF
        data = read_srtm_hgt(str(hgt_file))
        lat, lon = parse_srtm_filename(hgt_file.name)
        
        # 创建临时文件
        temp_tif = hgt_file.with_suffix('.tif')
        
        # 写入 GeoTIFF
        transform = rasterio.transform.from_origin(
            lon, lat + 1,  # 左上角
            30 / 111320,   # x 分辨率 (度)
            -30 / 111320   # y 分辨率 (度)
        )
        
        with rasterio.open(
            temp_tif, 'w',
            driver='GTiff',
            height=data.shape[0],
            width=data.shape[1],
            count=1,
            dtype=data.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=-32768
        ) as dst:
            dst.write(data, 1)
        
        datasets.append(rasterio.open(temp_tif))
    
    # 合并
    logger.info("合并瓦片...")
    mosaic, out_trans = merge(datasets)
    
    # 保存结果
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / 'dem_merged.tif'
    
    with rasterio.open(
        output_file, 'w',
        driver='GTiff',
        height=mosaic.shape[1],
        width=mosaic.shape[2],
        count=1,
        dtype=mosaic.dtype,
        crs='EPSG:4326',
        transform=out_trans,
        nodata=-32768
    ) as dst:
        dst.write(mosaic)
    
    logger.info(f"合并完成: {output_file}")
    
    # 清理临时文件
    for ds in datasets:
        ds.close()
    for hgt_file in hgt_files:
        temp_tif = hgt_file.with_suffix('.tif')
        if temp_tif.exists():
            temp_tif.unlink()


def download_srtm_guide():
    """打印 SRTM 下载指南"""
    guide = """
================================================================================
                           SRTM DEM 数据下载指南
================================================================================

1. 注册 NASA EarthData 账号
   - 访问: https://urs.earthdata.nasa.gov/
   - 点击 "Register" 创建账号
   - 完成邮箱验证

2. 下载 SRTM 数据
   - 访问: https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/
   - 或使用 EarthExplorer: https://earthexplorer.usgs.gov/
   - 选择覆盖你研究区域的瓦片

3. 瓦片命名规则
   - 格式: N36E103.hgt
   - N/S: 北纬/南纬
   - E/W: 东经/西经
   - 示例: N36E103 覆盖北纬36-37度, 东经103-104度

4. 甘肃地区需要的瓦片 (示例)
   - N32E100, N32E101, N32E102, N32E103, N32E104, N32E105
   - N33E100, N33E101, N33E102, N33E103, N33E104, N33E105
   - N34E100, N34E101, N34E102, N34E103, N34E104, N34E105
   - N35E100, N35E101, N35E102, N35E103, N35E104, N35E105
   - N36E100, N36E101, N36E102, N36E103, N36E104, N36E105
   - N37E100, N37E101, N37E102, N37E103, N37E104, N37E105
   - N38E100, N38E101, N38E102, N38E103, N38E104, N38E105
   - N39E100, N39E101, N39E102, N39E103, N39E104, N39E105
   - N40E100, N40E101, N40E102, N40E103, N40E104, N40E105
   - N41E100, N41E101, N41E102, N41E103, N41E104, N41E105

5. 使用本脚本处理
   python scripts/download_dem.py --merge --tile-dir /path/to/hgt/files --output data/external/dem

================================================================================
"""
    print(guide)


def process_dem(input_path: str, output_path: str, 
                 target_resolution: float = None,
                 clip_bbox: Tuple[float, float, float, float] = None):
    """
    处理 DEM 数据
    
    Args:
        input_path: 输入 DEM 文件
        output_path: 输出路径
        target_resolution: 目标分辨率 (米)
        clip_bbox: 裁剪边界框
    """
    import rasterio
    from rasterio.warp import reproject, calculate_default_transform, Resampling
    
    with rasterio.open(input_path) as src:
        data = src.read(1)
        profile = src.profile
        
        logger.info(f"DEM 信息:")
        logger.info(f"  形状: {data.shape}")
        logger.info(f"  CRS: {profile['crs']}")
        logger.info(f"  分辨率: {src.res}")
        logger.info(f"  高程范围: {np.nanmin(data):.1f} - {np.nanmax(data):.1f} m")
        
        # 裁剪
        if clip_bbox:
            from rasterio.mask import mask
            from shapely.geometry import box
            
            lat_min, lat_max, lon_min, lon_max = clip_bbox
            bbox_geom = box(lon_min, lat_min, lon_max, lat_max)
            
            data, transform = mask(src, [bbox_geom], crop=True)
            data = data[0]
            
            profile.update({
                'height': data.shape[0],
                'width': data.shape[1],
                'transform': transform
            })
            
            logger.info(f"裁剪后形状: {data.shape}")
        
        # 重采样
        if target_resolution:
            # 计算新的变换
            target_res_deg = target_resolution / 111320  # 近似转换
            new_transform, new_width, new_height = calculate_default_transform(
                profile['crs'], profile['crs'],
                profile['width'], profile['height'],
                *src.bounds,
                resolution=(target_res_deg, target_res_deg)
            )
            
            # 重采样
            resampled = np.empty((new_height, new_width), dtype=np.float32)
            reproject(
                source=data,
                destination=resampled,
                src_transform=profile['transform'],
                src_crs=profile['crs'],
                dst_transform=new_transform,
                dst_crs=profile['crs'],
                resampling=Resampling.bilinear
            )
            
            data = resampled
            profile.update({
                'height': new_height,
                'width': new_width,
                'transform': new_transform
            })
            
            logger.info(f"重采样后形状: {data.shape}")
    
    # 保存
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / 'dem_processed.tif'
    
    profile.update(dtype=np.float32, nodata=np.nan)
    
    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(data, 1)
    
    logger.info(f"处理完成: {output_file}")
    
    return data


def main():
    parser = argparse.ArgumentParser(description='DEM 数据处理脚本')
    parser.add_argument('--guide', action='store_true',
                       help='显示下载指南')
    parser.add_argument('--merge', action='store_true',
                       help='合并 SRTM 瓦片')
    parser.add_argument('--tile-dir', type=str,
                       help='SRTM 瓦片目录')
    parser.add_argument('--process', type=str,
                       help='处理 DEM 文件')
    parser.add_argument('--output', '-o', type=str, default='data/external/dem',
                       help='输出路径')
    parser.add_argument('--resolution', type=float,
                       help='目标分辨率 (米)')
    parser.add_argument('--clip', type=float, nargs=4,
                       metavar=('LAT_MIN', 'LAT_MAX', 'LON_MIN', 'LON_MAX'),
                       help='裁剪边界框')
    
    args = parser.parse_args()
    
    if args.guide:
        download_srtm_guide()
        return
    
    if not check_dependencies():
        sys.exit(1)
    
    if args.merge and args.tile_dir:
        merge_srtm_tiles(args.tile_dir, args.output)
    elif args.process:
        clip_bbox = tuple(args.clip) if args.clip else None
        process_dem(args.process, args.output, args.resolution, clip_bbox)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
