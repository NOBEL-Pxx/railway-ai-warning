# 🐉 LoongClaw — 气象AI科研助手框架

<div align="center">

**面向铁路短临降水智能预测的专属科研助手**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=flat&logo=pytorch)](https://pytorch.org/)
[![License](https://img.shields.io/badge/许可证-MIT-green?style=flat)](LICENSE)
[![Project](https://img.shields.io/badge/项目-大学生创新训练计划-165DFF?style=flat)](https://github.com/NOBEL-Pxx)
[![Period](https://img.shields.io/badge/执行周期-2026.04--2027.04-orange?style=flat)]()

</div>

---

## 📖 项目简介

**LoongClaw（龙爪）** 是服务于「气候暖湿化背景下铁路沿线小流域短临降水智能预测与致灾风险推演」项目的**统一品牌**与核心科研框架。它将 AI 大模型辅助、数据处理、模型训练、风险推演等科研流程整合为统一的命令行 + API 接口。

> 🎯 中国龙，气象魂 — 用 AI 守护铁路大动脉

---

## 🏗️ 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    LoongClaw 🐉                             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          🧠 科研助手层 (Assistant Layer)               │ │
│  │  Agent · Dialog · Memory · Skills · Workflow          │ │
│  │  任务管理 · 技能调度 · 记忆系统 · 对话交互              │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          📦 代码项目层 (Code Project Layer)            │ │
│  │  src/data · src/models · src/training · src/utils     │ │
│  │  数据处理 · 模型训练 · 风险推演                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          🏛️ 模型架构层 (Architecture Layer)           │ │
│  │  LoongClaw 动态路由混合智能框架                        │ │
│  │  AI专家 + 物理专家 + 气象专家 + 铁路专家               │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 四大专家协同

| 专家 | 核心模型 | 专长 |
|------|----------|------|
| 🤖 **AI专家** | MambaSwin-UNet-STA | 端到端降水预报、时空特征提取 |
| 🔬 **物理专家** | COTREC + WRF | 数值模式、物理约束推理 |
| 🌤️ **气象专家** | FY-4A + 多普勒雷达 | 多源数据融合、卫星反演 |
| 🚄 **铁路专家** | 致灾知识图谱 | 脆弱性曲线、风险评估 |

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/NOBEL-Pxx/loongclaw.git
cd loongclaw
pip install -r requirements.txt
```

### 使用

```python
from loongclaw import Dragon

# 初始化
dragon = Dragon()

# 查看项目状态
print(dragon.status())

# 查看今日任务
print(dragon.today())

# 对话式交互
dragon.chat("今天该做什么？")
dragon.chat("帮我检查数据质量")

# 执行技能
dragon.run("train-model", epochs=100, batch_size=32)

# 记录科研进展
dragon.remember("完成MambaSwin-UNet-STA架构搭建，TS评分提升至0.82")
dragon.remember("发现了雷达盲区数据的问题，决定用GAN插值", 
                entry_type="lesson", importance=4)

# 检索记忆
results = dragon.recall("雷达数据处理")

# 运行工作流
dragon.run_workflow("training_pipeline")

# 每日总结
print(dragon.daily_summary())
```

### CLI 模式

```bash
# 交互模式
python __init__.py

# 直接执行命令
python __init__.py --cmd "今天该做什么？"
```

### 直接使用 ML 模块

```bash
# 模型训练
python src/training/train.py --config configs/model.yaml

# 下载 ERA5 数据
python scripts/download_era5.py --start-year 2019 --end-year 2024

# 运行测试
python tests/test_model.py
```

---

## 📁 项目结构

```
LoongClaw/
├── __init__.py                    # 主入口（Dragon类 + CLI）
├── requirements.txt               # 依赖清单
│
├── core/                          # 核心引擎
│   ├── agent.py                   # 任务规划引擎（5阶段智能调度）
│   ├── dialog.py                  # 对话管理器
│   ├── memory.py                  # 记忆系统（短期/长期/检索）
│   ├── skills.py                  # 技能管理器
│   └── workflow.py                # 工作流引擎
│
├── configs/
│   ├── project.yaml               # 项目阶段配置
│   └── model.yaml                 # 模型/训练/数据配置
│
├── src/                           # 核心代码
│   ├── data/                      # 数据处理模块
│   │   ├── preprocess.py          # 数据预处理与质量控制
│   │   ├── features.py            # 特征工程（地形、雷达、时序）
│   │   └── interpolate.py         # 缺失值插补算法
│   ├── models/                    # 模型模块
│   │   ├── mamba_swin_unet.py     # MambaSwin-UNet-STA 主模型
│   │   ├── router.py              # LoongClaw 动态路由框架
│   │   └── physics.py             # 物理约束与水文模型（SCS-CN）
│   ├── training/
│   │   └── train.py               # PyTorch Lightning 训练脚本
│   └── utils/
│       ├── common.py              # 通用工具函数
│       ├── losses.py              # 损失函数（加权MSE/Focal/SSIM）
│       └── metrics.py             # 评估指标（TS/POD/FAR/CSI/ETS）
│
├── scripts/                       # 数据下载脚本
│   ├── download_era5.py           # ERA5 数据下载
│   └── download_dem.py            # DEM 数据处理
│
├── tests/                         # 测试
│   ├── test_model.py              # 模型测试
│   └── test_models.py             # 模型单元测试
│
├── skills/                        # 项目专属技能
│   ├── data/                      # 数据相关
│   ├── models/                    # 模型相关
│   └── paper/                     # 论文相关
│
├── workflows/                     # 预定义工作流
├── knowledge/                     # 项目知识库
│   ├── data/data_dict.md          # 数据字典
│   ├── models/architecture.md     # 模型架构文档
│   ├── project/plan.md            # 项目计划书
│   └── project/roadmap.md         # 技术路线图
├── docs/                          # 技术文档
│   ├── technical_proposal.md      # 技术方案
│   └── autodl_guide.md            # AutoDL 使用指南
│
├── data/                          # 数据目录
│   ├── raw/                       # 原始数据
│   ├── processed/                 # 处理后数据
│   └── external/                  # 外部数据（ERA5/DEM）
├── notebooks/                     # Jupyter notebooks
├── memory/                        # 记忆存储
├── logs/                          # 日志
└── README.md
```

---

## 🗓️ 项目阶段规划

| 阶段 | 时间 | 核心任务 |
|------|------|----------|
| 📊 数据治理 | 2026.04 - 2026.05 | 雨量数据脱敏清洗、缺失值插补、地形特征计算、基线验证 |
| 🧪 模型训练 | 2026.05 - 2026.08 | MambaSwin-UNet-STA搭建、动态路由开发、超参调优、消融实验 |
| 🔗 系统集成 | 2026.08 - 2026.11 | SCS-CN水文模型集成、风险推演插件、端到端流程测试 |
| ✅ 验证评估 | 2026.12 - 2027.01 | 典型暴雨个例验证、铁路局实地调研、可用性评估 |
| 📝 结题验收 | 2027.02 - 2027.04 | 论文撰写、代码开源、答辩准备 |

---

## ⚙️ 配置示例

```yaml
# configs/model.yaml
model:
  name: "MambaSwin-UNet-STA"
  in_channels: 1
  out_channels: 1
  base_channels: 64
  time_steps: 6
  forecast_steps: 6
  use_loongclaw: true

training:
  epochs: 200
  batch_size: 16
  lr: 0.0001
  accelerator: "auto"
  devices: 1
  early_stopping_patience: 20
  checkpoint_dir: "checkpoints"

data:
  train_path: "data/processed/train"
  val_path: "data/processed/val"
  test_path: "data/processed/test"
```

---

## 🔧 核心依赖

| 类别 | 库 | 用途 |
|------|-----|------|
| 深度学习 | PyTorch 2.0+, PyTorch Lightning | 模型训练框架 |
| 数据处理 | NumPy, Pandas, xarray, netCDF4 | 气象数据IO与处理 |
| 气象专业 | MetPy, CDSAPI | 气象计算、ERA5下载 |
| 地理空间 | rasterio, geopandas, shapely, pyproj | DEM处理与GIS分析 |
| 可视化 | Matplotlib, Seaborn, Cartopy | 气象图表与地图投影 |
| 框架 | PyYAML, OmegaConf | 配置管理 |

---

## 👥 团队

| 角色 | 信息 |
|------|------|
| **创建者** | 彭小溪 |
| **所属学校** | 兰州大学 |
| **指导老师** | 胡淑娟 教授 |
| **项目** | 大学生创新训练计划 |
| **执行周期** | 2026年4月 - 2027年4月 |

---

## 📄 许可证

MIT License © 2026 NOBEL-Pxx
