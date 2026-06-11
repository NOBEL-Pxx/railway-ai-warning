const app = getApp();

Page({
  data: {
    expanded: {
      observation: false,
      forecast: false,
      decision: false
    },
    cases: [
      {
        name: '22・7甘肃暴雨',
        tag: '观测盲区',
        info: '暴雨中心位于雷达盲区，预警延迟45分钟',
        image: 'https://picsum.photos/400/250?random=disaster1',
        stats: [
          { value: '6h', label: '列车停运' },
          { value: '1200万', label: '经济损失' }
        ]
      },
      {
        name: '25・8榆中山洪',
        tag: '预报盲区',
        info: '山洪暴发前2小时才发出预警',
        image: 'https://picsum.photos/400/250?random=disaster2',
        stats: [
          { value: '2h', label: '预警时效' },
          { value: '3km', label: '线路受损' }
        ]
      }
    ]
  },

  onLoad(options) {
    console.log('PainPoints page loaded', options);
    // 如果有指定展开的卡片
    if (options.expand) {
      this.setData({
        [`expanded.${options.expand}`]: true
      });
    }
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
      '行业痛点 - 智驭苍穹・守路安澜',
      '/pages/painpoints/painpoints'
    );
  },

  // 展开/收起卡片
  expandCard(e) {
    const type = e.currentTarget.dataset.type;
    const currentState = this.data.expanded[type];
    
    // 关闭其他卡片
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

  // 查看解决方案
  viewSolution() {
    app.vibrateShort();
    app.navigateTo('/pages/tech/tech');
  }
});