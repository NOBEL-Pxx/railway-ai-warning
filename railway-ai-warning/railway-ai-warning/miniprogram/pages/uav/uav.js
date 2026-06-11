const app = getApp();

Page({
  data: {
    uavSpecs: {
      model: 'Y3',
      endurance: '120min',
      range: '50km',
      speed: '80km/h',
      payload: '2kg'
    },
    payloads: [
      { name: '多光谱相机', spec: '4K/60fps', image: 'https://picsum.photos/200/200?random=payload1' },
      { name: '红外热像仪', spec: '640×512', image: 'https://picsum.photos/200/200?random=payload2' },
      { name: '气象传感器', spec: '六要素', image: 'https://picsum.photos/200/200?random=payload3' },
      { name: '激光雷达', spec: '100m测距', image: 'https://picsum.photos/200/200?random=payload4' }
    ],
    scenarios: [
      { time: 'T+0min', title: '灾害预警触发', desc: '系统识别高风险区域，自动调度无人机' },
      { time: 'T+5min', title: '快速部署起飞', desc: '垂起设计，无需跑道准备，即刻升空' },
      { time: 'T+10min', title: '现场数据采集', desc: '多载荷同步工作，实时获取现场数据' },
      { time: 'T+15min', title: '数据回传分析', desc: '5G实时传输，云端AI即时分析' }
    ],
    fleetStats: {
      total: 12,
      standby: 8,
      rate: '98%'
    }
  },

  onLoad(options) {
    console.log('UAV page loaded', options);
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
      '空天感知平台 - 智驭苍穹・守路安澜',
      '/pages/uav/uav'
    );
  },

  // 查看技术方案
  viewTech() {
    app.vibrateShort();
    app.navigateTo('/pages/tech/tech');
  }
});