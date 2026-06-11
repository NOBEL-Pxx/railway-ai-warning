# 项目结构说明

## 智驭苍穹・守路安澜 - 微信小程序完整代码

### 目录结构

```
railway-ai-warning/
├── miniprogram/                    # 小程序源代码
│   ├── app.js                      # 小程序入口逻辑
│   ├── app.json                    # 小程序全局配置
│   ├── app.wxss                    # 小程序全局样式
│   ├── sitemap.json                # 站点地图配置
│   ├── theme.json                  # 主题配置（深色/浅色模式）
│   ├── project.config.json         # 项目配置文件
│   │
│   ├── pages/                      # 页面目录（12个页面）
│   │   ├── launch/                 # 启动页
│   │   │   ├── launch.wxml
│   │   │   ├── launch.wxss
│   │   │   ├── launch.js
│   │   │   └── launch.json
│   │   │
│   │   ├── home/                   # 首页
│   │   │   ├── home.wxml
│   │   │   ├── home.wxss
│   │   │   ├── home.js
│   │   │   └── home.json
│   │   │
│   │   ├── overview/               # 项目概况
│   │   │   ├── overview.wxml
│   │   │   ├── overview.wxss
│   │   │   ├── overview.js
│   │   │   └── overview.json
│   │   │
│   │   ├── painpoints/             # 行业痛点
│   │   │   ├── painpoints.wxml
│   │   │   ├── painpoints.wxss
│   │   │   ├── painpoints.js
│   │   │   └── painpoints.json
│   │   │
│   │   ├── tech/                   # 技术架构
│   │   │   ├── tech.wxml
│   │   │   ├── tech.wxss
│   │   │   ├── tech.js
│   │   │   └── tech.json
│   │   │
│   │   ├── openclaw/               # LoongClaw引擎
│   │   │   ├── openclaw.wxml
│   │   │   ├── openclaw.wxss
│   │   │   ├── openclaw.js
│   │   │   └── openclaw.json
│   │   │
│   │   ├── uav/                    # 空天感知平台
│   │   │   ├── uav.wxml
│   │   │   ├── uav.wxss
│   │   │   ├── uav.js
│   │   │   └── uav.json
│   │   │
│   │   ├── achievement/            # 成果验证
│   │   │   ├── achievement.wxml
│   │   │   ├── achievement.wxss
│   │   │   ├── achievement.js
│   │   │   └── achievement.json
│   │   │
│   │   ├── business/               # 商业模式
│   │   │   ├── business.wxml
│   │   │   ├── business.wxss
│   │   │   ├── business.js
│   │   │   └── business.json
│   │   │
│   │   ├── team/                   # 团队介绍
│   │   │   ├── team.wxml
│   │   │   ├── team.wxss
│   │   │   ├── team.js
│   │   │   └── team.json
│   │   │
│   │   ├── vision/                 # 社会价值与愿景
│   │   │   ├── vision.wxml
│   │   │   ├── vision.wxss
│   │   │   ├── vision.js
│   │   │   └── vision.json
│   │   │
│   │   └── contact/                # 联系我们
│   │       ├── contact.wxml
│   │       ├── contact.wxss
│   │       ├── contact.js
│   │       └── contact.json
│   │
│   ├── components/                 # 组件目录
│   │   ├── glass-card/             # 磨砂玻璃卡片组件
│   │   │   ├── glass-card.wxml
│   │   │   ├── glass-card.wxss
│   │   │   ├── glass-card.js
│   │   │   └── glass-card.json
│   │   │
│   │   └── chart/                  # 图表组件
│   │       ├── chart.wxml
│   │       ├── chart.wxss
│   │       ├── chart.js
│   │       └── chart.json
│   │
│   ├── utils/                      # 工具函数
│   │   └── util.js                 # 通用工具函数
│   │
│   └── images/                     # 图片资源（使用网络占位）
│       └── .gitkeep
│
├── README.md                       # 项目说明文档
└── PROJECT_STRUCTURE.md            # 项目结构文档
```

### 页面清单

| 序号 | 页面名称 | 文件路径 | 功能说明 |
|------|----------|----------|----------|
| 1 | 启动页 | pages/launch/ | 全屏动画启动，展示项目LOGO和Slogan |
| 2 | 首页 | pages/home/ | 四大核心模块入口，快速导航 |
| 3 | 项目概况 | pages/overview/ | 一句话定位、核心价值、解决方案 |
| 4 | 行业痛点 | pages/painpoints/ | 观测/预报/决策三大盲区分析 |
| 5 | 技术架构 | pages/tech/ | 四层技术栈可视化展示 |
| 6 | LoongClaw引擎 | pages/openclaw/ | 四大专家模块与动态路由机制 |
| 7 | 空天感知 | pages/uav/ | 无人机集群平台与载荷配置 |
| 8 | 成果验证 | pages/achievement/ | 精度数据、对比图表、实战案例 |
| 9 | 商业模式 | pages/business/ | 三级盈利火箭、市场规模 |
| 10 | 团队介绍 | pages/team/ | 核心成员、指导老师、合作单位 |
| 11 | 社会价值 | pages/vision/ | 防灾减灾价值、发展愿景 |
| 12 | 联系我们 | pages/contact/ | 预约演示表单、联系方式 |

### 核心功能

1. **启动动画**：淡入上浮、自动跳转
2. **页面导航**：TabBar + 页面跳转
3. **卡片交互**：磨砂玻璃效果、点击反馈
4. **数据展示**：图表、时间轴、对比展示
5. **表单提交**：预约演示表单验证与提交
6. **分享功能**：支持分享给好友和朋友圈
7. **深色模式**：自动适配系统主题

### 技术特点

- **苹果风格设计**：极简、留白、精致阴影
- **磨砂玻璃效果**：backdrop-filter实现
- **响应式布局**：适配各种屏幕尺寸
- **流畅动画**：CSS3动画 + 小程序动画API
- **组件化开发**：可复用的自定义组件

### 图片资源说明

项目中所有图片使用网络占位图（picsum.photos），实际使用时请替换为真实图片：

- Logo图片
- 无人机实拍图
- 团队成员照片
- 案例场景图片
- 架构示意图

### 开发环境

- 微信开发者工具 v1.06.2307260+
- 基础库版本 2.32.0+
- 调试基础库：2.32.0

### 如何运行

1. 下载项目代码
2. 使用微信开发者工具打开 `miniprogram` 目录
3. 在 `project.config.json` 中配置您的小程序 AppID
4. 点击编译按钮运行

### 发布上线

1. 上传代码至微信小程序后台
2. 提交审核
3. 审核通过后发布

---

**智驭苍穹・守路安澜** - 铁路防灾AI预警系统官方展示小程序