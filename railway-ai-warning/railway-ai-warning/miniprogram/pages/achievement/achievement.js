const app = getApp();

Page({
  data: {
    metrics: [
      { name: '强降水命中率', value: '0.82', trend: '+15%', barWidth: 82 },
      { name: '空报率', value: '0.18', trend: '-35%', barWidth: 18 },
      { name: '灾害回溯吻合度', value: '76.5%', trend: '+12%', barWidth: 76.5 },
      { name: 'TS评分', value: '0.71', trend: '+20%', barWidth: 71 }
    ],
    comparisonData: [
      { label: '命中率', traditional: 0.67, openclaw: 0.82 },
      { label: 'TS评分', traditional: 0.56, openclaw: 0.71 },
      { label: '空报率', traditional: 0.28, openclaw: 0.18 },
      { label: '响应时间', traditional: 45, openclaw: 5 }
    ],
    cases: [
      {
        name: '2024年7月甘肃暴雨',
        date: '2024.07.15 - 2024.07.18',
        icon: '🌧️',
        result: '成功预警',
        stats: [
          { value: '6h', label: '提前预警' },
          { value: '0.85', label: '预报命中率' },
          { value: '0', label: '伤亡事故' }
        ]
      },
      {
        name: '2024年3月横风预警',
        date: '2024.03.22',
        icon: '💨',
        result: '成功预警',
        stats: [
          { value: '2h', label: '提前预警' },
          { value: '0.88', label: '风速预报精度' },
          { value: '3', label: '列车限速' }
        ]
      }
    ],
    honors: [
      { icon: '🏆', title: '铁路行业认证', desc: '通过中国铁路科学研究院权威检测' },
      { icon: '📜', title: '软件著作权', desc: '获得3项核心软件著作权登记' },
      { icon: '🔬', title: '学术论文', desc: '发表SCI/EI论文5篇' },
      { icon: '🏅', title: '竞赛获奖', desc: '挑战杯/互联网+省级金奖' }
    ]
  },

  onLoad(options) {
    console.log('Achievement page loaded', options);
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
      '成果验证 - 智驭苍穹・守路安澜',
      '/pages/achievement/achievement'
    );
  },

  // 查看商业模式
  viewBusiness() {
    app.vibrateShort();
    app.navigateTo('/pages/business/business');
  }
});