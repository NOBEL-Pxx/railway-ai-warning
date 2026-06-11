/**
 * 行业痛点页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多案例和交互功能
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    expanded: {
      observation: false,
      forecast: false,
      decision: false
    },
    activeCase: 0,
    
    // 痛点详情
    painPointDetails: [
      {
        id: 'observation',
        title: '观测盲区',
        subtitle: '雷达遮挡、站点稀疏',
        icon: '',
        color: '#FF4D4F',
        description: '传统气象观测网络存在覆盖盲区，雷达信号受地形遮挡，地面站点分布稀疏，难以获取铁路沿线精细化气象数据。',
        impacts: [
          '暴雨中心位于雷达盲区，预警延迟45分钟',
          '山区气象数据缺失，无法准确评估风险',
          '极端天气监测能力不足'
        ],
        stats: { value: '30%', label: '盲区覆盖率' }
      },
      {
        id: 'forecast',
        title: '预报盲区',
        subtitle: '精度不足、时效性差',
        icon: '',
        color: '#FF9500',
        description: '传统数值预报模型空间分辨率低，难以满足铁路短临预警需求，预报时效性和精度均有待提升。',
        impacts: [
          '山洪暴发前2小时才发出预警',
          '短临预报精度低于70%',
          '空间分辨率仅达公里级'
        ],
        stats: { value: '2h', label: '预警延迟' }
      },
      {
        id: 'decision',
        title: '决策盲区',
        subtitle: '响应滞后、信息孤岛',
        icon: '',
        color: '#7B61FF',
        description: '预警信息传递链条长，各部门协同效率低，错失最佳处置时机，缺乏统一决策支持平台。',
        impacts: [
          '预警响应时间长达45分钟',
          '部门间信息传递效率低',
          '缺乏智能决策辅助工具'
        ],
        stats: { value: '45min', label: '响应时间' }
      }
    ],
    
    // 真实案例
    cases: [
      {
        name: '22·7甘肃暴雨',
        date: '2022年7月',
        location: '甘肃兰州',
        tag: '观测盲区',
        tagColor: '#FF4D4F',
        info: '暴雨中心位于雷达盲区，预警延迟45分钟，导致列车停运6小时。',
        image: '/images/6.jpg',
        impact: '列车停运6小时，经济损失1200万元',
        stats: [
          { value: '6h', label: '列车停运' },
          { value: '1200万', label: '经济损失' },
          { value: '3', label: '延误车次' }
        ],
        lesson: '传统观测网络存在盲区，需要补充机动观测手段',
        solution: '部署无人机集群，实现机动补盲'
      },
      {
        name: '25·8榆中山洪',
        date: '2023年8月',
        location: '甘肃榆中',
        tag: '预报盲区',
        tagColor: '#FF9500',
        info: '山洪暴发前2小时才发出预警，导致线路受损3公里。',
        image: '/images/2.jpg',
        impact: '线路受损3公里，修复耗时2周',
        stats: [
          { value: '2h', label: '预警时效' },
          { value: '3km', label: '线路受损' },
          { value: '2周', label: '修复时间' }
        ],
        lesson: '短临预报精度不足，需要提升预报时效性',
        solution: '采用AI实时推演，缩短预警时间'
      },
      {
        name: '24·3横风事故',
        date: '2024年3月',
        location: '甘肃武威',
        tag: '决策盲区',
        tagColor: '#7B61FF',
        info: '横风预警信息传递延迟，导致列车脱轨事故。',
        image: '/images/1.jpg',
        impact: '列车脱轨，中断行车12小时',
        stats: [
          { value: '45min', label: '响应时间' },
          { value: '12h', label: '中断时长' },
          { value: '1', label: '事故等级' }
        ],
        lesson: '预警响应链条长，需要一体化决策平台',
        solution: '构建端到端预警平台，实现分钟级响应'
      }
    ],
    
    // 解决方案对比
    comparisons: [
      {
        aspect: '观测覆盖',
        traditional: '固定站点，盲区30%',
        ourSolution: '空天地一体，盲区<5%',
        improvement: '提升6倍'
      },
      {
        aspect: '预报精度',
        traditional: 'TS评分0.56',
        ourSolution: 'TS评分0.71',
        improvement: '提升27%'
      },
      {
        aspect: '响应时间',
        traditional: '45分钟',
        ourSolution: '<10分钟',
        improvement: '缩短78%'
      },
      {
        aspect: '预警准确率',
        traditional: '67%',
        ourSolution: '82%',
        improvement: '提升22%'
      }
    ],
    
    // 导航栏高度
    statusBarHeight: 44,
    navBarHeight: 44,
    showBack: false
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[PainPoints] Page loaded', options);
    
    // 获取系统信息计算导航栏高度
    this.calculateNavBar();
    
    // 检查页面栈判断是否需要返回按钮
    const pages = getCurrentPages();
    this.setData({
      showBack: pages.length > 1
    });
    
    // 如果有指定展开的卡片
    if (options.expand && this.data.expanded.hasOwnProperty(options.expand)) {
      this.setData({
        [`expanded.${options.expand}`]: true
      });
    }
    
    // 如果有指定案例
    if (options.case) {
      this.setData({ activeCase: parseInt(options.case) });
    }
  },

  onReady() {
    console.log('[PainPoints] Page ready');
  },

  onShow() {
    console.log('[PainPoints] Page show');
  },

  onHide() {
    console.log('[PainPoints] Page hide');
  },

  onUnload() {
    console.log('[PainPoints] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '行业痛点 - 智驭苍穹·守路安澜',
      '/pages/painpoints/painpoints',
      '/images/1.jpg'
    );
  },

  // ============ 导航栏计算 ============

  calculateNavBar() {
    try {
      const systemInfo = wx.getSystemInfoSync();
      const menuButtonInfo = wx.getMenuButtonBoundingClientRect();
      
      const statusBarHeight = systemInfo.statusBarHeight || 44;
      const navBarHeight = (menuButtonInfo.top - systemInfo.statusBarHeight) * 2 + menuButtonInfo.height;
      
      this.setData({
        statusBarHeight: statusBarHeight,
        navBarHeight: navBarHeight || 44
      });
    } catch (e) {
      console.error('[PainPoints] Get system info failed', e);
      this.setData({
        statusBarHeight: 44,
        navBarHeight: 44
      });
    }
  },

  // ============ 用户交互 ============

  // 返回上一页
  navBack() {
    app.vibrateShort();
    wx.navigateBack({
      fail: () => {
        wx.switchTab({
          url: '/pages/home/home'
        });
      }
    });
  },

  // 展开/收起卡片
  expandCard(e) {
    const type = e.currentTarget.dataset.type;
    const currentState = this.data.expanded[type];
    
    // 关闭其他卡片（手风琴效果）
    const newExpanded = {
      observation: false,
      forecast: false,
      decision: false
    };
    
    // 切换当前卡片状态
    newExpanded[type] = !currentState;
    
    this.setData({ expanded: newExpanded });
    
    if (!currentState) {
      app.vibrateShort();
    }
  },

  // 切换案例
  switchCase(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeCase: index });
    app.vibrateShort();
  },

  // 查看解决方案
  viewSolution() {
    app.vibrateShort();
    app.switchTab('/pages/tech/tech');
  },

  // 预览图片
  previewImage(e) {
    const index = e.currentTarget.dataset.index;
    const urls = this.data.cases.map(c => c.image);
    
    app.previewImage(urls, index);
  },

  // 处理图片加载错误
  onImageError(e) {
    const index = e.currentTarget.dataset.index;
    console.error('[PainPoints] Image load error:', index);
  },

  // 查看案例详情
  viewCaseDetail(e) {
    const index = e.currentTarget.dataset.index;
    const caseItem = this.data.cases[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: caseItem.name,
      content: `${caseItem.date} · ${caseItem.location}\n\n${caseItem.info}\n\n影响：${caseItem.impact}\n\n教训：${caseItem.lesson}\n\n解决方案：${caseItem.solution}`,
      showCancel: false,
      confirmText: '了解解决方案',
      success: () => {
        app.switchTab('/pages/tech/tech');
      }
    });
  },

  // 展开对比详情
  expandComparison(e) {
    const index = e.currentTarget.dataset.index;
    const comparison = this.data.comparisons[index];
    
    app.vibrateShort();
    app.showToast(`${comparison.aspect}: ${comparison.improvement}`, 'none');
  },

  // 联系咨询
  contactConsult() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  }
});
