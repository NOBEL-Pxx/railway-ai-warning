const app = getApp();

Page({
  data: {
    activeLevel: 1,
    levels: [
      {
        id: 1,
        name: '第一级：硬件装备',
        desc: '无人机系统销售',
        icon: '🚀',
        color: '#FF6B6B',
        details: [
          { label: '产品', value: 'Y3垂起固定翼无人机集群' },
          { label: '定价', value: '80-150万/套' },
          { label: '目标客户', value: '铁路局、工务段' },
          { label: '市场规模', value: '50亿/年' }
        ]
      },
      {
        id: 2,
        name: '第二级：SaaS订阅',
        desc: '预警平台服务',
        icon: '☁️',
        color: '#4ECDC4',
        details: [
          { label: '产品', value: 'LoongClaw预警云平台' },
          { label: '定价', value: '20-50万/年/线路' },
          { label: '目标客户', value: '铁路局、地铁公司' },
          { label: '市场规模', value: '100亿/年' }
        ]
      },
      {
        id: 3,
        name: '第三级：数据运营',
        desc: 'API与增值服务',
        icon: '📊',
        color: '#45B7D1',
        details: [
          { label: '产品', value: '风险数据API、保险服务' },
          { label: '定价', value: '按调用量/保单抽成' },
          { label: '目标客户', value: '保险公司、物流企业' },
          { label: '市场规模', value: '200亿/年' }
        ]
      }
    ],
    marketSize: {
      tam: '350亿',
      sam: '150亿',
      som: '5亿'
    },
    customers: [
      { icon: '🚄', name: '铁路局', desc: '18个铁路局集团，核心客户', tag: '核心', primary: true },
      { icon: '🚇', name: '地铁公司', desc: '50+城市地铁运营公司', tag: '重要', primary: false },
      { icon: '🏛️', name: '政府部门', desc: '应急管理、气象部门', tag: '拓展', primary: false },
      { icon: '🏢', name: '保险公司', desc: '铁路保险、灾害保险', tag: '潜在', primary: false }
    ],
    advantages: [
      { number: '01', title: '技术领先', desc: 'LoongClaw引擎精度领先行业15%以上' },
      { number: '02', title: '端到端方案', desc: '硬件+软件+服务一体化交付' },
      { number: '03', title: '行业认证', desc: '通过铁路行业权威检测认证' },
      { number: '04', title: '团队优势', desc: '兰大大气科学+计算机跨学科团队' }
    ],
    roadmap: [
      { year: '2024', title: '产品验证期', desc: '完成3个铁路局试点部署，验证产品可靠性' },
      { year: '2025', title: '市场拓展期', desc: '覆盖10个铁路局，实现营收5000万' },
      { year: '2026', title: '规模化期', desc: '全国推广，拓展海外市场，营收2亿' }
    ]
  },

  onLoad(options) {
    console.log('Business page loaded', options);
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
      '商业模式 - 智驭苍穹・守路安澜',
      '/pages/business/business'
    );
  },

  // 选择层级
  selectLevel(e) {
    const level = parseInt(e.currentTarget.dataset.level);
    this.setData({ activeLevel: level });
    app.vibrateShort();
  },

  // 查看团队
  viewTeam() {
    app.vibrateShort();
    app.navigateTo('/pages/team/team');
  }
});