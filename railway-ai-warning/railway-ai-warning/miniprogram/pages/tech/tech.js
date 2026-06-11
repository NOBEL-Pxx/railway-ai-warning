const app = getApp();

Page({
  data: {
    activeLayer: 0,
    layerDetails: [
      {
        name: '空天感知层',
        enName: 'Space-Air Sensing Layer',
        icon: '📡',
        description: '构建空天地一体化感知网络，整合卫星遥感、无人机集群和地面气象站数据，实现铁路沿线全域覆盖的实时监测能力。',
        components: [
          { name: '卫星遥感', desc: 'FY-4A/4B、Himawari-8多源卫星数据' },
          { name: '无人机集群', desc: 'Y3垂起固定翼无人机机动补盲' },
          { name: '地面站网', desc: '自动气象站、雷达、雨量计' },
          { name: '物联网传感器', desc: '边坡监测、道岔温度、风速风向' }
        ],
        techs: ['卫星通信', '5G传输', '边缘采集', '实时回传']
      },
      {
        name: '边缘计算层',
        enName: 'Edge Computing Layer',
        icon: '⚙️',
        description: '在数据源端进行实时预处理和特征提取，降低传输延迟，提升数据处理效率，为云端推演提供高质量输入。',
        components: [
          { name: '数据预处理', desc: '去噪、校正、格式标准化' },
          { name: '特征提取', desc: '时空特征、气象要素提取' },
          { name: '数据融合', desc: '多源数据时空对齐与融合' },
          { name: '边缘缓存', desc: '热点数据本地缓存加速' }
        ],
        techs: ['Kubernetes', 'Docker', 'Redis', 'Kafka']
      },
      {
        name: '云端推演层',
        enName: 'Cloud Inference Layer',
        icon: '☁️',
        description: '核心智能推演引擎，采用LoongClaw动态路由混合专家系统，融合AI、物理、统计、LLM四大专家模型，实现高精度风险预测。',
        components: [
          { name: 'LoongClaw引擎', desc: '动态路由混合专家系统' },
          { name: 'AI专家', desc: 'MambaSwin-UNet-STA深度学习模型' },
          { name: '物理专家', desc: 'COTREC+WRF数值预报' },
          { name: 'LLM专家', desc: '大模型风险解释与决策建议' }
        ],
        techs: ['PyTorch', 'TensorFlow', 'Ray', 'MLflow']
      },
      {
        name: '孪生可视层',
        enName: 'Digital Twin Visualization',
        icon: '🌐',
        description: '基于数字孪生技术的三维场景化展示平台，直观呈现风险分布、演变趋势和预警信息，支持多终端访问。',
        components: [
          { name: '三维场景', desc: '铁路线路高精度三维建模' },
          { name: '风险可视化', desc: '热力图、等值面、动画展示' },
          { name: '预警推送', desc: '多渠道预警信息实时推送' },
          { name: '决策支持', desc: '智能决策建议与应急预案' }
        ],
        techs: ['Three.js', 'Cesium', 'WebGL', 'Mapbox']
      }
    ]
  },

  onLoad(options) {
    console.log('Tech page loaded', options);
  },

  onReady() {
    // 默认选中第一层
    this.setData({ activeLayer: 0 });
  },

  onShow() {
    // 页面显示
  },

  onHide() {
    // 页面隐藏
  },

  onUnload() {
    // 页面卸载
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '技术架构 - 智驭苍穹・守路安澜',
      '/pages/tech/tech'
    );
  },

  // 选择层级
  selectLayer(e) {
    const layer = parseInt(e.currentTarget.dataset.layer);
    this.setData({ activeLayer: layer });
    app.vibrateShort();
  },

  // 查看LoongClaw引擎
  viewLoongClaw() {
    app.vibrateShort();
    app.navigateTo('/pages/openclaw/openclaw');
  }
});