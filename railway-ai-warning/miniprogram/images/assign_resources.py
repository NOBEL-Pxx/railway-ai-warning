# -*- coding: utf-8 -*-
"""
图片资源分配脚本
规则：
1. resources/ 共34张（用户提供，语义强，优先分配到正文内容页）
2. academic/ 共12张（自制，作为补充/随机池）
3. 同一张图不在两处重复出现
4. launch 页 logo-icon 区域 => 随机池（多张）
"""

import os, re

base = r'C:\Users\lenovo\Desktop\微信小程序\railway-ai-warning\miniprogram'

# ============================================================
# 分配方案：每个占位符 -> 新图（语义对应，全局唯一）
# 格式：(旧路径, 新路径)
# ============================================================
PLAN = [
    # ---- launch 页 ----
    # logo-icon: 改为由JS随机，wxml只留 {{launchBgImage}} 占位
    # tag 图标（4个）: 用 resources/ 中语义强的图
    ('/images/academic/forecast_score.png',         '/images/resources/sda_tr_attention.png'),    # 人工智能tag
    ('/images/academic/digital_twin.png',           '/images/resources/space_air_ground_arch.webp'),  # 卫星遥感tag
    ('/images/academic/uav_route.png',              '/images/resources/uav_geophysics_remote.jpg'),  # 铁路防灾tag（UAV图）
    ('/images/academic/sensor_payload.png',         '/images/resources/uav_em_fusion.jpg'),       # 低空巡检tag

    # feature 图标（3个）
    # sensor_payload -> uav_em_fusion (上面已用)，需要3个不重复的feature图
    # 这里采用 wxml 内联修改，见下方 WXML_PATCH

    # ---- uav 页 ----
    # payload图 (原 sensor_payload x2, hydrology_model, radar_echo)
    # uav_route 已经替换为 uav_geophysics_remote (launch tag)
    # 给 uav 页用真正的无人机图
    ('/images/academic/radar_echo.png',             '/images/resources/radar_cappi_product.jpg'),
    ('/images/academic/hydrology_model.png',        '/images/resources/small_watershed_hydro.png'),
    ('/images/academic/risk_heatmap.png',           '/images/resources/railway_debris_simulation.jpg'),

    # ---- painpoints 页 ----
    ('/images/academic/slope_analysis.png',         '/images/resources/debris_flow_railway.jpg'),
    # forecast_score -> 已分配给 launch tag，painpoints 里重用要换掉
    # 下方 WXML_PATCH 里单独处理

    # ---- home 页 新闻图 ----
    # precip_timeseries x2 -> 换两张不同的降水图
    # forecast_score -> 已分配，需换
    # radar_echo -> 已分配，需换

    # ---- openclaw 页 ----
    ('/images/academic/satellite_ir.jpg',           '/images/resources/edge_cloud_fog_end.webp'),
    # neural_arch: openclaw 架构图保留 academic/neural_arch 不变（OpenClaw自制图语义合适）

    # ---- vision 页 ----
    # satellite_ir -> 已分配给 openclaw，vision 里换一张
    # digital_twin -> 已分配给 launch tag，vision 里换

    # ---- contact 页 ----
    ('/images/academic/neural_arch.png',            '/images/resources/moe_routing.jpg'),  # contact头像换成MoE图

    # ---- business 页 论文图 ----
    # slope_analysis -> 已分配 debris_flow_railway
    # radar_echo -> 已分配 radar_cappi
    # precip_timeseries x 多处 -> 分配不同的降水图
    # data_fusion -> 保留或换

]

# 由于多处重复引用同一 academic 图，采用按页面逐一替换更精确
# 用正则逐文件处理

# ==========================
# 各页面的精确替换规则
# (文件相对路径, [(old_img, new_img), ...])
# ==========================
PER_FILE_REPLACEMENTS = {
    # launch.wxml
    'pages/launch/launch.wxml': [
        # logo-icon: 改为动态 {{launchBgImage}}
        ('src="/images/academic/satellite_ir.jpg" mode="aspectFit" lazy-load="true"',
         'src="{{launchBgImage}}" mode="aspectFit" lazy-load="true"'),
        # 4个 tag 图标
        ('src="/images/academic/forecast_score.png" mode="aspectFit">',  # 人工智能
         'src="/images/resources/spatiotemporal_transformer.png" mode="aspectFit">'),
        ('src="/images/academic/digital_twin.png" mode="aspectFit">',    # 卫星遥感
         'src="/images/resources/space_air_ground_arch.webp" mode="aspectFit">'),
        ('src="/images/academic/uav_route.png" mode="aspectFit">',       # 铁路防灾
         'src="/images/resources/uav_geophysics_remote.jpg" mode="aspectFit">'),
        ('src="/images/academic/sensor_payload.png" mode="aspectFit">',  # 低空巡检
         'src="/images/resources/uav_em_fusion.jpg" mode="aspectFit">'),
        # feature 图标 (3个)
        ('src="/images/academic/sensor_payload.png" mode="aspectFit"',   # 实时预警 feature
         'src="/images/resources/flood_warning_flow.webp" mode="aspectFit"'),
        ('src="/images/academic/data_fusion.png" mode="aspectFit"',      # 智能分析 feature
         'src="/images/resources/edge_ai_fusion.png" mode="aspectFit"'),
        ('src="/images/academic/neural_arch.png" mode="aspectFit"',      # 云端协同 feature
         'src="/images/resources/edge_cloud_fog_end.webp" mode="aspectFit"'),
        # team-logo
        ('src="/images/academic/slope_analysis.png" mode="aspectFit"',
         'src="/images/resources/nw_china_precip_map.jpg" mode="aspectFit"'),
    ],

    # uav.wxml
    'pages/uav/uav.wxml': [
        # uav-image (主图)
        ('src="/images/academic/uav_route.png"',
         'src="/images/resources/uav_geophysics_remote.jpg"'),
        # payload 图（4个载荷）- 语义对应
        # 第1个 sensor_payload -> 多光谱/RGB: sa_convlstm (不是最优，但暂用stagru)
        # 用4张不同图对应4种载荷
    ],

    # uav.js - payload 图
    'pages/uav/uav.js': [
        ("'/images/academic/sensor_payload.png',\n          image: '/images/academic/sensor_payload.png'",
         "'/images/resources/sa_convlstm_unit.jpg',\n          image: '/images/resources/sa_convlstm_unit.jpg'"),
        ("image: '/images/academic/sensor_payload.png'",
         "image: '/images/resources/sa_convlstm_unit.jpg'"),
        ("image: '/images/academic/hydrology_model.png'",
         "image: '/images/resources/scs_cn_runoff.png'"),
        ("image: '/images/academic/radar_echo.png'",
         "image: '/images/resources/radar_cappi_product.jpg'"),
        ("'/images/academic/risk_heatmap.png'",
         "'/images/resources/railway_debris_simulation.jpg'"),
    ],

    # uav.wxml payload images
    'pages/uav/uav.wxml_payload': [],  # handled below

    # painpoints.wxml
    'pages/painpoints/painpoints.wxml': [
        # card-icon-img (3个): forecast_score, risk_heatmap, slope_analysis
        ('src="/images/academic/forecast_score.png" mode="aspectFill"',
         'src="/images/resources/tsrc_radar_dl.jpg" mode="aspectFill"'),
        ('src="/images/academic/risk_heatmap.png" mode="aspectFill"',
         'src="/images/resources/radar_beam_blind.png" mode="aspectFill"'),
        ('src="/images/academic/slope_analysis.png" mode="aspectFill"',
         'src="/images/resources/debris_flow_railway.jpg" mode="aspectFill"'),
        # case-bg (precip_timeseries)
        ('src="/images/academic/precip_timeseries.png" mode="aspectFill"',
         'src="/images/resources/nw_precip_extreme_trend.jpg" mode="aspectFill"'),
        # case-large-img (slope_analysis, precip_timeseries)
        ('data-url="/images/academic/slope_analysis.png"',
         'data-url="/images/resources/debris_flow_railway.jpg"'),
        ('data-url="/images/academic/precip_timeseries.png"',
         'data-url="/images/resources/nw_precip_extreme_trend.jpg"'),
        # solution-bg (data_fusion)
        ('src="/images/academic/data_fusion.png" mode="aspectFill"',
         'src="/images/resources/metnet2_pipeline.png" mode="aspectFill"'),
    ],

    # home.wxml 新闻图
    'pages/home/home.wxml': [
        # 3条新闻图
        ('src="/images/academic/precip_timeseries.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/dgmr_nowcast.png" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/forecast_score.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/wrf_typhoon_forecast.png" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/radar_echo.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/stagru_radar_model.jpg" mode="aspectFill" lazy-load="true"'),
    ],

    # contact.wxml 头像
    'pages/contact/contact.wxml': [
        ('src="/images/academic/neural_arch.png" mode="aspectFit"',
         'src="/images/resources/moe_routing.jpg" mode="aspectFit"'),
    ],

    # openclaw.wxml
    'pages/openclaw/openclaw.wxml': [
        # arch-img (主架构图) neural_arch 保留 academic 版（自制，语义合适，但改为resources的MoE图更贴切）
        ('src="/images/academic/neural_arch.png" mode="aspectFit" lazy-load="true"',
         'src="/images/resources/moe_layer_arch.jpeg" mode="aspectFit" lazy-load="true"'),
        # arch-small-img (3个辅图)
        ('src="/images/academic/satellite_ir.jpg" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/convlstm_arch.png" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/forecast_score.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/swin_window_attention.png" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/digital_twin.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/mamba_ssm_arch.png" mode="aspectFill" lazy-load="true"'),
    ],

    # openclaw.js
    'pages/openclaw/openclaw.js': [
        ("architectureImage: '/images/academic/neural_arch.png'",
         "architectureImage: '/images/resources/moe_layer_arch.jpeg'"),
        ("'/images/academic/neural_arch.png'",
         "'/images/resources/moe_layer_arch.jpeg'"),
    ],

    # vision.wxml
    'pages/vision/vision.wxml': [
        # bg-image
        ('src="/images/academic/satellite_ir.jpg" mode="aspectFill"',
         'src="/images/resources/nw_china_precip_map.jpg" mode="aspectFill"'),
        # badge-icon
        ('src="/images/academic/forecast_score.png" mode="aspectFit"',
         'src="/images/resources/mamba_bidirectional_ssm.png" mode="aspectFit"'),
        # slogan-bg
        ('src="/images/academic/digital_twin.png" mode="aspectFill"',
         'src="/images/resources/digital_twin_infra_risk.png" mode="aspectFill"'),
    ],

    # business.wxml 论文图
    'pages/business/business.wxml': [
        ('src="/images/academic/slope_analysis.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/rain_infiltration_runoff.png" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/radar_echo.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/radar_mountain_block.webp" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/precip_timeseries.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/radar_seq_gan.jpg" mode="aspectFill" lazy-load="true"'),
        ('src="/images/academic/data_fusion.png" mode="aspectFill" lazy-load="true"',
         'src="/images/resources/radar_gan_nowcast.jpg" mode="aspectFill" lazy-load="true"'),
    ],
}

# uav.wxml payload 直接处理
UAV_WXML_PAYLOAD = [
    ('src="/images/academic/sensor_payload.png" mode="aspectFill" lazy-load="true"</image>\n        </view>\n        <view class="payload-item">\n          <image class="payload-image" src="/images/academic/sensor_payload.png"',
     'src="/images/resources/sa_convlstm_unit.jpg" mode="aspectFill" lazy-load="true"</image>\n        </view>\n        <view class="payload-item">\n          <image class="payload-image" src="/images/resources/sda_tr_attention.png"'),
]

# ============================================================
# 执行替换
# ============================================================
changed = []

for rel_path, replacements in PER_FILE_REPLACEMENTS.items():
    if rel_path.endswith('_payload'):
        continue
    fp = os.path.join(base, rel_path)
    if not os.path.exists(fp):
        print(f'FILE NOT FOUND: {rel_path}')
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
    if new_content != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed.append(rel_path)
        print(f'UPDATED: {rel_path}')
    else:
        print(f'NO CHANGE: {rel_path} (check old strings!)')

# uav.wxml payload - 单独处理两次重复的 sensor_payload 图
fp = os.path.join(base, 'pages/uav/uav.wxml')
with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()
new_content = content
# 4个payload图：逐行不同
payload_old = [
    'src="/images/academic/sensor_payload.png" mode="aspectFill" lazy-load="true"></image>',
    'src="/images/academic/sensor_payload.png" mode="aspectFill" lazy-load="true"></image>',
    'src="/images/academic/hydrology_model.png" mode="aspectFill" lazy-load="true"></image>',
    'src="/images/academic/radar_echo.png" mode="aspectFill" lazy-load="true"></image>',
]
payload_new = [
    'src="/images/resources/sa_convlstm_unit.jpg" mode="aspectFill" lazy-load="true"></image>',
    'src="/images/resources/sda_tr_attention.png" mode="aspectFill" lazy-load="true"></image>',
    'src="/images/resources/scs_cn_runoff.png" mode="aspectFill" lazy-load="true"></image>',
    'src="/images/resources/radar_cappi_product.jpg" mode="aspectFill" lazy-load="true"></image>',
]
for o, n in zip(payload_old, payload_new):
    pos = new_content.find(o)
    if pos >= 0:
        new_content = new_content[:pos] + n + new_content[pos+len(o):]
    else:
        print(f'  UAV payload NOT FOUND: {o[:60]}')

# uav-image 主图
new_content = new_content.replace(
    'src="/images/academic/uav_route.png" mode="aspectFit" lazy-load="true"',
    'src="/images/resources/uav_geophysics_remote.jpg" mode="aspectFit" lazy-load="true"'
)
# fleet-map
new_content = new_content.replace(
    'src="/images/academic/risk_heatmap.png" mode="aspectFill" lazy-load="true"',
    'src="/images/resources/railway_debris_simulation.jpg" mode="aspectFill" lazy-load="true"'
)
if new_content != content:
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    changed.append('pages/uav/uav.wxml')
    print('UPDATED: pages/uav/uav.wxml')

print(f'\n共修改 {len(changed)} 个文件')
