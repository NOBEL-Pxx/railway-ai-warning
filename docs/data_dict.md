# 数据字典

## 铁路雨量计数据

| 字段 | 类型 | 说明 | 单位 |
|------|------|------|------|
| station_id | str | 站点编号 | - |
| timestamp | datetime | 时间戳 | - |
| latitude | float | 纬度 | 度 |
| longitude | float | 经度 | 度 |
| precipitation | float | 分钟降水量 | mm |
| quality_flag | int | 质量标记 | 0-3 |

## ERA5再分析数据

| 变量 | 说明 | 单位 | 分辨率 |
|------|------|------|--------|
| t2m | 2米温度 | K | 0.25° |
| d2m | 2米露点温度 | K | 0.25° |
| u10 | 10米u风 | m/s | 0.25° |
| v10 | 10米v风 | m/s | 0.25° |
| sp | 地面气压 | Pa | 0.25° |
| tp | 总降水量 | m | 0.25° |

## 雷达拼图数据

| 字段 | 说明 | 单位 |
|------|------|------|
| reflectivity | 雷达反射率 | dBZ |
| echo_top | 回波顶高 | km |
| vil | 垂直积分液态水 | kg/m² |

## DEM地形数据

| 数据集 | 分辨率 | 来源 |
|--------|--------|------|
| SRTM | 30m | NASA |
| ASTER GDEM | 30m | NASA/METI |

## 特征工程

### 地形特征
- slope: 坡度 (度)
- aspect: 坡向 (度)
- flow_acc: 汇流面积
- curvature: 曲率

### 雷达特征
- echo_intensity: 回波强度
- echo_motion: 回波运动矢量
- convective_flag: 对流标记

### 时序特征
- rolling_mean: 滑动平均
- rolling_std: 滑动标准差
- trend: 趋势
