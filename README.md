# 🛤️ 智驭苍穹 · 守路安澜 — Railway AI Warning System

<div align="center">

**Air-Space-Ground Multi-Modal Short-Imminent Disaster Risk Digital Twin Warning System**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=flat&logo=pytorch)](https://pytorch.org/)
[![WeChat](https://img.shields.io/badge/Platform-微信小程序-07C160?style=flat&logo=wechat)](https://developers.weixin.qq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Team](https://img.shields.io/badge/Team-兰州大学-165DFF?style=flat)](https://www.lzu.edu.cn/)

[English](#-overview) | [中文](#-项目概述)

</div>

---

## 📖 Overview

**"智驭苍穹 · 守路安澜"** (Wisdom Commands the Skies · Safeguarding the Rails) is a comprehensive AI-powered railway disaster warning system. It integrates **AI, meteorology, railway engineering, and low-altitude drone technology** through the proprietary **LoongClaw Dynamic Router Mixture-of-Experts (MoE) framework** to deliver minute-level early warnings for railway corridor hazards.

> **One-line pitch**: AI-empowered railway disaster prevention digital twin command center.

### Key Innovations

- **MambaSwin-UNet-STA**: Novel deep learning architecture fusing Mamba state-space models, Swin Transformer, U-Net, and spatiotemporal attention
- **LoongClaw MoE Framework**: Dynamic routing among AI/Physics/Meteorology/Railway four expert systems
- **SCS-CN Hydrology Coupling**: Physics-constrained runoff modeling for disaster risk inference
- **Multi-Platform Delivery**: Python ML backend, Web 3D dashboard, WeChat Mini Program

---

## 🏗️ Repository Structure

```
railway-ai-warning/
│
├── README.md                         # Master README (this file)
├── LICENSE                           # MIT License
├── .gitignore
│
├── backend/                          # 🐍 Python ML Framework
│   ├── README.md                     # Backend-specific documentation
│   ├── requirements.txt              # Python dependencies
│   ├── __init__.py                   # Dragon class entry point
│   ├── core/                         # Agent framework
│   │   ├── agent.py                  # Task planning engine (5-phase scheduler)
│   │   ├── dialog.py                 # Dialogue manager
│   │   ├── memory.py                 # Memory system (short/long-term)
│   │   ├── skills.py                 # Skill manager (13 built-in skills)
│   │   └── workflow.py               # Workflow engine
│   ├── src/                          # ML source code
│   │   ├── models/                   # Neural network architectures
│   │   │   ├── mamba_swin_unet.py    # MambaSwin-UNet-STA main model
│   │   │   ├── router.py             # LoongClaw dynamic router
│   │   │   └── physics.py            # Physical constraints & hydrology
│   │   ├── data/                     # Data processing pipeline
│   │   │   ├── preprocess.py         # Quality control & normalization
│   │   │   ├── features.py           # Terrain/radar/temporal features
│   │   │   └── interpolate.py        # Missing value imputation
│   │   ├── training/train.py         # PyTorch Lightning training
│   │   └── utils/                    # Loss functions & metrics
│   ├── scripts/                      # Data download scripts
│   │   ├── download_era5.py          # ERA5 reanalysis data
│   │   └── download_dem.py           # SRTM DEM processing
│   ├── tests/                        # Unit & integration tests
│   ├── configs/                      # YAML configuration
│   │   ├── project.yaml              # Project phases & settings
│   │   └── model.yaml                # Model/training hyperparameters
│   ├── skills/                       # Extensible skill modules
│   ├── knowledge/                    # Domain knowledge base
│   └── notebooks/                    # Jupyter notebooks
│
├── web/                              # 🌐 Web Visualization Dashboard
│   ├── index.html                    # 3D starfield entry portal
│   ├── core.html                     # LoongClaw engine architecture
│   ├── system.html                   # Holographic system overview
│   ├── community.html                # Ecosystem & partnerships
│   ├── universe.html                 # Technology universe panorama
│   ├── dashboard.html                # Real-time data cockpit
│   ├── sky.html                      # UAV swarm management
│   ├── scripts/
│   │   └── collect_news_final.py     # Industry news auto-collector
│   └── assets/                       # Static assets
│       ├── pdf/                      # Whitepapers & proposals
│       ├── images/                   # System screenshots
│       └── videos/                   # Demo videos
│
├── miniprogram/                      # 📱 WeChat Mini Program
│   ├── project.config.json           # WeChat project config
│   ├── app.js / app.json / app.wxss  # App entry & global style
│   ├── pages/                        # 12 business pages
│   │   ├── launch/                   # Splash screen
│   │   ├── home/                     # Home (core entry)
│   │   ├── overview/                 # Project overview
│   │   ├── painpoints/               # Industry pain points
│   │   ├── tech/                     # 4-layer tech stack
│   │   ├── openclaw/                 # LoongClaw engine
│   │   ├── uav/                      # UAV platform
│   │   ├── achievement/              # Results & validation
│   │   ├── business/                 # Business model
│   │   ├── team/                     # Team introduction
│   │   ├── vision/                   # Social value & vision
│   │   └── contact/                  # Contact & demo booking
│   ├── components/                   # 8 reusable components
│   └── images/                       # App icons & illustrations
│
├── research/                         # 🔬 Auxiliary Research Code
│   └── convlstm/                     # ConvLSTM baseline model
│       ├── encoder.py / decoder.py   # Seq2seq architecture
│       ├── model.py                  # ConvLSTM cell implementation
│       ├── main.py / predict.py      # Training & inference
│       └── requirements.txt
│
├── docs/                             # 📄 Documentation
│   ├── proposals/                    # Project proposals
│   │   └── 萃英基金申报书.pdf
│   ├── technical/                    # Technical documents
│   │   └── technical_proposal.md
│   ├── data_dict.md                  # Data dictionary
│   ├── architecture.md               # System architecture
│   ├── plan.md                       # Project plan
│   ├── roadmap.md                    # Technical roadmap
│   └── autodl_guide.md              # Cloud GPU quickstart
│
├── data/                             # 📊 Data (gitignored)
│   └── .gitkeep
│
└── .github/                          # ⚙️ GitHub
    └── workflows/                    # CI/CD pipelines
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** with PyTorch 2.0+ (for backend)
- **Modern browser** (Chrome/Edge/Firefox) for Web dashboard
- **WeChat DevTools** v1.06+ (for mini program)

### Backend (ML Framework)

```bash
cd backend
pip install -r requirements.txt

# Launch research assistant CLI
python __init__.py

# Train the MambaSwin-UNet-STA model
python src/training/train.py --config configs/model.yaml

# Run model tests
python tests/test_model.py
```

### Web Dashboard

```bash
# No build step required — pure HTML/CSS/JS
# Open in browser:
open web/index.html        # macOS
start web/index.html       # Windows
xdg-open web/index.html    # Linux

# Or deploy to any static server (GitHub Pages / Vercel / Nginx)
```

### WeChat Mini Program

```bash
# 1. Open WeChat DevTools
# 2. Import project → select miniprogram/ directory
# 3. Replace "touristappid" in project.config.json with your AppID
# 4. Compile & run
```

---

## 🧠 LoongClaw MoE Architecture

| Expert | Core Model | Specialty |
|--------|-----------|-----------|
| 🤖 **AI Expert** | MambaSwin-UNet-STA (45M params) | End-to-end precipitation forecasting |
| 🔬 **Physics Expert** | COTREC + WRF | Numerical weather prediction, PDE constraints |
| 🌤️ **Meteorology Expert** | FY-4A + Doppler Radar | Multi-source data fusion, satellite retrieval |
| 🚄 **Railway Expert** | Disaster KG + Fragility Curves | Risk assessment, infrastructure vulnerability |

---

## 📊 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| TS (Threat Score) | Hit / (Hit + Miss + False Alarm) | > 0.50 |
| POD (Probability of Detection) | Hit / (Hit + Miss) | > 0.80 |
| FAR (False Alarm Rate) | False Alarm / (Hit + False Alarm) | < 0.30 |
| CSI (Critical Success Index) | Same as TS | > 0.50 |

---

## 🗓️ Project Roadmap

| Phase | Period | Key Tasks |
|-------|--------|-----------|
| 📊 Data Governance | 2026.04–05 | Data cleaning, interpolation, terrain features |
| 🧪 Model Training | 2026.05–08 | MambaSwin-UNet-STA, dynamic router, hyperparameter tuning |
| 🔗 System Integration | 2026.08–11 | SCS-CN coupling, risk inference, end-to-end testing |
| ✅ Validation | 2026.12–2027.01 | Case studies, field investigation, usability assessment |
| 📝 Finalization | 2027.02–04 | Paper writing, code open-sourcing, defense preparation |

---

## 👥 Team

| Role | Detail |
|------|--------|
| **Team Name** | 智驭苍穹 (Wisdom Commands the Skies) |
| **University** | Lanzhou University (兰州大学) |
| **Advisor** | Prof. Hu Shujuan (胡淑娟 教授) |
| **Project Lead** | Peng Xiaoxi (彭小溪) |
| **Program** | National Undergraduate Innovation Training Program |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📞 Contact

- 📧 Email: pxx05247258@gmail.com
- 📍 Address: Lanzhou University, Chengguan District, Lanzhou, China

---

<div align="center">

**🛤️ 空天地一体 · AI赋能铁路 · 守护万里安澜 🛤️**

*Air, Space, and Ground United — AI Empowering Railways — Safeguarding Every Mile*

</div>
