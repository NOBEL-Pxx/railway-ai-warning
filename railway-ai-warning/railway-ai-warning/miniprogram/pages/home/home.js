const app = getApp();

Page({
  data: {
    userInfo: null,
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    newsList: [
      {
        id: 1,
        title: '系统通过铁路行业权威认证',
        summary: 'LoongClaw引擎在多项指标上达到行业领先水平，获得专家一致好评...',
        image: 'https://picsum.photos/400/300?random=news1',
        date: '2024-01-15',
        tag: '认证'
      },
      {
        id: 2,
        title: '无人机集群完成首次实战演练',
        summary: 'Y3架构垂起固定翼无人机在复杂气象条件下完成巡检任务...',
        image: 'https://picsum.photos/400/300?random=news2',
        date: '2024-01-10',
        tag: '演练'
      },
      {
        id: 3,
        title: '与兰州铁路局签署合作协议',
        summary: '双方将在铁路防灾预警领域展开深度合作...',
        image: 'https://picsum.photos/400/300?random=news3',
        date: '2024-01-05',
        tag: '合作'
      }
    ]
  },

  onLoad(options) {
    console.log('Home page loaded', options);
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      });
    }
  },

  onReady() {
    // 页面首次渲染完成
  },

  onShow() {
    // 页面显示
    this.animateModules();
  },

  onHide() {
    // 页面隐藏
  },

  onUnload() {
    // 页面卸载
  },

  onPullDownRefresh() {
    // 下拉刷新
    setTimeout(() => {
      wx.stopPullDownRefresh();
      app.showToast('已刷新', 'success');
    }, 1000);
  },

  onReachBottom() {
    // 上拉加载更多
    console.log('Reach bottom');
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '智驭苍穹・守路安澜 - 铁路防灾AI预警系统',
      '/pages/home/home'
    );
  },

  onShareTimeline() {
    return {
      title: '智驭苍穹・守路安澜 - 铁路防灾AI预警系统',
      query: '',
      imageUrl: '/images/share_cover.png'
    };
  },

  // 模块动画
  animateModules() {
    const animation = wx.createAnimation({
      duration: 600,
      timingFunction: 'ease-out',
      delay: 100
    });
    
    animation.opacity(1).translateY(0).step();
    this.setData({
      moduleAnimation: animation.export()
    });
  },

  // 页面导航
  navigateTo(e) {
    const page = e.currentTarget.dataset.page;
    const urlMap = {
      'overview': '/pages/overview/overview',
      'tech': '/pages/tech/tech',
      'openclaw': '/pages/openclaw/openclaw',
      'uav': '/pages/uav/uav',
      'painpoints': '/pages/painpoints/painpoints',
      'achievement': '/pages/achievement/achievement',
      'business': '/pages/business/business',
      'team': '/pages/team/team',
      'vision': '/pages/vision/vision',
      'contact': '/pages/contact/contact'
    };
    
    const url = urlMap[page];
    if (url) {
      app.vibrateShort();
      app.navigateTo(url);
    }
  },

  // 预约演示
  bookDemo() {
    app.vibrateShort();
    app.navigateTo('/pages/contact/contact');
  },

  // 下载BP
  downloadBP() {
    app.vibrateShort();
    wx.showModal({
      title: '下载商业计划书',
      content: '是否下载完整版商业计划书？',
      confirmText: '下载',
      success: (res) => {
        if (res.confirm) {
          app.showLoading('下载中...');
          // 模拟下载
          setTimeout(() => {
            app.hideLoading();
            app.showToast('下载成功', 'success');
          }, 1500);
        }
      }
    });
  },

  // 查看更多新闻
  viewMoreNews() {
    app.showToast('更多动态即将上线', 'none');
  },

  // 查看新闻详情
  viewNewsDetail(e) {
    const id = e.currentTarget.dataset.id;
    app.vibrateShort();
    app.showToast(`查看新闻 ${id}`, 'none');
  },

  // 获取用户信息
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        });
        app.setGlobalData('userInfo', res.userInfo);
      }
    });
  },

  // 获取用户信息（旧版）
  getUserInfo(e) {
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    });
    app.setGlobalData('userInfo', e.detail.userInfo);
  }
});