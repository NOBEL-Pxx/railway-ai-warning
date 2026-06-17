"""
测试脚本：用随机数据验证模型代码正确性
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# 导入模型
from src.models.mamba_swin_unet import MambaSwinUNetSTA
from src.models.router import LoongClawFramework, WeatherContext


class RandomDataset(Dataset):
    """随机数据集"""
    
    def __init__(self, num_samples=100, time_steps=6, channels=1, height=64, width=64):
        self.num_samples = num_samples
        self.time_steps = time_steps
        self.channels = channels
        self.height = height
        self.width = width
        
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        # 输入: (T, C, H, W)
        x = torch.randn(self.time_steps, self.channels, self.height, self.width)
        # 目标: (H, W)
        y = torch.randn(self.height, self.width)
        return x, y


def test_mamba_swin_unet():
    """测试 MambaSwin-UNet-STA 模型"""
    print("=" * 60)
    print("测试 MambaSwin-UNet-STA 模型")
    print("=" * 60)
    
    # 创建模型
    model = MambaSwinUNetSTA(
        in_channels=1,
        out_channels=1,
        base_channels=32,  # 使用较小的通道数加快测试
        time_steps=6
    )
    
    # 统计参数量
    num_params = sum(p.numel() for p in model.parameters())
    print(f"\n模型参数量: {num_params:,}")
    
    # 创建随机输入
    batch_size = 2
    time_steps = 6
    x = torch.randn(batch_size, time_steps, 1, 64, 64)
    
    print(f"\n输入形状: {x.shape}")
    
    # 前向传播
    model.eval()
    with torch.no_grad():
        output = model(x)
    
    print(f"输出形状: {output.shape}")
    
    # 检查输出形状 (B, C, H, W)
    assert output.shape == (batch_size, 1, 64, 64), f"输出形状错误: {output.shape}"
    
    print("\n✓ MambaSwin-UNet-STA 模型测试通过!")
    return model


def test_loongclaw_framework():
    """测试 LoongClaw 动态路由框架"""
    print("\n" + "=" * 60)
    print("测试 LoongClaw 动态路由框架")
    print("=" * 60)
    
    # 创建基础模型
    ai_model = MambaSwinUNetSTA(
        in_channels=1,
        out_channels=1,
        base_channels=32,
        time_steps=6
    )
    
    # 创建 LoongClaw 框架
    framework = LoongClawFramework(ai_model)
    
    # 统计参数量
    num_params = sum(p.numel() for p in framework.parameters())
    print(f"\n框架参数量: {num_params:,}")
    
    # 创建随机输入
    batch_size = 2
    x = torch.randn(batch_size, 6, 1, 64, 64)
    
    # 创建天气形势上下文
    context = WeatherContext(
        convection_intensity=0.8,
        stability_index=0.3,
        system_speed=30.0,
        precipitation_intensity=50.0,
        terrain_complexity=0.7
    )
    
    print(f"\n天气形势:")
    print(f"  对流强度: {context.convection_intensity}")
    print(f"  稳定度指数: {context.stability_index}")
    print(f"  系统移动速度: {context.system_speed} m/s")
    print(f"  降水强度: {context.precipitation_intensity} mm/h")
    print(f"  地形复杂度: {context.terrain_complexity}")
    
    # 前向传播
    framework.eval()
    with torch.no_grad():
        output = framework(x, context)
    
    print(f"\n输出:")
    print(f"  预测形状: {output['prediction'].shape}")
    print(f"  专家权重: {output['weights'].tolist()}")
    print(f"  LLM分析: {output['llm_analysis']}")
    
    # 检查输出
    assert 'prediction' in output
    assert 'weights' in output
    assert output['prediction'].shape == (batch_size, 1, 64, 64)
    
    print("\n✓ LoongClaw 动态路由框架测试通过!")


def test_training_step():
    """测试训练步骤"""
    print("\n" + "=" * 60)
    print("测试训练步骤")
    print("=" * 60)
    
    # 创建模型
    model = MambaSwinUNetSTA(
        in_channels=1,
        out_channels=1,
        base_channels=32,
        time_steps=6
    )
    
    # 创建数据加载器
    dataset = RandomDataset(num_samples=10, height=64, width=64)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    
    # 创建优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    
    # 损失函数
    criterion = nn.MSELoss()
    
    # 训练一个batch
    model.train()
    for batch_idx, (x, y) in enumerate(dataloader):
        print(f"\nBatch {batch_idx + 1}:")
        print(f"  输入形状: {x.shape}")
        print(f"  目标形状: {y.shape}")
        
        # 前向传播
        optimizer.zero_grad()
        output = model(x)
        loss = criterion(output, y)
        
        print(f"  损失: {loss.item():.6f}")
        
        # 反向传播
        loss.backward()
        optimizer.step()
        
        # 只测试一个batch
        break
    
    print("\n✓ 训练步骤测试通过!")


def test_different_input_sizes():
    """测试不同输入尺寸"""
    print("\n" + "=" * 60)
    print("测试不同输入尺寸")
    print("=" * 60)
    
    model = MambaSwinUNetSTA(
        in_channels=1,
        out_channels=1,
        base_channels=32,
        time_steps=6
    )
    
    model.eval()
    
    # 测试不同尺寸（需要能被窗口大小8整除，且足够大）
    sizes = [(64, 64), (128, 128)]
    
    for h, w in sizes:
        x = torch.randn(1, 6, 1, h, w)
        with torch.no_grad():
            output = model(x)
        print(f"  输入: {x.shape} → 输出: {output.shape}")
        assert output.shape == (1, 1, h, w), f"尺寸不匹配: {output.shape}"
    
    print("\n✓ 不同输入尺寸测试通过!")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("LoongClaw 模型代码验证测试")
    print("=" * 60 + "\n")
    
    try:
        # 测试基础模型
        model = test_mamba_swin_unet()
        
        # 测试动态路由框架
        test_loongclaw_framework()
        
        # 测试训练步骤
        test_training_step()
        
        # 测试不同输入尺寸
        test_different_input_sizes()
        
        print("\n" + "=" * 60)
        print("All tests passed!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
