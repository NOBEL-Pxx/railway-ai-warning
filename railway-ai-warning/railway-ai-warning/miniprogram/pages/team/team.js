const app = getApp();

Page({
  data: {
    leader: {
      name: '彭小溪',
      role: '项目总负责人 / 算法架构',
      avatar: 'https://picsum.photos/200/200?random=leader',
      tags: ['大气科学', '机器学习'],
      desc: '兰州大学大气科学学院博士生，专注短临降水预报研究，发表SCI论文3篇，获挑战杯省级金奖。'
    },
    members: [
      {
        name: '张嘉策',
        role: '技术负责人',
        avatar: 'https://picsum.photos/150/150?random=member1',
        tag: '计算机',
        desc: '负责LoongClaw引擎开发与系统架构设计'
      },
      {
        name: '郝梦圆',
        role: '算法工程师',
        avatar: 'https://picsum.photos/150/150?random=member2',
        tag: '物理',
        desc: '负责物理专家模型与数值预报集成'
      },
      {
        name: '陈彦融',
        role: '硬件工程师',
        avatar: 'https://picsum.photos/150/150?random=member3',
        tag: '自动化',
        desc: '负责无人机系统设计与载荷集成'
      },
      {
        name: '文年平',
        role: '产品经理',
        avatar: 'https://picsum.photos/150/150?random=member4',
        tag: '管理',
        desc: '负责产品规划与用户需求分析'
      },
      {
        name: '任威豪',
        role: '前端工程师',
        avatar: 'https://picsum.photos/150/150?random=member5',
        tag: '计算机',
        desc: '负责可视化平台与小程序开发'
      }
    ],
    advisor: {
      name: '胡淑娟 教授',
      title: '兰州大学大气科学学院',
      avatar: 'https://picsum.photos/200/200?random=advisor',
      desc: '长期从事气象灾害预警研究，主持国家自然科学基金项目3项，发表高水平论文20余篇。',
      achievements: [
        { num: '20+', label: '论文发表' },
        { num: '3', label: '国家项目' },
        { num: '15年', label: '研究经验' }
      ]
    },
    partners: [
      { logo: '🏫', name: '兰州大学', desc: '技术支撑单位' },
      { logo: '🚄', name: '兰州铁路局', desc: '试点应用单位' },
      { logo: '🌤️', name: '甘肃省气象局', desc: '数据合作单位' },
      { logo: '🔬', name: '铁科院', desc: '检测认证单位' }
    ]
  },

  onLoad(options) {
    console.log('Team page loaded', options);
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
      '团队介绍 - 智驭苍穹・守路安澜',
      '/pages/team/team'
    );
  },

  // 查看愿景
  viewVision() {
    app.vibrateShort();
    app.navigateTo('/pages/vision/vision');
  }
});