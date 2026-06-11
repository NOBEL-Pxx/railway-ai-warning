const app = getApp();

Page({
  data: {
    positioning: '空天地多模态铁路短临致灾风险孪生预警系统',
    coreValues: [
      { icon: '🎯', title: '精准预测', desc: 'TS评分提升15%以上', color: 'primary' },
      { icon: '⚡', title: '快速响应', desc: '分钟级预警发布', color: 'success' },
      { icon: '🔍', title: '全域覆盖', desc: '空天地一体化感知', color: 'warning' },
      { icon: '🧠', title: '智能决策', desc: 'AI辅助风险研判', color: 'secondary' }
    ],
    painPoints: [
      { icon: '👁️‍🗨️', title: '观测盲区', desc: '雷达遮挡、站点稀疏' },
      { icon: '📉', title: '预报盲区', desc: '精度不足、时效性差' },
      { icon: '⏱️', title: '决策盲区', desc: '响应滞后、信息孤岛' }
    ],
    solutions: [
      { title: '空天感知层', desc: '卫星+无人机+地面站多源数据采集' },
      { title: '边缘计算层', desc: '实时预处理与特征提取' },
      { title: '云端推演层', desc: 'LoongClaw混合专家智能预测' },
      { title: '孪生可视层', desc: '三维场景化风险展示' }
    ],
    advantages: [
      { number: '01', title: '独创LoongClaw引擎', desc: '动态路由混合专家系统，融合AI、物理、统计、LLM四大专家' },
      { number: '02', title: '垂起固定翼无人机', desc: 'Y3架构设计，机动补盲，分钟级部署，秒级数据回传' },
      { number: '03', title: '数字孪生可视化', desc: '三维场景化展示，直观呈现风险分布与演变趋势' },
      { number: '04', title: '端到端解决方案', desc: '从数据采集到预警发布，全流程自动化处理' }
    ],
    scenarios: [
      { title: '暴雨洪涝', desc: '铁路沿线积水监测预警', image: 'https://picsum.photos/400/300?random=rain' },
      { title: '山体滑坡', desc: '边坡稳定性实时评估', image: 'https://picsum.photos/400/300?random=landslide' },
      { title: '大风预警', desc: '横风监测与限速建议', image: 'https://picsum.photos/400/300?random=wind' },
      { title: '冰雪灾害', desc: '道岔结冰监测预警', image: 'https://picsum.photos/400/300?random=snow' }
    ]
  },

  onLoad(options) {
    console.log('Overview page loaded', options);
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

  onReachBottom() {
    // 上拉加载
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '项目概况 - 智驭苍穹・守路安澜',
      '/pages/overview/overview'
    );
  },

  // 导航到痛点页面
  navigateToPainPoints(e) {
    const index = e.currentTarget.dataset.index;
    app.vibrateShort();
    app.navigateTo('/pages/painpoints/painpoints');
  },

  // 查看技术架构
  viewTechDetail() {
    app.vibrateShort();
    app.navigateTo('/pages/tech/tech');
  },

  // 预约演示
  bookDemo() {
    app.vibrateShort();
    app.navigateTo('/pages/contact/contact');
  }
});