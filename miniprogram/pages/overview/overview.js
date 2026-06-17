/**
 * 项目概况页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多展示内容和交互功能
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    isLoading: false,
    activeTab: 0,
    
    // 系统定位
    positioning: '空天地多模态铁路短临致灾风险孪生预警系统',
    positioningEn: 'Space-Air-Ground Multi-modal Railway Disaster Risk Digital Twin Warning System',
    
    // 核心价值
    coreValues: [
      { 
        icon: '🎯', 
        title: '精准预测',
        desc: 'TS评分提升15%以上',
        detail: '采用LoongClaw混合专家系统，融合AI、物理、统计、LLM四大专家模型',
        color: '#165DFF'
      },
      { 
        icon: '⚡', 
        title: '快速响应',
        desc: '分钟级预警发布',
        detail: '从数据采集到预警发布全流程自动化，响应时间缩短至10分钟以内',
        color: '#00CC99'
      },
      { 
        icon: '🌍', 
        title: '全域覆盖',
        desc: '空天地一体化感知',
        detail: '卫星遥感+无人机集群+地面站网，实现铁路沿线全域实时监测',
        color: '#FF9500'
      },
      { 
        icon: '🧠', 
        title: '智能决策',
        desc: 'AI辅助风险研判',
        detail: '基于大语言模型的风险解释与决策支持，提供智能化应对建议',
        color: '#7B61FF'
      }
    ],
    
    // 行业痛点
    painPoints: [
      { 
        icon: '👁', 
        title: '观测盲区', 
        desc: '雷达遮挡、站点稀疏',
        detail: '传统气象观测网络存在覆盖盲区，难以获取铁路沿线精细化气象数据',
        stat: '30%盲区率',
        solution: '无人机机动补盲'
      },
      { 
        icon: '📊', 
        title: '预报盲区', 
        desc: '精度不足、时效性差',
        detail: '传统数值预报模型空间分辨率低，难以满足铁路短临预警需求',
        stat: '2h延迟',
        solution: 'AI实时推演'
      },
      { 
        icon: '⏳', 
        title: '决策盲区', 
        desc: '响应滞后、信息孤岛',
        detail: '预警信息传递链条长，各部门协同效率低，错失最佳处置时机',
        stat: '45min响应',
        solution: '一体化平台'
      }
    ],
    
    // 解决方案
    solutions: [
      { 
        title: '空天感知层', 
        desc: '卫星+无人机+地面站多源数据采集',
        icon: '📡',
        features: ['卫星遥感', '无人机集群', '地面站网', '物联网传感器'],
        color: '#165DFF'
      },
      { 
        title: '边缘计算层', 
        desc: '实时预处理与特征提取',
        icon: '💾',
        features: ['数据预处理', '特征提取', '数据融合', '边缘缓存'],
        color: '#00D6B9'
      },
      { 
        title: '云端推演层', 
        desc: 'LoongClaw混合专家智能预测',
        icon: '🤖',
        features: ['LoongClaw引擎', 'AI专家', '物理专家', 'LLM专家'],
        color: '#7B61FF'
      },
      { 
        title: '孪生可视层', 
        desc: '三维场景化风险展示',
        icon: '🔮',
        features: ['三维场景', '风险可视化', '预警推送', '决策支持'],
        color: '#FF9500'
      }
    ],
    
    // 核心优势
    advantages: [
      { 
        number: '01', 
        title: '独创LoongClaw引擎', 
        desc: '动态路由混合专家系统，融合AI、物理、统计、LLM四大专家',
        icon: '🏆',
        highlight: true
      },
      { 
        number: '02', 
        title: '垂起固定翼无人机', 
        desc: 'Y3架构设计，机动补盲，分钟级部署，秒级数据回传',
        icon: '🚁',
        highlight: false
      },
      { 
        number: '03', 
        title: '数字孪生可视化', 
        desc: '三维场景化展示，直观呈现风险分布与演变趋势',
        icon: '🎨',
        highlight: false
      },
      { 
        number: '04', 
        title: '端到端解决方案', 
        desc: '从数据采集到预警发布，全流程自动化处理',
        icon: '🔗',
        highlight: false
      }
    ],
    
    // 应用场景
    scenarios: [
      { 
        title: '暴雨洪涝', 
        desc: '铁路沿线积水监测预警',
        image: '/images/5.jpg',
        stats: { accuracy: '92%', response: '8min' }
      },
      { 
        title: '山体滑坡', 
        desc: '边坡稳定性实时评估',
        image: '/images/2.jpg',
        stats: { accuracy: '88%', response: '10min' }
      },
      { 
        title: '大风预警', 
        desc: '横风监测与限速建议',
        image: '/images/1.jpg',
        stats: { accuracy: '95%', response: '5min' }
      },
      { 
        title: '冰雪灾害', 
        desc: '道岔结冰监测预警',
        image: '/images/3.jpg',
        stats: { accuracy: '90%', response: '12min' }
      }
    ],
    
    // 统计数据
    stats: [
      { value: '15%', label: 'TS评分提升', trend: '+', icon: '📈' },
      { value: '<10min', label: '预警响应时间', trend: '-', icon: '⏱' },
      { value: '99.9%', label: '系统可用性', trend: '+', icon: '🛡' },
      { value: '4层', label: '技术架构', trend: '', icon: '🏗' }
    ],
    
    // 发展历程
    milestones: [
      { year: '2022', title: '项目启动', desc: '组建跨学科研发团队' },
      { year: '2023', title: '技术突破', desc: 'LoongClaw引擎研发成功' },
      { year: '2024', title: '试点应用', desc: '兰州铁路局试点部署' },
      { year: '2025', title: '规模推广', desc: '全国铁路网络覆盖' }
    ],
    
    // 动画状态
    animationData: {}
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Overview] Page loaded', options);
    this.loadData();
    this.initAnimations();
  },

  onReady() {
    console.log('[Overview] Page ready');
    this.playEntryAnimation();
  },

  onShow() {
    console.log('[Overview] Page show');
  },

  onHide() {
    console.log('[Overview] Page hide');
  },

  onUnload() {
    console.log('[Overview] Page unload');
  },

  onPullDownRefresh() {
    setTimeout(() => {
      wx.stopPullDownRefresh();
      app.showToast('已刷新', 'success');
    }, 500);
  },

  onReachBottom() {
    // 上拉加载
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '项目概况 - 智驭苍穹·守路安澜',
      '/pages/overview/overview',
      '/images/1.jpg'
    );
  },

  // ============ 数据加载 ============

  loadData() {
    console.log('[Overview] Loading data...');
    // 模拟数据加载
  },

  // ============ 动画效果 ============

  initAnimations() {
    // 初始化动画
  },

  playEntryAnimation() {
    // 入场动画
    const animation = app.createAnimation({
      duration: 600,
      timingFunction: 'ease-out',
      delay: 100
    });
    
    animation.opacity(1).translateY(0).step();
    this.setData({ animationData: animation.export() });
  },

  // ============ 用户交互 ============

  // 切换Tab
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeTab: index });
    app.vibrateShort();
  },

  // 导航到痛点页面
  navigateToPainPoints(e) {
    const index = e.currentTarget.dataset.index;
    app.vibrateShort();
    
    const item = this.data.painPoints[index];
    app.showToast(`查看${item.title}`, 'none');
    
    setTimeout(() => {
      app.navigateTo('/pages/painpoints/painpoints', { index });
    }, 300);
  },

  // 查看技术架构
  viewTechDetail() {
    app.vibrateShort();
    app.switchTab('/pages/tech/tech');
  },

  // 查看解决方案详情
  viewSolutionDetail(e) {
    const index = e.currentTarget.dataset.index;
    const solution = this.data.solutions[index];
    
    app.vibrateShort();
    app.showModal(
      solution.title,
      solution.desc + '\n\n核心功能：' + solution.features.join('、'),
      { confirmText: '了解更多', showCancel: true }
    ).then(confirm => {
      if (confirm) {
        app.switchTab('/pages/tech/tech');
      }
    });
  },

  // 查看优势详情
  viewAdvantageDetail(e) {
    const index = e.currentTarget.dataset.index;
    const advantage = this.data.advantages[index];
    
    app.vibrateShort();
    app.showToast(advantage.title, 'none');
  },

  // 预约演示 - contact是tabBar页面，用switchTab
  bookDemo() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  },

  // 返回上一页
  goBack() {
    app.vibrateShort();
    wx.navigateBack({ delta: 1, fail: () => {
      app.switchTab('/pages/home/home');
    }});
  },

  // 预览图片
  previewImage(e) {
    const urls = this.data.scenarios.map(s => s.image);
    const current = e.currentTarget.dataset.src;
    
    app.previewImage(urls, urls.indexOf(current));
  },

  // 查看场景详情
  viewScenarioDetail(e) {
    const index = e.currentTarget.dataset.index;
    const scenario = this.data.scenarios[index];
    
    app.vibrateShort();
    app.showModal(
      scenario.title,
      `${scenario.desc}\n\n准确率：${scenario.stats.accuracy}\n响应时间：${scenario.stats.response}`,
      { confirmText: '查看案例', showCancel: true }
    );
  },

  // 滚动到指定区域
  scrollToSection(e) {
    const section = e.currentTarget.dataset.section;
    const query = wx.createSelectorQuery();
    
    query.select('.' + section + '-section').boundingClientRect();
    query.selectViewport().scrollOffset();
    query.exec(res => {
      if (res[0]) {
        app.pageScrollTo(res[0].top + res[1].scrollTop - 100, 300);
      }
    });
  }
});
