# 模型架构文档

## MambaSwin-UNet-STA

### 模型参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| in_channels | 1 | 输入通道数 |
| out_channels | 1 | 输出通道数 |
| base_channels | 64 | 基础通道数 |
| time_steps | 6 | 输入时间步数 |

### Mamba模块参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| d_state | 16 | 状态维度 |
| d_conv | 3 | 卷积核大小 |
| expand | 2 | 扩展因子 |

### Swin Transformer参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| window_size | 7 | 窗口大小 |
| num_heads | 8 | 注意力头数 |

### 训练配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| epochs | 200 | 训练轮数 |
| batch_size | 16 | 批大小 |
| lr | 1e-4 | 学习率 |
| optimizer | AdamW | 优化器 |
| scheduler | CosineAnnealingLR | 学习率调度 |

## OpenClaw动态路由

### 专家模块

1. **AI专家**: MambaSwin-UNet-STA
2. **物理专家**: COTREC + 简化WRF
3. **统计专家**: XGBoost集成
4. **LLM专家**: 大模型推理

### 路由策略

根据天气形势动态分配权重:
- 强对流场景: AI专家权重提升
- 稳定性降水: 物理专家权重提升
- 默认均衡: 均匀分配

## 物理约束

### 损失函数

```python
total_loss = mse_loss 
           + 0.1 * non_negative_loss
           + 0.05 * mass_conservation_loss
           + 0.01 * smoothness_loss
           + 0.05 * terrain_loss
```

### 约束类型

1. **非负约束**: 降水值 ≥ 0
2. **质量守恒**: 连续方程检验
3. **平滑性**: 空间梯度约束
4. **地形强迫**: 地形抬升效应
