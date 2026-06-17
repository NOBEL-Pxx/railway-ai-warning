"""
物理约束模块
实现质量守恒、地形强迫等物理约束
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Optional, Tuple


class MassConservationConstraint(nn.Module):
    """
    质量守恒约束
    确保降水预报满足质量守恒定律
    """
    
    def __init__(self, dx: float = 1000.0, dy: float = 1000.0):
        """
        Args:
            dx: x方向网格间距 (米)
            dy: y方向网格间距 (米)
        """
        super().__init__()
        self.dx = dx
        self.dy = dy
        
    def forward(self, precipitation: torch.Tensor, 
                wind_u: Optional[torch.Tensor] = None,
                wind_v: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        计算质量守恒残差
        
        Args:
            precipitation: 降水场 (B, T, H, W)
            wind_u: u风场
            wind_v: v风场
            
        Returns:
            质量守恒残差
        """
        if wind_u is None or wind_v is None:
            # 如果没有风场，检查降水时空连续性
            return self._temporal_continuity(precipitation)
        
        # 连续方程: ∂ρ/∂t + ∇·(ρv) = 0
        # 简化为: ∂P/∂t + ∂(Pu)/∂x + ∂(Pv)/∂y ≈ 0
        
        # 时间导数
        dP_dt = precipitation[:, 1:] - precipitation[:, :-1]
        
        # 空间导数
        d_Pu_dx = (precipitation * wind_u)[:, :, :, 1:] - (precipitation * wind_u)[:, :, :, :-1]
        d_Pv_dy = (precipitation * wind_v)[:, :, 1:, :] - (precipitation * wind_v)[:, :, :-1, :]
        
        # 质量守恒残差
        residual = dP_dt + d_Pu_dx / self.dx + d_Pv_dy / self.dy
        
        return residual.abs().mean()
    
    def _temporal_continuity(self, precipitation: torch.Tensor) -> torch.Tensor:
        """时间连续性约束"""
        diff = precipitation[:, 1:] - precipitation[:, :-1]
        return diff.abs().mean()


class TerrainForcing(nn.Module):
    """
    地形强迫模块
    模拟地形对气流的抬升/阻挡效应
    """
    
    def __init__(self, dem: np.ndarray, resolution: float = 30.0):
        """
        Args:
            dem: DEM高程数据
            resolution: 空间分辨率 (米)
        """
        super().__init__()
        self.dem = torch.from_numpy(dem).float()
        self.resolution = resolution
        
        # 预计算地形因子
        self.slope = self._compute_slope(dem)
        self.aspect = self._compute_aspect(dem)
        
    def _compute_slope(self, dem: np.ndarray) -> np.ndarray:
        """计算坡度"""
        from scipy.ndimage import sobel
        dz_dx = sobel(dem, axis=1) / (8 * self.resolution)
        dz_dy = sobel(dem, axis=0) / (8 * self.resolution)
        slope = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
        return slope
    
    def _compute_aspect(self, dem: np.ndarray) -> np.ndarray:
        """计算坡向"""
        from scipy.ndimage import sobel
        dz_dx = sobel(dem, axis=1) / (8 * self.resolution)
        dz_dy = sobel(dem, axis=0) / (8 * self.resolution)
        aspect = np.arctan2(dz_dy, dz_dx)
        return aspect
    
    def forward(self, wind_u: torch.Tensor, wind_v: torch.Tensor) -> torch.Tensor:
        """
        计算地形强迫产生的垂直速度
        
        Args:
            wind_u: u风场 (m/s)
            wind_v: v风场 (m/s)
            
        Returns:
            地形强迫垂直速度 (m/s)
        """
        # 地形抬升: w = u * ∂h/∂x + v * ∂h/∂y
        slope_tensor = torch.from_numpy(self.slope).to(wind_u.device)
        aspect_tensor = torch.from_numpy(self.aspect).to(wind_u.device)
        
        # 坡度分量
        slope_x = slope_tensor * torch.cos(aspect_tensor)
        slope_y = slope_tensor * torch.sin(aspect_tensor)
        
        # 垂直速度
        w = wind_u * slope_x + wind_v * slope_y
        
        return w
    
    def compute_enhancement_factor(self, precipitation: torch.Tensor) -> torch.Tensor:
        """
        计算地形降水增强因子
        
        Args:
            precipitation: 原始降水场
            
        Returns:
            增强后的降水场
        """
        # 地形抬升增强降水
        slope_tensor = torch.from_numpy(self.slope).to(precipitation.device)
        
        # 增强因子 (简化模型)
        enhancement = 1.0 + slope_tensor * 2.0  # 坡度越大，增强越明显
        
        return precipitation * enhancement


class PhysicsConstraintLoss(nn.Module):
    """物理约束损失函数"""
    
    def __init__(self, dem: Optional[np.ndarray] = None):
        super().__init__()
        
        self.mass_conservation = MassConservationConstraint()
        
        if dem is not None:
            self.terrain_forcing = TerrainForcing(dem)
        else:
            self.terrain_forcing = None
            
    def forward(self, prediction: torch.Tensor, 
                target: torch.Tensor,
                wind_u: Optional[torch.Tensor] = None,
                wind_v: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, dict]:
        """
        计算物理约束损失
        
        Returns:
            (总损失, 损失分量字典)
        """
        losses = {}
        
        # 1. MSE损失
        losses['mse'] = F.mse_loss(prediction, target)
        
        # 2. 非负约束
        losses['non_negative'] = F.relu(-prediction).mean()
        
        # 3. 质量守恒
        losses['mass_conservation'] = self.mass_conservation(prediction, wind_u, wind_v)
        
        # 4. 平滑性
        losses['smoothness'] = self._smoothness_loss(prediction)
        
        # 5. 地形约束
        if self.terrain_forcing is not None:
            losses['terrain'] = self._terrain_consistency_loss(prediction)
        else:
            losses['terrain'] = torch.tensor(0.0)
        
        # 加权总损失
        total_loss = (
            losses['mse'] +
            0.1 * losses['non_negative'] +
            0.05 * losses['mass_conservation'] +
            0.01 * losses['smoothness'] +
            0.05 * losses['terrain']
        )
        
        return total_loss, losses
    
    def _smoothness_loss(self, x: torch.Tensor) -> torch.Tensor:
        """平滑性损失"""
        dx = x[:, :, :, 1:] - x[:, :, :, :-1]
        dy = x[:, :, 1:, :] - x[:, :, :-1, :]
        return (dx ** 2).mean() + (dy ** 2).mean()
    
    def _terrain_consistency_loss(self, precipitation: torch.Tensor) -> torch.Tensor:
        """地形一致性损失 - 地形高处降水应更连续"""
        if self.terrain_forcing is None:
            return torch.tensor(0.0, device=precipitation.device)
        
        # 获取地形坡度
        slope_tensor = torch.from_numpy(self.terrain_forcing.slope).to(precipitation.device)
        
        # 高坡度区域（>5度）的降水时空梯度应更平滑
        high_slope_mask = slope_tensor > 0.087  # 约5度
        
        if high_slope_mask.any():
            # 时间梯度
            if precipitation.dim() == 4 and precipitation.shape[1] > 1:
                temporal_grad = (precipitation[:, 1:] - precipitation[:, :-1]).abs()
                # 对高坡度区域施加更强的平滑约束
                high_slope_loss = (temporal_grad * high_slope_mask.unsqueeze(0).unsqueeze(0)).mean()
            else:
                high_slope_loss = torch.tensor(0.0, device=precipitation.device)
            
            # 空间梯度
            spatial_grad_x = (precipitation[:, :, :, 1:] - precipitation[:, :, :, :-1]).abs()
            spatial_grad_y = (precipitation[:, :, 1:, :] - precipitation[:, :, :-1, :]).abs()
            
            # 高坡度区域的空间连续性
            spatial_loss = (
                (spatial_grad_x * high_slope_mask[:, :-1].unsqueeze(0).unsqueeze(0)).mean() +
                (spatial_grad_y * high_slope_mask[:-1, :].unsqueeze(0).unsqueeze(0)).mean()
            ) / 2
            
            return high_slope_loss + 0.5 * spatial_loss
        
        return torch.tensor(0.0, device=precipitation.device)


class COTRECPhysics(nn.Module):
    """
    COTREC物理外推模型
    基于雷达回波的连续性追踪
    
    参考: COTREC (Continuity of Tracking Radar Echoes by Correlation)
    """
    
    def __init__(self, window_size: int = 15, max_velocity: float = 50.0):
        """
        Args:
            window_size: 相关系数计算的窗口大小
            max_velocity: 最大允许速度 (像素/帧)
        """
        super().__init__()
        self.window_size = window_size
        self.max_velocity = max_velocity
        self.padding = window_size // 2
    
    def compute_optical_flow(self, prev: torch.Tensor, 
                             curr: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        基于相关性的光流计算 (COTREC方法)
        
        Args:
            prev: 前一时刻雷达图 (B, H, W) 或 (B, C, H, W)
            curr: 当前时刻雷达图
            
        Returns:
            (u, v) 光流场
        """
        # 确保输入维度正确
        if prev.dim() == 4:
            prev = prev.squeeze(1)
            curr = curr.squeeze(1)
        
        B, H, W = prev.shape
        
        # 使用块匹配方法计算光流
        # 对每个位置，在搜索范围内找到最佳匹配
        u = torch.zeros(B, H, W, device=prev.device)
        v = torch.zeros(B, H, W, device=prev.device)
        
        # 简化实现：使用梯度法
        # 计算图像梯度
        Ix = (curr[:, :, 1:] - curr[:, :, :-1])  # x方向梯度
        Iy = (curr[:, 1:, :] - curr[:, :-1, :])  # y方向梯度
        It = curr - prev  # 时间梯度
        
        # Lucas-Kanade 方法
        # 在局部窗口内求解: [Ix, Iy] * [u, v]^T = -It
        
        # 创建可分离的高斯核用于加权
        kernel_size = 5
        sigma = 1.5
        
        # 计算 Ix^2, Iy^2, Ix*Iy 的局部和
        Ix_padded = F.pad(Ix, (0, 1, 0, 0), mode='replicate')  # 补齐到原始尺寸
        Iy_padded = F.pad(Iy, (0, 0, 0, 1), mode='replicate')
        
        # 使用平均池化近似局部求和
        Ix2 = F.avg_pool2d(Ix_padded.unsqueeze(1), kernel_size, stride=1, padding=kernel_size//2).squeeze(1)
        Iy2 = F.avg_pool2d(Iy_padded.unsqueeze(1), kernel_size, stride=1, padding=kernel_size//2).squeeze(1)
        IxIy = F.avg_pool2d((Ix_padded * Iy_padded).unsqueeze(1), kernel_size, stride=1, padding=kernel_size//2).squeeze(1)
        IxIt = F.avg_pool2d((Ix_padded * It).unsqueeze(1), kernel_size, stride=1, padding=kernel_size//2).squeeze(1)
        IyIt = F.avg_pool2d((Iy_padded * It).unsqueeze(1), kernel_size, stride=1, padding=kernel_size//2).squeeze(1)
        
        # 求解 2x2 线性系统
        det = Ix2 * Iy2 - IxIy * IxIy + 1e-8
        
        u = (Iy2 * (-IxIt) - IxIy * (-IyIt)) / det
        v = (Ix2 * (-IyIt) - IxIy * (-IxIt)) / det
        
        # 限制最大速度
        velocity_mag = torch.sqrt(u**2 + v**2)
        scale = torch.clamp(self.max_velocity / (velocity_mag + 1e-8), max=1.0)
        u = u * scale
        v = v * scale
        
        return u, v
    
    def extrapolate(self, radar: torch.Tensor, 
                    steps: int = 6,
                    decay: float = 0.95) -> torch.Tensor:
        """
        半拉格朗日外推预测
        
        Args:
            radar: 雷达时序数据 (B, T, H, W)
            steps: 外推步数
            decay: 衰减系数 (模拟降水消散)
            
        Returns:
            外推结果 (B, steps, H, W)
        """
        # 计算光流
        if radar.shape[1] >= 2:
            u, v = self.compute_optical_flow(radar[:, -2], radar[:, -1])
        else:
            # 只有一帧，无法计算光流
            u = torch.zeros(radar.shape[0], radar.shape[2], radar.shape[3], device=radar.device)
            v = torch.zeros_like(u)
        
        # 半拉格朗日外推
        predictions = []
        current = radar[:, -1]  # (B, H, W)
        
        # 创建网格
        B, H, W = current.shape
        grid_y, grid_x = torch.meshgrid(
            torch.arange(H, device=current.device, dtype=torch.float32),
            torch.arange(W, device=current.device, dtype=torch.float32),
            indexing='ij'
        )
        
        for step in range(steps):
            # 计算后向轨迹
            # 从目标点追溯到源点
            src_x = grid_x - u  # (H, W)
            src_y = grid_y - v  # (H, W)
            
            # 归一化到 [-1, 1]
            src_x_norm = 2.0 * src_x / (W - 1) - 1.0
            src_y_norm = 2.0 * src_y / (H - 1) - 1.0
            
            # 双线性插值
            grid_sample = torch.stack([src_x_norm, src_y_norm], dim=-1)  # (H, W, 2)
            grid_sample = grid_sample.unsqueeze(0).expand(B, -1, -1, -1)  # (B, H, W, 2)
            
            # 对每个batch进行插值
            current_unsq = current.unsqueeze(1)  # (B, 1, H, W)
            advected = F.grid_sample(
                current_unsq, grid_sample, 
                mode='bilinear', 
                padding_mode='zeros',
                align_corners=True
            ).squeeze(1)  # (B, H, W)
            
            # 应用衰减
            advected = advected * decay
            
            predictions.append(advected)
            current = advected
        
        return torch.stack(predictions, dim=1)  # (B, steps, H, W)
    
    def extrapolate_with_growth(self, radar: torch.Tensor,
                                 steps: int = 6,
                                 growth_rate: float = 0.02,
                                 max_intensity: float = 60.0) -> torch.Tensor:
        """
        带生消过程的外推预测
        
        Args:
            radar: 雷达时序数据 (B, T, H, W)
            steps: 外推步数
            growth_rate: 生消率
            max_intensity: 最大回波强度 (dBZ)
            
        Returns:
            外推结果 (B, steps, H, W)
        """
        # 基础外推
        base_prediction = self.extrapolate(radar, steps, decay=1.0)
        
        # 计算生消场 (基于时间趋势)
        if radar.shape[1] >= 2:
            trend = radar[:, -1] - radar[:, -2]  # (B, H, W)
            # 扩展到所有时间步
            trend = trend.unsqueeze(1).expand(-1, steps, -1, -1)  # (B, steps, H, W)
            
            # 应用生消
            time_weights = torch.arange(1, steps + 1, device=radar.device, dtype=torch.float32)
            time_weights = time_weights.view(1, steps, 1, 1)
            
            growth = trend * growth_rate * time_weights
            prediction = base_prediction + growth
        else:
            prediction = base_prediction
        
        # 限制范围
        prediction = torch.clamp(prediction, 0, max_intensity)
        
        return prediction


class SCSCNModel(nn.Module):
    """
    SCS-CN 水文模型
    用于计算地表径流和致灾风险推演
    
    参考: USDA SCS Curve Number Method
    """
    
    def __init__(self, cn_map: np.ndarray, dem: np.ndarray = None):
        """
        Args:
            cn_map: CN值分布图 (H, W), 范围 0-100
            dem: DEM高程数据 (H, W), 用于汇流计算
        """
        super().__init__()
        self.cn_map = torch.from_numpy(cn_map).float()
        self.dem = torch.from_numpy(dem).float() if dem is not None else None
        
        # 预计算潜在最大滞留量 S
        # S = 25400 / CN - 254 (mm)
        self._compute_s()
        
        if dem is not None:
            self._compute_flow_direction()
    
    def _compute_s(self):
        """计算潜在最大滞留量 S"""
        cn = torch.clamp(self.cn_map, 1, 100)  # 避免除零
        self.s_map = 25400.0 / cn - 254.0  # mm
    
    def _compute_flow_direction(self):
        """计算流向 (D8算法)"""
        dem = self.dem.numpy()
        H, W = dem.shape
        
        # 8方向编码: E, SE, S, SW, W, NW, N, NE
        self.flow_dir = np.zeros((H, W), dtype=np.int8)
        
        # 计算每个像素的流向
        for i in range(1, H - 1):
            for j in range(1, W - 1):
                # 8邻域高程差
                neighbors = [
                    dem[i, j+1] - dem[i, j],    # E
                    dem[i+1, j+1] - dem[i, j],  # SE
                    dem[i+1, j] - dem[i, j],    # S
                    dem[i+1, j-1] - dem[i, j],  # SW
                    dem[i, j-1] - dem[i, j],    # W
                    dem[i-1, j-1] - dem[i, j],  # NW
                    dem[i-1, j] - dem[i, j],    # N
                    dem[i-1, j+1] - dem[i, j],  # NE
                ]
                
                # 找最大下坡方向
                max_drop = max(neighbors)
                if max_drop > 0:
                    self.flow_dir[i, j] = neighbors.index(max_drop)
                else:
                    self.flow_dir[i, j] = -1  # 无出流
        
        self.flow_dir = torch.from_numpy(self.flow_dir)
    
    def compute_runoff(self, precipitation: torch.Tensor, 
                       antecedent_moisture: str = 'normal') -> torch.Tensor:
        """
        计算地表径流
        
        Args:
            precipitation: 降水量 (mm), shape (B, T, H, W) 或 (B, H, W)
            antecedent_moisture: 前期土壤湿润条件 ('dry', 'normal', 'wet')
            
        Returns:
            径流量 (mm)
        """
        # 根据前期条件调整CN值
        cn_adjustment = {
            'dry': lambda cn: cn / (2.281 - 0.01281 * cn),
            'normal': lambda cn: cn,
            'wet': lambda cn: cn / (0.427 + 0.00573 * cn)
        }
        
        cn = self.cn_map.to(precipitation.device)
        cn_adjusted = cn_adjustment[antecedent_moisture](cn)
        cn_adjusted = torch.clamp(cn_adjusted, 1, 100)
        
        # 重新计算 S
        s = 25400.0 / cn_adjusted - 254.0
        
        # 初始抽损 Ia = 0.2 * S
        ia = 0.2 * s
        
        # 径流计算: Q = (P - Ia)^2 / (P - Ia + S)
        # 当 P > Ia 时才有径流
        if precipitation.dim() == 4:
            # (B, T, H, W) -> 对时间维度累加
            p_cumsum = precipitation.cumsum(dim=1)
        else:
            p_cumsum = precipitation
        
        runoff = torch.zeros_like(p_cumsum)
        excess = p_cumsum - ia  # (..., H, W)
        
        # 只在 P > Ia 时计算径流
        mask = excess > 0
        runoff = torch.where(
            mask,
            excess ** 2 / (excess + s + 1e-8),
            torch.zeros_like(p_cumsum)
        )
        
        return runoff
    
    def compute_peak_flow(self, runoff: torch.Tensor, 
                          area: float = 1.0,  # km^2
                          tc: float = 1.0) -> torch.Tensor:  # 汇流时间 (小时)
        """
        计算洪峰流量
        
        Args:
            runoff: 径流量 (mm)
            area: 流域面积 (km^2)
            tc: 汇流时间 (小时)
            
        Returns:
            洪峰流量 (m^3/s)
        """
        # Rational公式: Qp = 0.278 * C * I * A
        # 简化: Qp = runoff * area / (3.6 * tc)
        
        # 将mm转换为m
        runoff_m = runoff / 1000.0
        
        # 计算流量
        peak_flow = runoff_m * area * 1e6 / (tc * 3600)  # m^3/s
        
        return peak_flow
    
    def compute_risk_level(self, runoff: torch.Tensor,
                           thresholds: dict = None) -> torch.Tensor:
        """
        计算致灾风险等级
        
        Args:
            runoff: 径流量 (mm)
            thresholds: 风险阈值配置
            
        Returns:
            风险等级 (0: 无风险, 1: 低风险, 2: 中风险, 3: 高风险, 4: 极高风险)
        """
        if thresholds is None:
            thresholds = {
                'low': 10.0,      # mm
                'medium': 25.0,
                'high': 50.0,
                'extreme': 100.0
            }
        
        risk = torch.zeros_like(runoff, dtype=torch.long)
        
        risk = torch.where(runoff >= thresholds['extreme'], torch.tensor(4), risk)
        risk = torch.where((runoff >= thresholds['high']) & (runoff < thresholds['extreme']), torch.tensor(3), risk)
        risk = torch.where((runoff >= thresholds['medium']) & (runoff < thresholds['high']), torch.tensor(2), risk)
        risk = torch.where((runoff >= thresholds['low']) & (runoff < thresholds['medium']), torch.tensor(1), risk)
        
        return risk
    
    def forward(self, precipitation: torch.Tensor,
                antecedent_moisture: str = 'normal') -> dict:
        """
        完整的水文模拟
        
        Args:
            precipitation: 降水量 (mm)
            antecedent_moisture: 前期土壤湿润条件
            
        Returns:
            包含径流、洪峰、风险等级的字典
        """
        runoff = self.compute_runoff(precipitation, antecedent_moisture)
        risk = self.compute_risk_level(runoff)
        
        return {
            'runoff': runoff,
            'risk_level': risk,
            's_value': self.s_map.to(precipitation.device)
        }


class RiskInferenceEngine(nn.Module):
    """
    致灾风险推演引擎
    整合降水预报与水文模型
    """
    
    def __init__(self, cn_map: np.ndarray, dem: np.ndarray = None,
                 railway_lines: np.ndarray = None):
        """
        Args:
            cn_map: CN值分布图
            dem: DEM数据
            railway_lines: 铁路线位置掩码 (H, W), 1表示铁路
        """
        super().__init__()
        self.hydrology = SCSCNModel(cn_map, dem)
        self.railway_mask = torch.from_numpy(railway_lines).float() if railway_lines is not None else None
        
        # 铁路灾害阈值 (根据历史数据标定)
        self.disaster_thresholds = {
            'slope_failure': 50.0,    # 边坡失稳阈值 (mm)
            'subgrade_erosion': 30.0,  # 路基冲刷阈值 (mm)
            'waterlogging': 20.0       # 积水阈值 (mm)
        }
    
    def forward(self, precipitation_forecast: torch.Tensor,
                terrain_features: dict = None) -> dict:
        """
        执行风险推演
        
        Args:
            precipitation_forecast: 降水预报 (B, T, H, W), 单位mm
            terrain_features: 地形特征 (坡度、坡向等)
            
        Returns:
            风险推演结果
        """
        # 水文模拟
        hydro_result = self.hydrology(precipitation_forecast)
        
        runoff = hydro_result['runoff']
        risk_level = hydro_result['risk_level']
        
        # 铁路沿线风险提取
        if self.railway_mask is not None:
            railway_mask = self.railway_mask.to(precipitation_forecast.device)
            railway_risk = self._extract_railway_risk(risk_level, railway_mask)
        else:
            railway_risk = None
        
        # 特定灾害风险分析
        disaster_risks = self._analyze_disaster_risks(
            precipitation_forecast, runoff, terrain_features
        )
        
        return {
            'runoff': runoff,
            'risk_level': risk_level,
            'railway_risk': railway_risk,
            'disaster_risks': disaster_risks,
            'max_risk_time': self._find_peak_risk_time(risk_level)
        }
    
    def _extract_railway_risk(self, risk_level: torch.Tensor, 
                               railway_mask: torch.Tensor) -> torch.Tensor:
        """提取铁路沿线风险"""
        # 铁路位置的风险值
        if risk_level.dim() == 4:
            # (B, T, H, W)
            railway_risk = risk_level * railway_mask.unsqueeze(0).unsqueeze(0)
        else:
            railway_risk = risk_level * railway_mask
        
        return railway_risk
    
    def _analyze_disaster_risks(self, precipitation: torch.Tensor,
                                 runoff: torch.Tensor,
                                 terrain_features: dict = None) -> dict:
        """分析特定灾害风险"""
        risks = {}
        
        # 边坡失稳风险
        if terrain_features and 'slope' in terrain_features:
            slope = terrain_features['slope']
            # 坡度越大，失稳风险越高
            slope_factor = torch.sigmoid(slope * 10)  # 归一化
            risks['slope_failure'] = (runoff * slope_factor) > self.disaster_thresholds['slope_failure']
        else:
            risks['slope_failure'] = runoff > self.disaster_thresholds['slope_failure']
        
        # 路基冲刷风险
        risks['subgrade_erosion'] = runoff > self.disaster_thresholds['subgrade_erosion']
        
        # 积水风险
        risks['waterlogging'] = runoff > self.disaster_thresholds['waterlogging']
        
        return risks
    
    def _find_peak_risk_time(self, risk_level: torch.Tensor) -> torch.Tensor:
        """找到风险峰值时刻"""
        if risk_level.dim() == 4:
            # (B, T, H, W) -> 对空间维度取最大风险
            max_risk = risk_level.amax(dim=(2, 3))  # (B, T)
            peak_time = max_risk.argmax(dim=1)  # (B,)
            return peak_time
        return torch.tensor(0)


if __name__ == "__main__":
    # 测试物理约束
    constraint = PhysicsConstraintLoss()
    
    prediction = torch.randn(2, 6, 64, 64)
    target = torch.randn(2, 6, 64, 64)
    
    loss, losses = constraint(prediction, target)
    
    print(f"Total loss: {loss.item():.4f}")
    for name, value in losses.items():
        print(f"  {name}: {value.item():.4f}")
    
    # 测试COTREC
    print("\n测试COTREC外推:")
    cotrec = COTRECPhysics()
    radar = torch.randn(2, 3, 64, 64)
    forecast = cotrec.extrapolate(radar, steps=6)
    print(f"  输入形状: {radar.shape}")
    print(f"  预报形状: {forecast.shape}")
    
    # 测试SCS-CN
    print("\n测试SCS-CN水文模型:")
    cn_map = np.random.uniform(60, 90, (64, 64))
    scs = SCSCNModel(cn_map)
    precip = torch.rand(2, 6, 64, 64) * 50  # 0-50mm
    result = scs(precip)
    print(f"  径流形状: {result['runoff'].shape}")
    print(f"  风险等级范围: {result['risk_level'].min()}-{result['risk_level'].max()}")
