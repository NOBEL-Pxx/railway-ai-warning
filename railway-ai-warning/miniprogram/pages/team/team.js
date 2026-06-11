/**
 * 团队介绍页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多团队信息和交互功能
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeTab: 0,
    showDetail: false,
    
    // 项目负责人
    leader: {
      name: '彭小溪',
      role: '项目负责人 / 算法架构',
      avatar: '/images/avatar1.jpg',
      tags: ['大气科学', '机器学习', '萃英学院'],
      desc: '兰州大学萃英学院本科生，主攻大气科学与人工智能交叉研究方向，负责项目整体架构设计与核心算法开发。',
      achievements: [
        { num: '省级', label: '创新训练计划' },
        { num: '5000元', label: '项目经费' },
        { num: '2026.04-2027.04', label: '项目周期' }
      ],
      social: {
        email: 'pengxx@lzu.edu.cn'
      }
    },
    
    // 核心成员
    members: [
      {
        name: '文年平',
        role: '核心成员 / 系统开发',
        avatar: '/images/avatar2.jpg',
        tag: '计算机',
        tagColor: '#165DFF',
        desc: '负责小程序前端开发与系统集成测试，协助完成可视化模块与数据处理流程。',
        skills: ['微信小程序', 'JavaScript', '数据可视化'],
        experience: '全栈开发经验'
      }
    ],
    
    // 指导教师
    advisor: {
      name: '胡淑娟 教授',
      title: '兰州大学大气科学学院',
      avatar: '/images/avatar3.jpg',
      desc: '长期从事气象灾害预警研究，主持国家自然科学基金项目3项，发表高水平论文20余篇。',
      achievements: [
        { num: '20+', label: '论文发表' },
        { num: '3', label: '国家项目' },
        { num: '15年', label: '研究经验' }
      ],
      research: ['气象灾害预警', '短临预报', '风险评估']
    },
    
    // 合作伙伴
    partners: [
      { 
        logo: '', 
        name: '兰州大学', 
        desc: '技术支撑单位',
        type: '高校'
      },
      { 
        logo: '', 
        name: '兰州铁路局', 
        desc: '试点应用单位',
        type: '铁路'
      },
      { 
        logo: '', 
        name: '甘肃省气象局', 
        desc: '数据合作单位',
        type: '气象'
      },
      { 
        logo: '', 
        name: '铁科院', 
        desc: '检测认证单位',
        type: '科研'
      }
    ],
    
    // 团队文化
    culture: [
      {
        title: '创新',
        desc: '持续技术创新，引领行业发展',
        icon: ''
      },
      {
        title: '协作',
        desc: '跨学科团队协作，优势互补',
        icon: ''
      },
      {
        title: '责任',
        desc: '守护铁路安全，服务社会民生',
        icon: ''
      }
    ],
    
    // 招聘信息
    jobs: [
      {
        title: '算法工程师',
        department: '技术研发部',
        location: '兰州',
        requirements: ['硕士及以上学历', '深度学习经验', 'Python熟练'],
        salary: '15-25K'
      },
      {
        title: '前端工程师',
        department: '产品研发部',
        location: '兰州',
        requirements: ['本科及以上学历', 'Vue/React经验', '3年以上经验'],
        salary: '12-20K'
      },
      {
        title: '产品经理',
        department: '产品部',
        location: '兰州',
        requirements: ['本科及以上学历', 'B端产品经验', '铁路行业背景优先'],
        salary: '15-22K'
      }
    ]
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Team] Page loaded', options);
  },

  onReady() {
    console.log('[Team] Page ready');
  },

  onShow() {
    console.log('[Team] Page show');
  },

  onHide() {
    console.log('[Team] Page hide');
  },

  onUnload() {
    console.log('[Team] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '团队介绍 - 智驭苍穹·守路安澜',
      '/pages/team/team',
      '/images/share.jpg'
    );
  },

  // ============ 用户交互 ============

  // 切换Tab
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeTab: index });
    app.vibrateShort();
  },

  // 查看愿景
  viewVision() {
    app.vibrateShort();
    app.navigateTo('/pages/vision/vision');
  },

  // 查看成员详情
  viewMemberDetail(e) {
    const index = e.currentTarget.dataset.index;
    const member = this.data.members[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: member.name,
      content: `${member.role}\n\n${member.desc}\n\n技能：${member.skills.join('、')}\n经验：${member.experience}`,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 查看导师详情
  viewAdvisorDetail() {
    app.vibrateShort();
    
    const advisor = this.data.advisor;
    wx.showModal({
      title: advisor.name,
      content: `${advisor.title}\n\n${advisor.desc}\n\n研究方向：${advisor.research.join('、')}`,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 查看职位详情
  viewJobDetail(e) {
    const index = e.currentTarget.dataset.index;
    const job = this.data.jobs[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: job.title,
      content: `${job.department} · ${job.location}\n薪资：${job.salary}\n\n要求：\n${job.requirements.join('\n')}`,
      confirmText: '申请职位',
      success: (res) => {
        if (res.confirm) {
          app.switchTab('/pages/contact/contact');
        }
      }
    });
  },

  // 联系咨询
  contactConsult() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  }
});
