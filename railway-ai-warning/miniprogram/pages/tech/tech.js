/**
 * 技术架构页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多技术细节和交互功能
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeLayer: 0,
    showDetail: false,
    
    // 技术架构层级
    layerDetails: [
      {
        name: '空天感知层',
        enName: 'Space-Air Sensing Layer',
        icon: '',
        color: '#165DFF',
        gradient: 'linear-gradient(135deg, #165DFF 0%, #4B8BFF 100%)',
        description: '构建空天地一体化感知网络，整合卫星遥感、无人机集群和地面气象站数据，实现铁路沿线全域覆盖的实时监测能力。',
        components: [
          { 
            name: '卫星遥感', 
            desc: 'FY-4A/4B、Himawari-8多源卫星数据',
            icon: ''
          },
          { 
            name: '无人机集群', 
            desc: 'Y3垂起固定翼无人机机动补盲',
            icon: ''
          },
          { 
            name: '地面站网', 
            desc: '自动气象站、雷达、雨量计',
            icon: ''
          },
          { 
            name: '物联网传感器', 
            desc: '边坡监测、道岔温度、风速风向',
            icon: ''
          }
        ],
        techs: ['卫星通信', '5G传输', '边缘采集', '实时回传'],
        metrics: [
          { value: '1km', label: '空间分辨率' },
          { value: '5min', label: '数据更新' },
          { value: '99%', label: '数据完整率' }
        ],
        features: [
          '多源数据融合采集',
          '分钟级数据更新',
          '全域无缝覆盖',
          '边缘智能预处理'
        ]
      },
      {
        name: '边缘计算层',
        enName: 'Edge Computing Layer',
        icon: '',
        color: '#00D6B9',
        gradient: 'linear-gradient(135deg, #00D6B9 0%, #00CC99 100%)',
        description: '在数据源端进行实时预处理和特征提取，降低传输延迟，提升数据处理效率，为云端推演提供高质量输入。',
        components: [
          { 
            name: '数据预处理', 
            desc: '去噪、校正、格式标准化',
            icon: ''
          },
          { 
            name: '特征提取', 
            desc: '时空特征、气象要素提取',
            icon: ''
          },
          { 
            name: '数据融合', 
            desc: '多源数据时空对齐与融合',
            icon: ''
          },
          { 
            name: '边缘缓存', 
            desc: '热点数据本地缓存加速',
            icon: ''
          }
        ],
        techs: ['Kubernetes', 'Docker', 'Redis', 'Kafka'],
        metrics: [
          { value: '50ms', label: '处理延迟' },
          { value: '80%', label: '带宽节省' },
          { value: '10x', label: '处理加速' }
        ],
        features: [
          '毫秒级数据处理',
          '智能缓存策略',
          '边缘AI推理',
          '数据质量保障'
        ]
      },
      {
        name: '云端推演层',
        enName: 'Cloud Inference Layer',
        icon: '',
        color: '#7B61FF',
        gradient: 'linear-gradient(135deg, #7B61FF 0%, #9B8EFF 100%)',
        description: '核心智能推演引擎，采用LoongClaw动态路由混合专家系统，融合AI、物理、统计、LLM四大专家模型，实现高精度风险预测。',
        components: [
          { 
            name: 'LoongClaw引擎', 
            desc: '动态路由混合专家系统',
            icon: ''
          },
          { 
            name: 'AI专家', 
            desc: 'MambaSwin-UNet-STA深度学习模型',
            icon: ''
          },
          { 
            name: '物理专家', 
            desc: 'COTREC+WRF数值预报',
            icon: ''
          },
          { 
            name: 'LLM专家', 
            desc: '大模型风险解释与决策建议',
            icon: ''
          }
        ],
        techs: ['PyTorch', 'TensorFlow', 'Ray', 'MLflow'],
        metrics: [
          { value: '0.71', label: 'TS评分' },
          { value: '82%', label: '命中率' },
          { value: '10min', label: '响应时间' }
        ],
        features: [
          '混合专家智能融合',
          '动态权重分配',
          '多场景自适应',
          '端到端优化'
        ]
      },
      {
        name: '孪生可视层',
        enName: 'Digital Twin Visualization',
        icon: '',
        color: '#FF9500',
        gradient: 'linear-gradient(135deg, #FF9500 0%, #FFB800 100%)',
        description: '基于数字孪生技术的三维场景化展示平台，直观呈现风险分布、演变趋势和预警信息，支持多终端访问。',
        components: [
          { 
            name: '三维场景', 
            desc: '铁路线路高精度三维建模',
            icon: ''
          },
          { 
            name: '风险可视化', 
            desc: '热力图、等值面、动画展示',
            icon: ''
          },
          { 
            name: '预警推送', 
            desc: '多渠道预警信息实时推送',
            icon: ''
          },
          { 
            name: '决策支持', 
            desc: '智能决策建议与应急预案',
            icon: ''
          }
        ],
        techs: ['Three.js', 'Cesium', 'WebGL', 'Mapbox'],
        metrics: [
          { value: '60fps', label: '渲染帧率' },
          { value: '1m', label: '模型精度' },
          { value: '3端', label: '多端支持' }
        ],
        features: [
          '沉浸式三维体验',
          '实时风险渲染',
          '多端协同展示',
          '智能交互分析'
        ]
      }
    ],
    
    // 技术栈展示
    techStack: [
      { name: 'Python', category: '后端', icon: '' },
      { name: 'PyTorch', category: 'AI', icon: '' },
      { name: 'TensorFlow', category: 'AI', icon: '' },
      { name: 'Kubernetes', category: '运维', icon: '' },
      { name: 'Docker', category: '运维', icon: '' },
      { name: 'Redis', category: '数据库', icon: '' },
      { name: 'Kafka', category: '消息', icon: '' },
      { name: 'Three.js', category: '可视化', icon: '' }
    ],
    
    // 架构特点
    architectureFeatures: [
      {
        title: '高可用',
        desc: '99.9%系统可用性',
        icon: ''
      },
      {
        title: '高性能',
        desc: '毫秒级响应',
        icon: ''
      },
      {
        title: '可扩展',
        desc: '弹性伸缩架构',
        icon: ''
      },
      {
        title: '安全性',
        desc: '端到端加密',
        icon: ''
      }
    ]
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Tech] Page loaded', options);
  },

  onReady() {
    console.log('[Tech] Page ready');
    // 默认选中第一层
    this.setData({ activeLayer: 0 });
  },

  onShow() {
    console.log('[Tech] Page show');
  },

  onHide() {
    console.log('[Tech] Page hide');
  },

  onUnload() {
    console.log('[Tech] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '技术架构 - 智驭苍穹·守路安澜',
      '/pages/tech/tech',
      '/images/1.jpg'
    );
  },

  // ============ 用户交互 ============

  // 选择层级
  selectLayer(e) {
    const layer = parseInt(e.currentTarget.dataset.layer);
    this.setData({ activeLayer: layer });
    app.vibrateShort();
  },

  // 查看组件详情
  viewComponentDetail(e) {
    const layerIndex = e.currentTarget.dataset.layer;
    const compIndex = e.currentTarget.dataset.component;
    const component = this.data.layerDetails[layerIndex].components[compIndex];
    
    app.vibrateShort();
    app.showToast(component.name, 'none');
  },

  // 查看LoongClaw引擎
  viewLoongClaw() {
    app.vibrateShort();
    app.navigateTo('/pages/openclaw/openclaw');
  },

  // 查看无人机详情
  viewUAV() {
    app.vibrateShort();
    app.navigateTo('/pages/uav/uav');
  },

  // 切换详情显示
  toggleDetail() {
    this.setData({ showDetail: !this.data.showDetail });
    app.vibrateShort();
  },

  // 查看技术文档
  viewDocs() {
    app.vibrateShort();
    app.showToast('技术文档即将上线', 'none');
  },

  // 查看架构图
  viewArchitecture() {
    app.vibrateShort();
    app.previewImage(['/images/1.jpg']);
  }
});
