# 🛤️ 智驭苍穹 · 守路安澜 — Railway AI Warning System

<div align="center">

**Air-Space-Ground Multi-Modal Short-Imminent Disaster Risk Digital Twin Warning System**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=flat&logo=pytorch)](https://pytorch.org/)
[![WeChat](https://img.shields.io/badge/Platform-微信小程序-07C160?style=flat&logo=wechat)](https://developers.weixin.qq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Team](https://img.shields.io/badge/Team-兰州大学-165DFF?style=flat)](https://www.lzu.edu.cn/)

</div>

---

## 📖 Overview

**"智驭苍穹 · 守路安澜"** is an AI-powered multi-modal railway disaster early warning system developed at Lanzhou University. It integrates deep learning, numerical weather prediction, remote sensing, and railway engineering through the proprietary **LoongClaw Dynamic Router MoE framework** to deliver minute-level hazard warnings for railway corridors.

> **Mission**: AI Empowering Railways — Safeguarding Every Mile

<div align="center">
  <img src="assets/figures/remote_sensing_weather_ai.png" alt="Remote Sensing & AI Weather Forecasting" width="90%">
  <p><em>Multi-source remote sensing data fusion and AI-driven extreme weather forecasting — from satellite constellations to railway corridor risk assessment</em></p>
</div>

---

## 🔬 Technical Approach

<div align="center">
  <img src="assets/figures/project_pipeline.png" alt="Project Pipeline" width="80%">
  <p><em>End-to-end research pipeline: data acquisition → quality control → feature engineering → model training → risk inference → visualization</em></p>
</div>

### Core Innovations

| Innovation | Technical Stack | Highlights |
|-----------|----------------|------------|
| **MambaSwin-UNet-STA** | Mamba SSM + Swin Transformer + U-Net + Spatiotemporal Attention | 45M params, linear-complexity sequence modeling, 200ms inference |
| **LoongClaw MoE Router** | Dynamic expert weighting based on real-time weather context | AI + Physics + Meteorology + Railway four-expert collaborative inference |
| **SCS-CN Hydrology** | USDA Curve Number method coupled with DEM flow routing | Physics-constrained runoff prediction, railway corridor risk mapping |
| **Multi-Platform Delivery** | Python backend + Web 3D dashboard + WeChat Mini Program | Full-stack deployment from research prototype to public-facing product |

<div align="center">
  <img src="assets/figures/research_framework.png" alt="Research Framework" width="85%">
  <p><em>LoongClaw research framework — bridging atmospheric science, artificial intelligence, and railway engineering</em></p>
</div>

---

## 🏗️ Repository Structure

```
railway-ai-warning/
├── README.md                    # Master documentation
├── LICENSE                      # MIT License
├── assets/                      # Visual assets (figures & animations)
│   ├── figures/                 # Static diagrams & results
│   └── animations/              # Dynamic demos
│
├── backend/                     # Python ML Framework
│   ├── __init__.py              # Dragon class (CLI entry)
│   ├── requirements.txt
│   ├── core/                    # Agent framework (5 engines)
│   ├── src/                     # ML source (models/data/training/utils)
│   ├── scripts/                 # ERA5 & DEM download
│   ├── configs/                 # project.yaml + model.yaml
│   ├── tests/                   # Unit & integration tests
│   └── knowledge/               # Domain knowledge base
│
├── web/                         # Web Visualization Dashboard
│   ├── index.html               # 3D starfield portal
│   ├── core.html                # LoongClaw engine architecture
│   ├── system.html              # Holographic system overview
│   ├── community.html           # Ecosystem & partnerships
│   ├── universe.html            # Technology universe
│   ├── dashboard.html           # Real-time monitoring cockpit
│   └── sky.html                 # UAV swarm management
│
├── miniprogram/                 # WeChat Mini Program
│   ├── app.js / app.json        # 12-page Apple-style UI
│   ├── pages/                   # Launch, Home, Tech, UAV, etc.
│   └── components/              # 8 reusable glass-morphism components
│
├── research/                    # Auxiliary research code
│   └── convlstm/                # ConvLSTM baseline model
│
├── docs/                        # Documentation
│   ├── proposals/               # Project proposals & applications
│   ├── technical/               # Technical design documents
│   ├── architecture.md          # System architecture
│   └── roadmap.md               # Development roadmap
│
└── data/                        # Data storage (gitignored)
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python __init__.py                          # Launch Dragon CLI
python src/training/train.py --config configs/model.yaml  # Train model
python tests/test_model.py                  # Verify correctness
```

### Web Dashboard

```bash
# Zero build — pure HTML/CSS/JS, CDN-loaded dependencies
open web/index.html
```

### WeChat Mini Program

```bash
# WeChat DevTools → Import → select miniprogram/ directory
# Replace "touristappid" in project.config.json with your AppID
```

---

## 🧠 LoongClaw MoE Architecture

| Expert | Model | Responsibility |
|--------|-------|----------------|
| 🤖 **AI** | MambaSwin-UNet-STA | End-to-end precipitation nowcast, spatiotemporal modeling |
| 🔬 **Physics** | COTREC + WRF | Numerical weather prediction, mass/energy conservation |
| 🌤️ **Meteorology** | FY-4A + Doppler Radar | Multi-source satellite/radar data fusion |
| 🚄 **Railway** | Disaster KG + Fragility Curves | Infrastructure vulnerability, risk assessment |

<div align="center">
  <img src="assets/figures/ai_natural_systems.png" alt="AI & Natural Systems" width="70%">
  <img src="assets/animations/data_fusion.gif" alt="Data Fusion" width="46%">
  <img src="assets/figures/physics_ai.png" alt="Physics-AI Integration" width="46%">
  <p><em>AI-driven understanding of complex atmospheric systems (top) · Multi-source data fusion dynamics (bottom left) · Physics-informed AI integration (bottom right)</em></p>
</div>

---

## 📊 Evaluation

| Metric | Formula | Target |
|--------|---------|--------|
| TS (Threat Score) | H / (H + M + F) | > 0.50 |
| POD (Detection Rate) | H / (H + M) | > 0.80 |
| FAR (False Alarm) | F / (H + F) | < 0.30 |
| CSI | H / (H + M + F) | > 0.50 |

*H = Hits, M = Misses, F = False Alarms*

---

## 🗓️ Roadmap

| Phase | Period | Status |
|-------|--------|--------|
| 📊 Data Governance | 2026.04–05 | ✅ Complete |
| 🧪 Model Training | 2026.05–08 | 🔄 In Progress |
| 🔗 System Integration | 2026.08–11 | ⬜ Pending |
| ✅ Field Validation | 2026.12–2027.01 | ⬜ Pending |
| 📝 Publication | 2027.02–04 | ⬜ Pending |

---

## 👥 Team

| Role | Detail |
|------|--------|
| **Team** | 智驭苍穹 (Wisdom Commands the Skies) |
| **University** | Lanzhou University |
| **Advisor** | Prof. Hu Shujuan |
| **Lead** | Peng Xiaoxi |
| **Program** | National Undergraduate Innovation Training · 䇹政基金 |

---

## 📄 License

MIT License © 2026 NOBEL-Pxx

---

<div align="center">

**🛤️ 空天地一体 · AI赋能铁路 · 守护万里安澜 🛤️**

</div>
