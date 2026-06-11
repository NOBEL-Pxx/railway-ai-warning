const app = getApp();

Page({
  data: {
    currentExpert: 0,
    activeScenario: 0,
    experts: [
      {
        id: 'ai',
        name: 'AI专家',
        shortName: 'AI',
        title: 'MambaSwin-UNet-STA',
        icon: '🧠',
        badge: '核心',
        color: 'blue',
        description: '基于深度学习的端到端降水预报模型，融合Mamba状态空间模型、Swin Transformer和时空注意力机制，实现高精度短临预报。',
        capabilities: [
          '时空特征自动提取',
          '长序列依赖建模',
          '多尺度特征融合',
          '端到端梯度优化'
        ],
        metric: { value: '0.82', label: '命中率' }
      },
      {
        id: 'physics',
        name: '物理专家',
        shortName: '物理',
        title: 'COTREC + WRF',
        icon: '🌍',
        badge: '传统',
        color: 'green',
        description: '基于物理过程的数值天气预报模型，利用大气运动方程和热力学原理，提供物理可解释的预报结果。',
        capabilities: [
          '大气动力学模拟',
          '云微物理过程',
          '地形效应刻画',
          '物理约束满足'
        ],
        metric: { value: '72h', label: '预报时效' }
      },
      {
        id: 'statistics',
        name: '统计专家',
        shortName: '统计',
        title: 'XGBoost Ensemble',
        icon: '📊',
        badge: '融合',
        color: 'orange',
        description: '基于机器学习的统计预报模型，整合历史数据规律和多源预报结果，提供稳健的融合预测。',
        capabilities: [
          '历史规律挖掘',
          '多源结果融合',
          '不确定性量化',
          '偏差自动订正'
        ],
        metric: { value: '0.15', label: 'TS评分' }
      },
      {
        id: 'llm',
        name: 'LLM专家',
        shortName: 'LLM',
        title: '大模型解释',
        icon: '💬',
        badge: '智能',
        color: 'purple',
        description: '基于大语言模型的风险解释与决策支持系统，将复杂气象数据转化为易懂的决策建议。',
        capabilities: [
          '自然语言解释',
          '风险等级评估',
          '决策建议生成',
          '多轮对话交互'
        ],
        metric: { value: '95%', label: '满意度' }
      }
    ],
    scenarios: [
      {
        name: '暴雨场景',
        weights: [
          { name: 'AI专家', value: 45, color: '#165DFF' },
          { name: '物理专家', value: 30, color: '#00CC99' },
          { name: '统计专家', value: 20, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      },
      {
        name: '大风场景',
        weights: [
          { name: 'AI专家', value: 35, color: '#165DFF' },
          { name: '物理专家', value: 40, color: '#00CC99' },
          { name: '统计专家', value: 20, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      },
      {
        name: '冰雪场景',
        weights: [
          { name: 'AI专家', value: 30, color: '#165DFF' },
          { name: '物理专家', value: 35, color: '#00CC99' },
          { name: '统计专家', value: 30, color: '#FF9500' },
          { name: 'LLM专家', value: 5, color: '#7B61FF' }
        ]
      }
    ]
  },

  onLoad(options) {
    console.log('LoongClaw page loaded', options);
  },

  onReady() {
    // 页面首次渲染完成
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
      'LoongClaw引擎 - 智驭苍穹・守路安澜',
      '/pages/openclaw/openclaw'
    );
  },

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

  // 查看成果验证
  viewAchievement() {
    app.vibrateShort();
    app.navigateTo('/pages/achievement/achievement');
  }
});