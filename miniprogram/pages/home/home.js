/**
 * 首页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多交互功能和数据展示
 */

const app = getApp();

Page({
  data: {
    // 用户信息
    userInfo: null,
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    
    // 页面状态
    isRefreshing: false,
    isLoading: false,
    scrollTop: 0,
    
    // 公告数据
    announcement: {
      show: true,
      text: '系统已通过铁路行业权威认证，欢迎预约演示',
      type: 'success'
    },
    
    // Hero区域数据
    heroData: {
      title: '智驭苍穹·守路安澜',
      subtitle: '空天地多模态铁路短临致灾风险孪生预警系统',
      badge: 'AI智能预警',
      stats: [
        { value: '15%', label: 'TS评分提升', suffix: '+' },
        { value: '10', label: '分钟级预警', suffix: '<' },
        { value: '99.9%', label: '系统可用性', suffix: '' }
      ]
    },
    
    // 核心模块数据
    modules: [
      {
        id: 'overview',
        title: '项目概况',
        desc: '系统定位与核心价值',
        icon: '📋',
        gradient: 'blue',
        badge: '推荐'
      },
      {
        id: 'tech',
        title: '技术架构',
        desc: '四层架构技术体系',
        icon: '🔧',
        gradient: 'purple',
        badge: null
      },
      {
        id: 'openclaw',
        title: 'LoongClaw',
        desc: '混合专家智能引擎',
        icon: '🧠',
        gradient: 'primary',
        badge: '核心'
      },
      {
        id: 'uav',
        title: '空天感知',
        desc: '无人机集群系统',
        icon: '🚁',
        gradient: 'cyan',
        badge: null
      }
    ],
    
    // 快速入口数据
    quickEntries: [
      {
        id: 'painpoints',
        title: '行业痛点',
        icon: '⚠️',
        color: 'danger',
        badge: 3
      },
      {
        id: 'achievement',
        title: '成果验证',
        icon: '📊',
        color: 'success',
        badge: null
      },
      {
        id: 'business',
        title: '商业模式',
        icon: '💼',
        color: 'warning',
        badge: null
      },
      {
        id: 'team',
        title: '团队介绍',
        icon: '👥',
        color: 'secondary',
        badge: null
      },
      {
        id: 'vision',
        title: '发展愿景',
        icon: '🎯',
        color: 'info',
        badge: null
      },
      {
        id: 'contact',
        title: '联系我们',
        icon: '📞',
        color: 'contact',
        badge: null
      }
    ],
    
    // 新闻列表
    newsList: [
      {
        id: 1,
        title: '系统通过铁路行业权威认证',
        summary: 'LoongClaw引擎在多项指标上达到行业领先水平，获得专家一致好评。TS评分提升15%，预警响应时间缩短至10分钟以内。',
        image: '/images/1.jpg',
        date: '2024-01-15',
        tag: '认证',
        tagType: 'primary',
        views: 1256,
        likes: 89
      },
      {
        id: 2,
        title: '无人机集群完成首次实战演练',
        summary: 'Y3架构垂起固定翼无人机在复杂气象条件下完成巡检任务，数据回传成功率达99.5%。',
        image: '/images/2.jpg',
        date: '2024-01-10',
        tag: '演练',
        tagType: 'success',
        views: 986,
        likes: 67
      },
      {
        id: 3,
        title: '与兰州铁路局签署合作协议',
        summary: '双方将在铁路防灾预警领域展开深度合作，共同推进智慧铁路建设。',
        image: '/images/3.jpg',
        date: '2024-01-05',
        tag: '合作',
        tagType: 'warning',
        views: 754,
        likes: 45
      },
      {
        id: 4,
        title: '荣获挑战杯省级金奖',
        summary: '项目在全国大学生挑战杯竞赛中脱颖而出，荣获科技创新类省级金奖。',
        image: '/images/4.jpg',
        date: '2024-01-01',
        tag: '荣誉',
        tagType: 'secondary',
        views: 623,
        likes: 112
      }
    ],
    
    // 数据统计
    statistics: {
      show: true,
      items: [
        { label: '服务线路', value: '12', unit: '条', trend: '+3' },
        { label: '预警次数', value: '2,856', unit: '次', trend: '+156' },
        { label: '准确预警', value: '98.5', unit: '%', trend: '+2.3%' },
        { label: '客户满意度', value: '4.9', unit: '分', trend: '+0.2' }
      ]
    },
    
    // 合作伙伴
    partners: [
      { name: '兰州大学', logo: '' },
      { name: '兰州铁路局', logo: '' },
      { name: '甘肃省气象局', logo: '' },
      { name: '铁科院', logo: '' }
    ],
    
    // 动画状态
    animationData: {},
    moduleAnimation: {},
    newsAnimation: {}
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Home] Page loaded', options);
    
    // 检查是否支持获取用户资料
    if (wx.getUserProfile) {
      this.setData({ canIUseGetUserProfile: true });
    }
    
    // 加载缓存数据
    this.loadCachedData();
    
    // 初始化动画
    this.initAnimations();
  },

  onReady() {
    console.log('[Home] Page ready');
    // 执行入场动画
    this.playEntryAnimation();
  },

  onShow() {
    console.log('[Home] Page show');
    // 更新统计数据
    this.updateStatistics();
    
    // 检查公告
    this.checkAnnouncement();
  },

  onHide() {
    console.log('[Home] Page hide');
  },

  onUnload() {
    console.log('[Home] Page unload');
    // 清除定时器
    if (this.statisticsTimer) {
      clearInterval(this.statisticsTimer);
    }
  },

  // ============ 下拉刷新和上拉加载 ============

  onPullDownRefresh() {
    console.log('[Home] Pull down refresh');
    this.setData({ isRefreshing: true });
    
    // 模拟刷新数据
    setTimeout(() => {
      this.refreshData();
      wx.stopPullDownRefresh();
      this.setData({ isRefreshing: false });
      app.showToast('已刷新最新内容', 'success');
    }, 1500);
  },

  onReachBottom() {
    console.log('[Home] Reach bottom');
    // 可以加载更多新闻
    this.loadMoreNews();
  },

  onPageScroll(e) {
    this.setData({ scrollTop: e.scrollTop });
    
    // 导航栏背景透明度变化
    const opacity = Math.min(e.scrollTop / 200, 1);
    this.setNavBarOpacity(opacity);
  },

  // ============ 分享功能 ============

  onShareAppMessage() {
    return app.onShareAppMessage(
      '智驭苍穹·守路安澜 - 铁路防灾AI预警系统',
      '/pages/home/home',
      '/images/1.jpg'
    );
  },

  onShareTimeline() {
    return app.onShareTimeline(
      '智驭苍穹·守路安澜 - 铁路防灾AI预警系统',
      '/images/1.jpg'
    );
  },

  // ============ 数据加载 ============

  loadCachedData() {
    try {
      const cachedNews = app.getStorage('home_news');
      if (cachedNews) {
        this.setData({ newsList: cachedNews });
      }
    } catch (e) {
      console.error('[Home] Load cached data failed:', e);
    }
  },

  refreshData() {
    // 模拟刷新数据
    const updatedNews = this.data.newsList.map(news => ({
      ...news,
      views: news.views + Math.floor(Math.random() * 10)
    }));
    
    this.setData({ newsList: updatedNews });
    app.setStorage('home_news', updatedNews);
  },

  loadMoreNews() {
    if (this.data.isLoading) return;
    
    this.setData({ isLoading: true });
    
    // 模拟加载更多
    setTimeout(() => {
      const newNews = [
        {
          id: this.data.newsList.length + 1,
          title: '新功能上线：智能预警推送',
          summary: '新增智能预警推送功能，可根据用户偏好定制预警信息接收方式。',
          image: '/images/4.jpg',
          date: '2023-12-28',
          tag: '更新',
          tagType: 'info',
          views: 456,
          likes: 23
        }
      ];
      
      this.setData({
        newsList: [...this.data.newsList, ...newNews],
        isLoading: false
      });
    }, 1000);
  },

  // ============ 动画效果 ============

  initAnimations() {
    // 初始化动画对象
    this.moduleAnimation = app.createAnimation({
      duration: 600,
      timingFunction: 'ease-out',
      delay: 100
    });
    
    this.newsAnimation = app.createAnimation({
      duration: 500,
      timingFunction: 'ease-out'
    });
  },

  playEntryAnimation() {
    // 模块卡片动画
    const animation = app.createAnimation({
      duration: 600,
      timingFunction: 'ease-out',
      delay: 200
    });
    
    animation.opacity(1).translateY(0).step();
    this.setData({ moduleAnimation: animation.export() });
    
    // 快速入口动画
    const quickAnimation = app.createAnimation({
      duration: 500,
      timingFunction: 'ease-out',
      delay: 400
    });
    
    quickAnimation.opacity(1).scale(1).step();
    this.setData({ quickAnimation: quickAnimation.export() });
  },

  animateModules() {
    const animation = app.createAnimation({
      duration: 600,
      timingFunction: 'ease-out',
      delay: 100
    });
    
    animation.opacity(1).translateY(0).step();
    this.setData({ moduleAnimation: animation.export() });
  },

  setNavBarOpacity(opacity) {
    // 可以在这里动态设置导航栏样式
  },

  // ============ 用户交互 ============

  navigateTo(e) {
    const page = e.currentTarget.dataset.page;
    // tabBar 页面列表，必须用 switchTab
    const tabBarPages = ['tech', 'achievement', 'contact'];
    
    if (tabBarPages.includes(page)) {
      app.vibrateShort();
      app.switchTab('/pages/' + page + '/' + page);
      return;
    }
    
    const urlMap = {
      'overview': '/pages/overview/overview',
      'openclaw': '/pages/openclaw/openclaw',
      'uav': '/pages/uav/uav',
      'painpoints': '/pages/painpoints/painpoints',
      'business': '/pages/business/business',
      'team': '/pages/team/team',
      'vision': '/pages/vision/vision',
      'home': '/pages/home/home'
    };
    
    const url = urlMap[page];
    if (url) {
      app.vibrateShort();
      if (page === 'home') {
        app.switchTab(url);
      } else {
        app.navigateTo(url);
      }
    }
  },

  // 预约演示 - contact是tabBar页面，用switchTab
  bookDemo() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  },

  // 打开项目书PDF
  downloadBP() {
    app.vibrateShort();
    wx.showLoading({ title: '正在打开...' });
    
    const fs = wx.getFileSystemManager();
    const srcPath = '/项目书.pdf';
    const targetPath = `${wx.env.USER_DATA_PATH}/项目书.pdf`;
    
    try {
      fs.access(srcPath, () => {
        fs.copyFile({
          srcPath: srcPath,
          destPath: targetPath,
          success: () => {
            wx.openDocument({
              filePath: targetPath,
              fileType: 'pdf',
              showMenu: true,
              success: () => { wx.hideLoading(); },
              fail: (err) => {
                wx.hideLoading();
                console.error('[Home] Open document failed:', err);
                wx.showModal({
                  title: '打开失败',
                  content: '无法打开项目书，请尝试在微信中长按项目书按钮保存文件后查看',
                  showCancel: false
                });
              }
            });
          },
          fail: (err) => {
            wx.hideLoading();
            console.error('[Home] Copy file failed:', err);
            wx.showModal({
              title: '文件读取失败',
              content: '项目书文件暂不可用，请稍后重试',
              showCancel: false
            });
          }
        });
      }, () => {
        wx.hideLoading();
        wx.showModal({
          title: '文件不存在',
          content: '项目书PDF文件未找到，请联系开发者',
          showCancel: false
        });
      });
    } catch (e) {
      wx.hideLoading();
      console.error('[Home] downloadBP error:', e);
      wx.showModal({
        title: '打开失败',
        content: '发生未知错误，请稍后重试',
        showCancel: false
      });
    }
  },

  // 查看更多新闻
  viewMoreNews() {
    app.vibrateShort();
    app.switchTab('/pages/achievement/achievement');
  },

  // 查看新闻详情（弹窗显示详情，支持分享）
  viewNewsDetail(e) {
    const id = e.currentTarget.dataset.id;
    const news = this.data.newsList.find(n => n.id === id);
    
    app.vibrateShort();
    
    if (news) {
      // 增加浏览量
      const updatedNews = this.data.newsList.map(n => 
        n.id === id ? { ...n, views: n.views + 1 } : n
      );
      this.setData({ newsList: updatedNews });
      
      // 弹窗显示新闻详情
      wx.showModal({
        title: news.title,
        content: `${news.summary}\n\n📅 日期：${news.date}\n👁 浏览：${news.views}\n❤ 点赞：${news.likes}`,
        showCancel: true,
        cancelText: '关闭',
        confirmText: '分享',
        confirmColor: '#00D4FF',
        success: (res) => {
          if (res.confirm) {
            wx.showShareMenu({
              withShareTicket: true,
              menus: ['shareAppMessage', 'shareTimeline']
            });
            app.showToast('请点击右上角分享给好友', 'none');
          }
        }
      });
    }
  },

  // 点赞新闻
  likeNews(e) {
    const id = e.currentTarget.dataset.id;
    const updatedNews = this.data.newsList.map(news => 
      news.id === id ? { ...news, likes: news.likes + 1 } : news
    );
    
    this.setData({ newsList: updatedNews });
    app.vibrateShort();
    app.showToast('点赞成功', 'success');
  },

  // 关闭公告
  closeAnnouncement() {
    this.setData({
      'announcement.show': false
    });
    app.setStorage('announcement_closed', Date.now());
  },

  // 点击公告
  tapAnnouncement() {
    app.switchTab('/pages/achievement/achievement');
  },

  // ============ 用户信息 ============

  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        });
        app.setGlobalData('userInfo', res.userInfo);
        app.showToast('欢迎 ' + res.userInfo.nickName, 'success');
      },
      fail: () => {
        app.showToast('获取用户信息失败');
      }
    });
  },

  getUserInfo(e) {
    if (e.detail.userInfo) {
      this.setData({
        userInfo: e.detail.userInfo,
        hasUserInfo: true
      });
      app.setGlobalData('userInfo', e.detail.userInfo);
    }
  },

  // ============ 统计数据 ============

  updateStatistics() {
    // 模拟动态更新统计数据
    const items = this.data.statistics.items.map(item => ({
      ...item,
      value: this.animateNumber(item.value)
    }));
    
    this.setData({
      'statistics.items': items
    });
  },

  animateNumber(value) {
    // 简单的数字动画效果
    return value;
  },

  // ============ 辅助功能 ============

  checkAnnouncement() {
    const lastClosed = app.getStorage('announcement_closed');
    const now = Date.now();
    
    // 24小时内不重复显示
    if (lastClosed && now - lastClosed < 24 * 60 * 60 * 1000) {
      this.setData({
        'announcement.show': false
      });
    }
  },

  recordDownload(type) {
    // 记录下载行为
    console.log('[Home] Download recorded:', type);
  },

  // 预览图片
  previewImage(e) {
    const url = e.currentTarget.dataset.url;
    const urls = this.data.newsList.map(n => n.image);
    
    app.previewImage(urls, urls.indexOf(url));
  },

  // 拨打电话
  makePhoneCall() {
    app.makePhoneCall('400-888-9999');
  },

  // 复制联系方式
  copyContact(e) {
    const type = e.currentTarget.dataset.type;
    const content = type === 'email' ? 'business@railway-ai.com' : '400-888-9999';
    
    app.setClipboardData(content).then(() => {
      app.showToast('已复制到剪贴板', 'success');
    });
  },

  // 扫码功能
  scanCode() {
    app.scanCode().then(res => {
      console.log('[Home] Scan result:', res);
      app.showToast('扫码成功: ' + res.result);
    }).catch(() => {
      app.showToast('扫码取消');
    });
  },

  // 回到顶部
  scrollToTop() {
    app.pageScrollTo(0, 300);
  },

  // 页面滚动到指定位置
  scrollToSection(e) {
    const section = e.currentTarget.dataset.section;
    const query = wx.createSelectorQuery();
    
    query.select('.' + section + '-section').boundingClientRect();
    query.selectViewport().scrollOffset();
    query.exec(res => {
      if (res[0]) {
        app.pageScrollTo(res[0].top + res[1].scrollTop - 100, 300);
      }
    });
  }
});
