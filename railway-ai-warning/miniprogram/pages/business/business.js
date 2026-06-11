/**
 * 商业模式页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多商业内容和交互功能
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeLevel: 1,
    activeTab: 0,
    showCalculator: false,
    
    // 商业模式层级
    levels: [
      {
        id: 1,
        name: '第一级：硬件装备',
        shortName: '硬件',
        desc: '无人机系统销售',
        icon: '🛩️',
        color: '#FF6B6B',
        gradient: 'linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%)',
        details: [
          { label: '产品', value: 'Y3垂起固定翼无人机集群' },
          { label: '定价', value: '80-150万/套' },
          { label: '目标客户', value: '铁路局、工务段' },
          { label: '市场规模', value: '50亿/年' }
        ],
        features: [
          '全套无人机系统',
          '载荷设备配套',
          '培训与技术支持',
          '售后维护服务'
        ],
        revenue: '硬件销售利润30%'
      },
      {
        id: 2,
        name: '第二级：SaaS订阅',
        shortName: 'SaaS',
        desc: '预警平台服务',
        icon: '☁️',
        color: '#4ECDC4',
        gradient: 'linear-gradient(135deg, #4ECDC4 0%, #7EDDD7 100%)',
        details: [
          { label: '产品', value: 'LoongClaw预警云平台' },
          { label: '定价', value: '20-50万/年/线路' },
          { label: '目标客户', value: '铁路局、地铁公司' },
          { label: '市场规模', value: '100亿/年' }
        ],
        features: [
          '实时预警服务',
          '数据分析报告',
          '7×24技术支持',
          '定期系统升级'
        ],
        revenue: '订阅收入，毛利率70%'
      },
      {
        id: 3,
        name: '第三级：数据运营',
        shortName: '数据',
        desc: 'API与增值服务',
        icon: '📊',
        color: '#45B7D1',
        gradient: 'linear-gradient(135deg, #45B7D1 0%, #7ACDE0 100%)',
        details: [
          { label: '产品', value: '风险数据API、保险服务' },
          { label: '定价', value: '按调用量/保单抽成' },
          { label: '目标客户', value: '保险公司、物流企业' },
          { label: '市场规模', value: '200亿/年' }
        ],
        features: [
          '数据API接口',
          '风险评估服务',
          '保险精算支持',
          '行业分析报告'
        ],
        revenue: '数据服务，毛利率85%'
      }
    ],
    
    // 市场规模
    marketSize: {
      tam: { value: '350亿', label: '总市场(TAM)' },
      sam: { value: '150亿', label: '可服务市场(SAM)' },
      som: { value: '5亿', label: '目标市场(SOM)' }
    },
    
    // 目标客户
    customers: [
      { 
        icon: '🚂', 
        name: '铁路局', 
        desc: '18个铁路局集团，核心客户', 
        tag: '核心', 
        tagColor: '#FF4D4F',
        primary: true 
      },
      { 
        icon: '🚇', 
        name: '地铁公司', 
        desc: '50+城市地铁运营公司', 
        tag: '重要', 
        tagColor: '#FF9500',
        primary: false 
      },
      { 
        icon: '🏛️', 
        name: '政府部门', 
        desc: '应急管理、气象部门', 
        tag: '拓展', 
        tagColor: '#165DFF',
        primary: false 
      },
      { 
        icon: '🛡️', 
        name: '保险公司', 
        desc: '铁路保险、灾害保险', 
        tag: '潜在', 
        tagColor: '#7B61FF',
        primary: false 
      }
    ],
    
    // 竞争优势
    advantages: [
      { 
        number: '01', 
        title: '技术领先', 
        desc: 'LoongClaw引擎精度领先行业15%以上',
        icon: '🔬'
      },
      { 
        number: '02', 
        title: '端到端方案', 
        desc: '硬件+软件+服务一体化交付',
        icon: '🔗'
      },
      { 
        number: '03', 
        title: '行业认证', 
        desc: '通过铁路行业权威检测认证',
        icon: '📜'
      },
      { 
        number: '04', 
        title: '团队优势', 
        desc: '兰大大气科学+计算机跨学科团队',
        icon: '🎓'
      }
    ],
    
    // 发展路线图
    roadmap: [
      { 
        year: '2024', 
        title: '产品验证期', 
        desc: '完成3个铁路局试点部署，验证产品可靠性',
        milestones: ['兰州铁路局试点', '产品认证通过', '首批客户签约'],
        status: '进行中'
      },
      { 
        year: '2025', 
        title: '市场拓展期', 
        desc: '覆盖10个铁路局，实现营收5000万',
        milestones: ['覆盖10个铁路局', 'SaaS订阅上线', '营收5000万'],
        status: '规划中'
      },
      { 
        year: '2026', 
        title: '规模化期', 
        desc: '全国推广，拓展海外市场，营收2亿',
        milestones: ['全国铁路覆盖', '海外市场拓展', '营收2亿'],
        status: '规划中'
      }
    ],
    
    // 定价方案
    pricing: [
      {
        name: '基础版',
        price: '20万/年',
        period: '每线路',
        features: [
          '基础预警服务',
          '标准数据报告',
          '工作日技术支持',
          '季度系统升级'
        ],
        recommended: false
      },
      {
        name: '专业版',
        price: '35万/年',
        period: '每线路',
        features: [
          '高级预警服务',
          '定制数据报告',
          '7×24技术支持',
          '月度系统升级',
          '专属客户经理'
        ],
        recommended: true
      },
      {
        name: '企业版',
        price: '定制',
        period: '面议',
        features: [
          '全功能服务',
          '私有化部署',
          '专属技术团队',
          '实时系统升级',
          'API接口开放'
        ],
        recommended: false
      }
    ],
    
    // 计算器
    calculator: {
      lines: 1,
      level: 'professional',
      result: 35
    }
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Business] Page loaded', options);
  },

  onReady() {
    console.log('[Business] Page ready');
  },

  onShow() {
    console.log('[Business] Page show');
  },

  onHide() {
    console.log('[Business] Page hide');
  },

  onUnload() {
    console.log('[Business] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '商业模式 - 智驭苍穹·守路安澜',
      '/pages/business/business',
      '/images/3.jpg'
    );
  },

  // ============ 用户交互 ============

  // 返回上一页
  goBack() {
    app.vibrateShort();
    wx.navigateBack({ delta: 1, fail: () => {
      app.switchTab('/pages/home/home');
    }});
  },

  // 选择层级
  selectLevel(e) {
    const level = parseInt(e.currentTarget.dataset.level);
    this.setData({ activeLevel: level });
    app.vibrateShort();
  },

  // 切换Tab
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeTab: index });
    app.vibrateShort();
  },

  // 查看团队
  viewTeam() {
    app.vibrateShort();
    app.navigateTo('/pages/team/team');
  },

  // 查看客户详情
  viewCustomerDetail(e) {
    const index = e.currentTarget.dataset.index;
    const customer = this.data.customers[index];
    
    app.vibrateShort();
    app.showToast(customer.name, 'none');
  },

  // 查看路线图详情
  viewRoadmapDetail(e) {
    const index = e.currentTarget.dataset.index;
    const roadmap = this.data.roadmap[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: `${roadmap.year} ${roadmap.title}`,
      content: `${roadmap.desc}\n\n里程碑：\n${roadmap.milestones.join('\n')}`,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 选择定价方案
  selectPricing(e) {
    const index = e.currentTarget.dataset.index;
    const pricing = this.data.pricing[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: pricing.name,
      content: `${pricing.price}/${pricing.period}\n\n包含功能：\n${pricing.features.join('\n')}`,
      confirmText: '立即咨询',
      success: (res) => {
        if (res.confirm) {
          app.switchTab('/pages/contact/contact');
        }
      }
    });
  },

  // 切换计算器
  toggleCalculator() {
    this.setData({ showCalculator: !this.data.showCalculator });
    app.vibrateShort();
  },

  // 计算器线路数变化
  onLinesChange(e) {
    const lines = parseInt(e.detail.value) || 1;
    this.setData({
      'calculator.lines': lines
    });
    this.calculatePrice();
  },

  // 计算器级别变化
  onLevelChange(e) {
    const level = e.currentTarget.dataset.level;
    this.setData({
      'calculator.level': level
    });
    this.calculatePrice();
  },

  // 计算价格
  calculatePrice() {
    const { lines, level } = this.data.calculator;
    const priceMap = {
      basic: 20,
      professional: 35,
      enterprise: 50
    };
    const result = lines * priceMap[level];
    this.setData({ 'calculator.result': result });
  },

  // 联系咨询
  contactConsult() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  }
});
