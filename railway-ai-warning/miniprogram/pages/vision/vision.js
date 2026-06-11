/**
 * 愿景页 - 智驭苍穹·守路安澜
 * 优化版 - 展示项目发展愿景和规划
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeSection: 0,
    
    // 愿景宣言
    vision: {
      title: '让每一列火车都安全抵达',
      subtitle: 'Vision 2030',
      description: '成为全球领先的铁路防灾预警解决方案提供商，用AI技术守护每一条铁路线路的安全。',
      image: '/images/1.jpg'
    },
    
    // 使命
    mission: {
      title: '我们的使命',
      items: [
        {
          icon: '',
          title: '守护安全',
          desc: '用科技力量守护铁路安全，保护人民生命财产安全'
        },
        {
          icon: '',
          title: '技术创新',
          desc: '持续投入研发，推动铁路防灾预警技术进步'
        },
        {
          icon: '',
          title: '服务社会',
          desc: '让先进技术惠及更多铁路线路和乘客'
        }
      ]
    },
    
    // 核心价值观
    values: [
      {
        title: '安全至上',
        desc: '将安全作为一切工作的首要目标',
        icon: '',
        color: '#FF4D4F'
      },
      {
        title: '创新驱动',
        desc: '持续创新，引领行业技术发展',
        icon: '',
        color: '#165DFF'
      },
      {
        title: '合作共赢',
        desc: '与合作伙伴共同成长，创造价值',
        icon: '',
        color: '#00CC99'
      },
      {
        title: '追求卓越',
        desc: '精益求精，追求技术与服务的卓越',
        icon: '',
        color: '#FF9500'
      }
    ],
    
    // 战略规划
    strategies: [
      {
        phase: '近期',
        period: '2024-2025',
        title: '产品验证与市场拓展',
        goals: [
          '完成5个铁路局试点部署',
          '获得铁路行业权威认证',
          '实现年营收5000万元',
          '建立完善的售后服务体系'
        ],
        icon: ''
      },
      {
        phase: '中期',
        period: '2026-2028',
        title: '规模化与全国覆盖',
        goals: [
          '覆盖全国18个铁路局',
          '拓展地铁及城际铁路市场',
          '实现年营收2亿元',
          '建立行业技术标准'
        ],
        icon: ''
      },
      {
        phase: '远期',
        period: '2029-2030',
        title: '国际化与生态构建',
        goals: [
          '拓展海外市场，服务一带一路',
          '构建铁路安全生态系统',
          '实现年营收10亿元',
          '成为全球铁路安全领域领导者'
        ],
        icon: ''
      }
    ],
    
    // 发展里程碑
    milestones: [
      { year: '2022', event: '项目启动，组建核心团队', highlight: false },
      { year: '2023', event: 'LoongClaw引擎研发成功', highlight: true },
      { year: '2024', event: '首个试点项目落地', highlight: true },
      { year: '2025', event: '产品规模化推广', highlight: false },
      { year: '2026', event: '全国铁路网络覆盖', highlight: true },
      { year: '2028', event: '海外市场拓展', highlight: false },
      { year: '2030', event: '成为全球铁路安全领导者', highlight: true }
    ],
    
    // 社会责任
    socialResponsibility: {
      title: '社会责任',
      items: [
        {
          icon: '',
          title: '安全守护',
          desc: '守护铁路安全，保护人民生命财产安全'
        },
        {
          icon: '',
          title: '绿色发展',
          desc: '推动绿色技术应用，减少环境影响'
        },
        {
          icon: '',
          title: '人才培养',
          desc: '培养铁路安全领域专业人才'
        },
        {
          icon: '',
          title: '科技普惠',
          desc: '让先进技术惠及更多地区和人群'
        }
      ]
    },
    
    // 合作伙伴愿景
    partnerVision: {
      title: '携手共创未来',
      desc: '我们期待与更多合作伙伴携手，共同推动铁路安全事业的发展',
      partners: [
        { name: '铁路局', icon: '' },
        { name: '科研机构', icon: '' },
        { name: '高校', icon: '' },
        { name: '企业', icon: '' }
      ]
    }
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Vision] Page loaded', options);
  },

  onReady() {
    console.log('[Vision] Page ready');
  },

  onShow() {
    console.log('[Vision] Page show');
  },

  onHide() {
    console.log('[Vision] Page hide');
  },

  onUnload() {
    console.log('[Vision] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '发展愿景 - 智驭苍穹·守路安澜',
      '/pages/vision/vision',
      '/images/1.jpg'
    );
  },

  // ============ 用户交互 ============

  // 切换章节
  switchSection(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeSection: index });
    app.vibrateShort();
  },

  // 查看战略详情
  viewStrategyDetail(e) {
    const index = e.currentTarget.dataset.index;
    const strategy = this.data.strategies[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: `${strategy.phase}规划 (${strategy.period})`,
      content: `${strategy.title}\n\n目标：\n${strategy.goals.join('\n')}`,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 预览愿景图片
  previewVisionImage() {
    app.vibrateShort();
    app.previewImage([this.data.vision.image]);
  },

  // 联系合作
  contactCooperation() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  },

  // 了解更多
  learnMore() {
    app.vibrateShort();
    app.navigateTo('/pages/business/business');
  }
});
