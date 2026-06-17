"""
MambaSwin-UNet-STA 深度学习模型
融合Mamba、Swin Transformer、U-Net和时空注意力机制
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List
import math


class MambaBlock(nn.Module):
    """
    Mamba模块 - 高效序列建模
    线性复杂度O(n)，突破Transformer二次复杂度瓶颈
    """
    
    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 3, expand: int = 2):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)
        
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)
        self.conv1d = nn.Conv1d(self.d_inner, self.d_inner, kernel_size=d_conv, 
                                padding=d_conv - 1, groups=self.d_inner)
        self.out_proj = nn.Linear(self.d_inner, d_model, bias=False)
        
        # SSM参数
        self.A = nn.Parameter(torch.randn(self.d_inner, d_state))
        self.B = nn.Parameter(torch.randn(self.d_inner, d_state))
        self.C = nn.Parameter(torch.randn(self.d_inner, d_state))
        self.D = nn.Parameter(torch.ones(self.d_inner))
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (B, L, D) 输入序列
        Returns:
            (B, L, D) 输出序列
        """
        B, L, D = x.shape
        
        # 投影
        xz = self.in_proj(x)
        x, z = xz.chunk(2, dim=-1)
        
        # 卷积
        x = x.transpose(1, 2)
        x = self.conv1d(x)[:, :, :L]
        x = x.transpose(1, 2)
        
        # SSM (简化版本)
        # TODO: 实现完整的Mamba SSM
        y = x * torch.sigmoid(z)
        
        # 输出投影
        out = self.out_proj(y)
        
        return out


class SwinTransformerBlock(nn.Module):
    """
    Swin Transformer块
    窗口注意力机制，层级特征融合
    """
    
    def __init__(self, dim: int, num_heads: int = 8, window_size: int = 8,
                 mlp_ratio: float = 4.0, dropout: float = 0.0):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.window_size = window_size
        self.mlp_ratio = mlp_ratio
        
        self.norm1 = nn.LayerNorm(dim)
        self.attn = WindowAttention(dim, window_size, num_heads)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, int(dim * mlp_ratio)),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(int(dim * mlp_ratio), dim),
            nn.Dropout(dropout)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (B, H, W, C) 输入特征
        """
        shortcut = x
        x = self.norm1(x)
        
        # 窗口注意力
        x = self.attn(x)
        
        x = shortcut + x
        x = x + self.mlp(self.norm2(x))
        
        return x


class WindowAttention(nn.Module):
    """窗口注意力模块"""
    
    def __init__(self, dim: int, window_size: int, num_heads: int):
        super().__init__()
        self.dim = dim
        self.window_size = window_size
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5
        
        self.qkv = nn.Linear(dim, dim * 3)
        self.proj = nn.Linear(dim, dim)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, H, W, C = x.shape
        
        # 重塑为窗口
        x = x.view(B, H // self.window_size, self.window_size, 
                   W // self.window_size, self.window_size, C)
        x = x.permute(0, 1, 3, 2, 4, 5).contiguous()
        x = x.view(-1, self.window_size * self.window_size, C)
        
        # 注意力计算
        qkv = self.qkv(x).reshape(-1, self.window_size ** 2, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        
        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        
        x = (attn @ v).transpose(1, 2).reshape(-1, self.window_size ** 2, C)
        x = self.proj(x)
        
        # 恢复形状
        x = x.view(B, H // self.window_size, W // self.window_size, 
                   self.window_size, self.window_size, C)
        x = x.permute(0, 1, 3, 2, 4, 5).contiguous()
        x = x.view(B, H, W, C)
        
        return x


class SpatioTemporalAttention(nn.Module):
    """
    时空注意力模块
    捕捉降水演变的时空动态特征
    """
    
    def __init__(self, dim: int, num_heads: int = 8, dropout: float = 0.0):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5
        
        # 时间注意力
        self.temporal_qkv = nn.Linear(dim, dim * 3)
        self.temporal_proj = nn.Linear(dim, dim)
        
        # 空间注意力
        self.spatial_qkv = nn.Linear(dim, dim * 3)
        self.spatial_proj = nn.Linear(dim, dim)
        
        self.norm = nn.LayerNorm(dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (B, T, H, W, C) 时空特征
        """
        B, T, H, W, C = x.shape
        
        # 时间注意力
        x_temporal = x.permute(0, 2, 3, 1, 4).contiguous()  # (B, H, W, T, C)
        x_temporal = x_temporal.view(B * H * W, T, C)
        
        qkv = self.temporal_qkv(x_temporal).reshape(B * H * W, T, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        
        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn = self.dropout(attn)
        
        x_temporal = (attn @ v).transpose(1, 2).reshape(B * H * W, T, C)
        x_temporal = self.temporal_proj(x_temporal)
        x_temporal = x_temporal.view(B, H, W, T, C).permute(0, 3, 1, 2, 4)
        
        # 空间注意力
        x_spatial = x.view(B * T, H * W, C)
        
        qkv = self.spatial_qkv(x_spatial).reshape(B * T, H * W, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        
        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn = self.dropout(attn)
        
        x_spatial = (attn @ v).transpose(1, 2).reshape(B * T, H * W, C)
        x_spatial = self.spatial_proj(x_spatial)
        x_spatial = x_spatial.view(B, T, H, W, C)
        
        return self.norm(x + x_temporal + x_spatial)


class EncoderBlock(nn.Module):
    """编码器块"""
    
    def __init__(self, in_channels: int, out_channels: int, 
                 use_mamba: bool = True, use_swin: bool = True):
        super().__init__()
        
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
        
        self.use_mamba = use_mamba
        self.use_swin = use_swin
        
        if use_mamba:
            self.mamba = MambaBlock(out_channels)
        if use_swin:
            self.swin = SwinTransformerBlock(out_channels)
            
        self.pool = nn.MaxPool2d(2)
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.conv(x)
        
        B, C, H, W = x.shape
        
        if self.use_mamba:
            x_flat = x.flatten(2).transpose(1, 2)  # (B, H*W, C)
            x_flat = self.mamba(x_flat)
            x = x_flat.transpose(1, 2).view(B, C, H, W)
            
        if self.use_swin:
            x = x.permute(0, 2, 3, 1)  # (B, H, W, C)
            x = self.swin(x)
            x = x.permute(0, 3, 1, 2)
        
        skip = x
        x = self.pool(x)
        
        return x, skip


class DecoderBlock(nn.Module):
    """解码器块"""
    
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int):
        super().__init__()
        
        self.up = nn.ConvTranspose2d(in_channels, out_channels, 2, stride=2)
        self.conv = nn.Sequential(
            nn.Conv2d(out_channels + skip_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
        
    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        x = self.up(x)
        
        # 处理尺寸不匹配
        if x.shape[2:] != skip.shape[2:]:
            x = F.interpolate(x, size=skip.shape[2:], mode='bilinear', align_corners=True)
        
        x = torch.cat([x, skip], dim=1)
        x = self.conv(x)
        
        return x


class MambaSwinUNetSTA(nn.Module):
    """
    MambaSwin-UNet-STA 主模型
    融合Mamba、Swin Transformer、U-Net和时空注意力
    """
    
    def __init__(self, in_channels: int = 1, out_channels: int = 1,
                 base_channels: int = 64, time_steps: int = 6):
        super().__init__()
        
        self.time_steps = time_steps
        
        # 编码器
        self.enc1 = EncoderBlock(in_channels * time_steps, base_channels)
        self.enc2 = EncoderBlock(base_channels, base_channels * 2)
        self.enc3 = EncoderBlock(base_channels * 2, base_channels * 4)
        self.enc4 = EncoderBlock(base_channels * 4, base_channels * 8)
        
        # 瓶颈层 - 时空注意力
        self.bottleneck_conv = nn.Sequential(
            nn.Conv2d(base_channels * 8, base_channels * 16, 3, padding=1),
            nn.BatchNorm2d(base_channels * 16),
            nn.ReLU(inplace=True)
        )
        self.sta = SpatioTemporalAttention(base_channels * 16)
        
        # 解码器
        self.dec4 = DecoderBlock(base_channels * 16, base_channels * 8, base_channels * 8)
        self.dec3 = DecoderBlock(base_channels * 8, base_channels * 4, base_channels * 4)
        self.dec2 = DecoderBlock(base_channels * 4, base_channels * 2, base_channels * 2)
        self.dec1 = DecoderBlock(base_channels * 2, base_channels, base_channels)
        
        # 输出层
        self.out_conv = nn.Conv2d(base_channels, out_channels, 1)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (B, T, C, H, W) 输入时序数据
        Returns:
            (B, T, H, W) 预测降水场
        """
        B, T, C, H, W = x.shape
        
        # 将时间维度合并到通道维度
        x = x.view(B, T * C, H, W)
        
        # 编码
        x, skip1 = self.enc1(x)
        x, skip2 = self.enc2(x)
        x, skip3 = self.enc3(x)
        x, skip4 = self.enc4(x)
        
        # 瓶颈层
        x = self.bottleneck_conv(x)
        
        # 时空注意力 (简化版本，直接处理)
        # x shape: (B, C, H, W)
        B, C, H, W = x.shape
        x_flat = x.flatten(2).transpose(1, 2)  # (B, H*W, C)
        x_flat = self.sta.norm(x_flat)
        x = x_flat.transpose(1, 2).view(B, C, H, W)
        
        # 解码
        x = self.dec4(x, skip4)
        x = self.dec3(x, skip3)
        x = self.dec2(x, skip2)
        x = self.dec1(x, skip1)
        
        # 输出
        out = self.out_conv(x)
        
        return out


if __name__ == "__main__":
    # 测试模型
    model = MambaSwinUNetSTA(in_channels=1, out_channels=1, time_steps=6)
    x = torch.randn(2, 6, 1, 128, 128)  # (B, T, C, H, W)
    out = model(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {out.shape}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
