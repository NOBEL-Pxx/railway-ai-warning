const app = getApp();

Page({
  data: {
    values: [
      { icon: '🛡️', title: '防灾减灾', desc: '提前预警，守护生命财产安全' },
      { icon: '🚄', title: '交通强国', desc: '保障铁路安全高效运营' },
      { icon: '🌍', title: '技术输出', desc: '一带一路，惠及全球铁路' }
    ],
    impacts: [
      { number: '1000+', title: '万公里铁路守护', desc: '覆盖全国主要铁路干线' },
      { number: '10万+', title: '列车安全护航', desc: '每日保障列车安全运行' },
      { number: '1亿+', title: '旅客平安出行', desc: '守护亿万旅客生命安全' },
      { number: '100亿', title: '经济损失避免', desc: '减少灾害造成的经济损失' }
    ],
    roadmap: [
      { year: '2024', title: '立足西北', desc: '完成兰州铁路局试点部署，验证产品可靠性' },
      { year: '2025', title: '辐射全国', desc: '覆盖全国重点铁路干线，服务18个铁路局' },
      { year: '2027', title: '走向国际', desc: '服务一带一路沿线国家，输出中国技术' },
      { year: '2030', title: '全球领先', desc: '成为全球铁路防灾预警领域领导者' }
    ],
    mission: '以科技创新守护铁路安全，让人类出行更加安心',
    slogan: ['天有可测风云', '路有预知安澜']
  },

  onLoad(options) {
    console.log('Vision page loaded', options);
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
      '社会价值与愿景 - 智驭苍穹・守路安澜',
      '/pages/vision/vision'
    );
  },

  // 联系我们
  contactUs() {
    app.vibrateShort();
    app.navigateTo('/pages/contact/contact');
  }
});