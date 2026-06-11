/**
 * 成果验证页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多成果数据和展示
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeTab: 0,
    showChart: false,
    
    // 核心指标
    metrics: [
      { 
        name: '强降水命中率', 
        value: '0.82', 
        trend: '+15%', 
        barWidth: 82,
        icon: '',
        description: '相比传统方法提升15个百分点'
      },
      { 
        name: '空报率', 
        value: '0.18', 
        trend: '-35%', 
        barWidth: 18,
        icon: '',
        description: '误报率大幅降低'
      },
      { 
        name: '灾害回溯吻合度', 
        value: '76.5%', 
        trend: '+12%', 
        barWidth: 76.5,
        icon: '',
        description: '历史灾害事件吻合度'
      },
      { 
        name: 'TS评分', 
        value: '0.71', 
        trend: '+20%', 
        barWidth: 71,
        icon: '',
        description: '综合预报评分'
      }
    ],
    
    // 对比数据
    comparisonData: [
      { label: '命中率', traditional: 0.67, openclaw: 0.82, unit: '' },
      { label: 'TS评分', traditional: 0.56, openclaw: 0.71, unit: '' },
      { label: '空报率', traditional: 0.28, openclaw: 0.18, unit: '' },
      { label: '响应时间', traditional: 45, openclaw: 5, unit: 'min' }
    ],
    
    // 实战案例
    cases: [
      {
        name: '2024年7月甘肃暴雨',
        date: '2024.07.15 - 2024.07.18',
        location: '甘肃兰州',
        icon: '',
        result: '成功预警',
        resultColor: '#00CC99',
        description: '提前6小时准确预警暴雨过程，成功避免列车停运事故',
        stats: [
          { value: '6h', label: '提前预警' },
          { value: '0.85', label: '预报命中率' },
          { value: '0', label: '伤亡事故' }
        ],
        images: [
          '/images/5.jpg',
          '/images/6.jpg'
        ]
      },
      {
        name: '2024年3月横风预警',
        date: '2024.03.22',
        location: '甘肃武威',
        icon: '',
        result: '成功预警',
        resultColor: '#00CC99',
        description: '准确预报强横风天气，及时发布限速指令',
        stats: [
          { value: '2h', label: '提前预警' },
          { value: '0.88', label: '风速预报精度' },
          { value: '3', label: '列车限速' }
        ],
        images: [
          '/images/1.jpg'
        ]
      },
      {
        name: '2024年1月冰雪预警',
        date: '2024.01.10',
        location: '甘肃张掖',
        icon: '',
        result: '成功预警',
        resultColor: '#00CC99',
        description: '提前预警道岔结冰风险，及时采取除冰措施',
        stats: [
          { value: '4h', label: '提前预警' },
          { value: '0.91', label: '结冰预报精度' },
          { value: '0', label: '延误车次' }
        ],
        images: [
          '/images/3.jpg'
        ]
      }
    ],
    
    // 荣誉资质
    honors: [
      { 
        icon: '', 
        title: '铁路行业认证', 
        desc: '通过中国铁路科学研究院权威检测',
        type: 'certificate',
        date: '2024.01'
      },
      { 
        icon: '', 
        title: '软件著作权', 
        desc: '获得3项核心软件著作权登记',
        type: 'copyright',
        date: '2023.12'
      },
      { 
        icon: '', 
        title: '学术论文', 
        desc: '发表SCI/EI论文5篇',
        type: 'paper',
        date: '2023.11'
      },
      { 
        icon: '', 
        title: '竞赛获奖', 
        desc: '挑战杯/互联网+省级金奖',
        type: 'medal',
        date: '2023.10'
      }
    ],
    
    // 合作单位
    partners: [
      { name: '兰州大学', logo: '', type: '高校' },
      { name: '兰州铁路局', logo: '', type: '铁路' },
      { name: '甘肃省气象局', logo: '', type: '气象' },
      { name: '铁科院', logo: '', type: '科研' }
    ],
    
    // 数据统计
    statistics: {
      serviceDays: 365,
      warningCount: 2856,
      accuracy: 98.5,
      satisfaction: 4.9
    }
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Achievement] Page loaded', options);
  },

  onReady() {
    console.log('[Achievement] Page ready');
  },

  onShow() {
    console.log('[Achievement] Page show');
  },

  onHide() {
    console.log('[Achievement] Page hide');
  },

  onUnload() {
    console.log('[Achievement] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '成果验证 - 智驭苍穹·守路安澜',
      '/pages/achievement/achievement',
      '/images/4.jpg'
    );
  },

  // ============ 用户交互 ============

  // 切换Tab
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeTab: index });
    app.vibrateShort();
  },

  // 查看商业模式
  viewBusiness() {
    app.vibrateShort();
    app.navigateTo('/pages/business/business');
  },

  // 查看案例详情
  viewCaseDetail(e) {
    const index = e.currentTarget.dataset.index;
    const caseItem = this.data.cases[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: caseItem.name,
      content: `${caseItem.date} · ${caseItem.location}\n\n${caseItem.description}\n\n结果：${caseItem.result}`,
      showCancel: false,
      confirmText: '查看详情'
    });
  },

  // 预览图片
  previewImage(e) {
    const urls = e.currentTarget.dataset.urls;
    const index = e.currentTarget.dataset.index || 0;
    
    app.previewImage(urls, index);
  },

  // 查看荣誉详情
  viewHonorDetail(e) {
    const index = e.currentTarget.dataset.index;
    const honor = this.data.honors[index];
    
    app.vibrateShort();
    app.showToast(`${honor.title} (${honor.date})`, 'none');
  },

  // 切换图表显示
  toggleChart() {
    this.setData({ showChart: !this.data.showChart });
    app.vibrateShort();
  },

  // 联系咨询
  contactConsult() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  }
});
