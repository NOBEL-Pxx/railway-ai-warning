# -*- coding: utf-8 -*-
import os, shutil

src_dir = r'C:\Users\lenovo\Desktop\图片资源占位'
dst_dir = r'C:\Users\lenovo\Desktop\微信小程序\railway-ai-warning\miniprogram\images\resources'
os.makedirs(dst_dir, exist_ok=True)

# 中文文件名 -> 短英文文件名（语义对应）
mapping = {
    'AI驱动WRF模式台风预报.png':                        'wrf_typhoon_forecast.png',
    'ConvLSTM时空序列预测架构（经典基线.png':             'convlstm_arch.png',
    'DeepMind DGMR短临降水预报对比.png':                 'dgmr_nowcast.png',
    'Mamba状态空间模型核心架构.png':                     'mamba_ssm_arch.png',
    'Mamba编码器与双向SSM设计（Audio Mamba示例）.png':    'mamba_bidirectional_ssm.png',
    'MetNet-2混合预报系统流程.png':                      'metnet2_pipeline.png',
    'SCS-CN曲线数法径流模型.png':                       'scs_cn_runoff.png',
    'Swin Transformer移位窗口注意力掩码示意图.png':        'swin_window_attention.png',
    '中国西北地区降水时空分布与400mm等降水量线.jpg':         'nw_china_precip_map.jpg',
    '基于双分支编码器的雷达回波外推模型（STAGRU）.jpg':       'stagru_radar_model.jpg',
    '小流域水文循环过程.png':                            'small_watershed_hydro.png',
    '带自注意力机制的SA-ConvLSTM单元结构.jpg':            'sa_convlstm_unit.jpg',
    '数字孪生基础设施风险评估框架.png':                    'digital_twin_infra_risk.png',
    '数字孪生施工安全风险预测框架.jpg':                    'digital_twin_safety.jpg',
    '无人机地球物理遥感系统架构.jpg':                     'uav_geophysics_remote.jpg',
    '无人机遥感与电磁散射融合框架.jpg':                    'uav_em_fusion.jpg',
    '时空Transformer编码器-解码器架构.png':               'spatiotemporal_transformer.png',
    '时空解耦注意力Transformer（SDA-TR）.png':            'sda_tr_attention.png',
    '泥石流-轨道-列车相互作用机理.jpg':                    'debris_flow_railway.jpg',
    '洪水早期预警系统决策流程.webp':                      'flood_warning_flow.webp',
    '混合专家模型（MoE）路由机制.jpg':                    'moe_routing.jpg',
    '空天地一体化网络架构（Space-Air-Ground）.webp':       'space_air_ground_arch.webp',
    '西北地区降水极值与趋势显著性统计.jpg':                 'nw_precip_extreme_trend.jpg',
    '边缘AI数据融合与加速框架.png':                       'edge_ai_fusion.png',
    '边缘计算三层架构（云-雾-端）.webp':                   'edge_cloud_fog_end.webp',
    '通用MoE层架构（Router + Experts）.jpeg':            'moe_layer_arch.jpeg',
    '铁路沿线泥石流灾害与列车脱轨数值模拟.jpg':              'railway_debris_simulation.jpg',
    '降雨-入渗-径流过程曲线.png':                        'rain_infiltration_runoff.png',
    '雷达回波CAPPI拼图产品示例.jpg':                      'radar_cappi_product.jpg',
    '雷达回波外推深度学习框架（TSRC模型）.jpg':              'tsrc_radar_dl.jpg',
    '雷达回波外推进化网络与生成网络.jpg':                    'radar_gan_nowcast.jpg',
    '雷达回波序列生成对抗外推网络.jpg':                     'radar_seq_gan.jpg',
    '雷达波束几何盲区示意.png':                           'radar_beam_blind.png',
    '雷达波束山地遮挡与盲区形成.webp':                     'radar_mountain_block.webp',
}

ok = 0
miss = []
for cn, en in mapping.items():
    src = os.path.join(src_dir, cn)
    dst = os.path.join(dst_dir, en)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'OK: {en}')
        ok += 1
    else:
        print(f'MISS: {cn}')
        miss.append(cn)

print(f'\n共复制 {ok} 个文件，缺失 {len(miss)} 个')
if miss:
    for m in miss:
        print(f'  缺失: {m}')
