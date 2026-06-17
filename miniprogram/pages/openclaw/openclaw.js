/**
 * LoongClaw引擎页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多专家模型展示和交互功能
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    currentExpert: 0,
    activeScenario: 0,
    showArchitecture: false,
    
    // 专家模型
    experts: [
      {
        id: 'ai',
        name: 'AI专家',
        shortName: 'AI',
        title: 'MambaSwin-UNet-STA',
        icon: '🤖',
        badge: '核心',
        color: '#165DFF',
        gradient: 'linear-gradient(135deg, #165DFF 0%, #4B8BFF 100%)',
        description: '基于深度学习的端到端降水预报模型，融合Mamba状态空间模型、Swin Transformer和时空注意力机制，实现高精度短临预报。',
        capabilities: [
          '时空特征自动提取',
          '长序列依赖建模',
          '多尺度特征融合',
          '端到端梯度优化'
        ],
        techDetails: [
          { label: '模型架构', value: 'MambaSwin-UNet-STA' },
          { label: '参数量', value: '45M' },
          { label: '推理时间', value: '200ms' },
          { label: 'GPU显存', value: '8GB' }
        ],
        metric: { value: '0.82', label: '命中率' },
        advantages: [
          '端到端训练优化',
          '长时序建模能力强',
          '计算效率高'
        ]
      },
      {
        id: 'physics',
        name: '物理专家',
        shortName: '物理',
        title: 'COTREC + WRF',
        icon: '🌪️',
        badge: '传统',
        color: '#00CC99',
        gradient: 'linear-gradient(135deg, #00CC99 0%, #00D6B9 100%)',
        description: '基于物理过程的数值天气预报模型，利用大气运动方程和热力学原理，提供物理可解释的预报结果。',
        capabilities: [
          '大气动力学模拟',
          '云微物理过程',
          '地形效应刻画',
          '物理约束满足'
        ],
        techDetails: [
          { label: '预报模式', value: 'WRF 4.3' },
          { label: '分辨率', value: '3km' },
          { label: '预报时效', value: '72h' },
          { label: '更新频率', value: '6h' }
        ],
        metric: { value: '72h', label: '预报时效' },
        advantages: [
          '物理可解释性强',
          '长期预报稳定',
          '极端天气捕捉'
        ]
      },
      {
        id: 'statistics',
        name: '统计专家',
        shortName: '统计',
        title: 'XGBoost Ensemble',
        icon: '📊',
        badge: '融合',
        color: '#FF9500',
        gradient: 'linear-gradient(135deg, #FF9500 0%, #FFB800 100%)',
        description: '基于机器学习的统计预报模型，整合历史数据规律和多源预报结果，提供稳健的融合预测。',
        capabilities: [
          '历史规律挖掘',
          '多源结果融合',
          '不确定性量化',
          '偏差自动订正'
        ],
        techDetails: [
          { label: '算法', value: 'XGBoost' },
          { label: '特征数', value: '128' },
          { label: '训练样本', value: '10万+' },
          { label: '更新周期', value: '每日' }
        ],
        metric: { value: '0.15', label: 'TS评分' },
        advantages: [
          '融合多源信息',
          '不确定性量化',
          '偏差自动订正'
        ]
      },
      {
        id: 'llm',
        name: 'LLM专家',
        shortName: 'LLM',
        title: '大模型解释',
        icon: '💬',
        badge: '智能',
        color: '#7B61FF',
        gradient: 'linear-gradient(135deg, #7B61FF 0%, #9B8EFF 100%)',
        description: '基于大语言模型的风险解释与决策支持系统，将复杂气象数据转化为易懂的决策建议。',
        capabilities: [
          '自然语言解释',
          '风险等级评估',
          '决策建议生成',
          '多轮对话交互'
        ],
        techDetails: [
          { label: '模型', value: 'GPT-4' },
          { label: '上下文', value: '8K' },
          { label: '响应时间', value: '1s' },
          { label: '支持语言', value: '中英' }
        ],
        metric: { value: '95%', label: '满意度' },
        advantages: [
          '自然语言交互',
          '智能决策建议',
          '多语言支持'
        ]
      }
    ],
    
    // 场景权重
    scenarios: [
      {
        name: '暴雨场景',
        icon: '🌧️',
        description: '强降水预报场景',
        weights: [
          { name: 'AI专家', value: 45, color: '#165DFF' },
          { name: '物理专家', value: 30, color: '#00CC99' },
          { name: '统计专家', value: 20, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      },
      {
        name: '大风场景',
        icon: '💨',
        description: '横风预警场景',
        weights: [
          { name: 'AI专家', value: 35, color: '#165DFF' },
          { name: '物理专家', value: 40, color: '#00CC99' },
          { name: '统计专家', value: 20, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      },
      {
        name: '冰雪场景',
        icon: '❄️',
        description: '冰雪灾害预警场景',
        weights: [
          { name: 'AI专家', value: 30, color: '#165DFF' },
          { name: '物理专家', value: 35, color: '#00CC99' },
          { name: '统计专家', value: 30, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      },
      {
        name: '综合场景',
        icon: '🌐',
        description: '多灾种综合预警',
        weights: [
          { name: 'AI专家', value: 38, color: '#165DFF' },
          { name: '物理专家', value: 32, color: '#00CC99' },
          { name: '统计专家', value: 25, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      }
    ],
    
    // 核心优势
    coreAdvantages: [
      {
        title: '动态路由',
        desc: '根据场景自动调整专家权重',
        icon: '🔀'
      },
      {
        title: '智能融合',
        desc: '多专家结果智能融合输出',
        icon: '⚗️'
      },
      {
        title: '持续学习',
        desc: '在线学习不断优化模型',
        icon: '📚'
      },
      {
        title: '可解释性',
        desc: '提供预报结果解释说明',
        icon: '💡'
      }
    ],
    
    // 性能指标
    performanceMetrics: [
      { label: 'TS评分', value: '0.71', trend: '+15%', icon: '📈' },
      { label: '命中率', value: '82%', trend: '+12%', icon: '🎯' },
      { label: '空报率', value: '18%', trend: '-35%', icon: '📉' },
      { label: '响应时间', value: '<10min', trend: '-78%', icon: '⏱️' }
    ],
    
    // 架构图
    architectureImage: '/images/resources/moe_layer_arch.jpeg'
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[LoongClaw] Page loaded', options);
  },

  onReady() {
    console.log('[LoongClaw] Page ready');
  },

  onShow() {
    console.log('[LoongClaw] Page show');
  },

  onHide() {
    console.log('[LoongClaw] Page hide');
  },

  onUnload() {
    console.log('[LoongClaw] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      'LoongClaw引擎 - 智驭苍穹·守路安澜',
      '/pages/openclaw/openclaw',
      '/images/resources/moe_layer_arch.jpeg'
    );
  },

  // ============ 返回上一页 ============
  goBack() {
    app.vibrateShort();
    wx.navigateBack({ delta: 1, fail: () => {
      app.switchTab('/pages/home/home');
    }});
  },

  // ============ 用户交互 ============

  // 轮播切换
  onSwiperChange(e) {
    this.setData({
      currentExpert: e.detail.current
    });
  },

  // 切换专家
  switchExpert(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      currentExpert: index
    });
    app.vibrateShort();
  },

  // 选择场景
  selectScenario(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      activeScenario: index
    });
    app.vibrateShort();
  },

  // 查看专家详情
  viewExpertDetail(e) {
    const index = e.currentTarget.dataset.index;
    const expert = this.data.experts[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: expert.name,
      content: `${expert.title}\n\n${expert.description}\n\n核心能力：\n${expert.capabilities.join('\n')}`,
      showCancel: false,
      confirmText: '了解更多'
    });
  },

  // 查看成果验证
  viewAchievement() {
    app.vibrateShort();
    app.switchTab('/pages/achievement/achievement');
  },

  // 切换架构图显示
  toggleArchitecture() {
    this.setData({ showArchitecture: !this.data.showArchitecture });
    app.vibrateShort();
  },

  // 预览架构图
  previewArchitecture() {
    app.vibrateShort();
    app.previewImage([this.data.architectureImage]);
  },

  // 查看技术文档
  viewDocs() {
    app.vibrateShort();
    app.showToast('技术文档即将上线', 'none');
  },

  // 运行演示
  runDemo() {
    app.vibrateShort();
    app.showToast('演示功能开发中', 'none');
  }
});
