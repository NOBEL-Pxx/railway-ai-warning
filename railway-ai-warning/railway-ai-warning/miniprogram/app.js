App({
  globalData: {
    userInfo: null,
    systemInfo: null,
    isDarkMode: false,
    theme: 'light'
  },

  onLaunch(options) {
    console.log('App Launch', options);
    this.getSystemInfo();
    this.checkDarkMode();
    this.initCloud();
  },

  onShow(options) {
    console.log('App Show', options);
    this.checkDarkMode();
  },

  onHide() {
    console.log('App Hide');
  },

  onError(msg) {
    console.error('App Error:', msg);
  },

  onPageNotFound(res) {
    console.error('Page Not Found:', res);
    wx.redirectTo({
      url: '/pages/home/home'
    });
  },

  getSystemInfo() {
    try {
      const systemInfo = wx.getSystemInfoSync();
      this.globalData.systemInfo = systemInfo;
      console.log('System Info:', systemInfo);
    } catch (e) {
      console.error('Get system info failed:', e);
    }
  },

  checkDarkMode() {
    const systemInfo = this.globalData.systemInfo;
    if (systemInfo) {
      const isDarkMode = systemInfo.theme === 'dark';
      this.globalData.isDarkMode = isDarkMode;
      this.globalData.theme = isDarkMode ? 'dark' : 'light';
      this.applyTheme(isDarkMode);
    }
  },

  applyTheme(isDarkMode) {
    if (wx.setNavigationBarColor) {
      wx.setNavigationBarColor({
        frontColor: isDarkMode ? '#ffffff' : '#ffffff',
        backgroundColor: isDarkMode ? '#1C1C1E' : '#165DFF',
        animation: {
          duration: 300,
          timingFunc: 'easeIn'
        }
      });
    }
  },

  initCloud() {
    if (wx.cloud) {
      wx.cloud.init({
        env: 'railway-ai-warning-env',
        traceUser: true
      });
      console.log('Cloud initialized');
    } else {
      console.log('Cloud API not available');
    }
  },

  setGlobalData(key, value) {
    this.globalData[key] = value;
  },

  getGlobalData(key) {
    return this.globalData[key];
  },

  // 震动反馈
  vibrateShort() {
    if (wx.vibrateShort) {
      wx.vibrateShort({ type: 'light' });
    }
  },

  vibrateLong() {
    if (wx.vibrateLong) {
      wx.vibrateLong();
    }
  },

  // 分享功能
  onShareAppMessage(title, path, imageUrl) {
    return {
      title: title || '智驭苍穹・守路安澜 - 铁路防灾AI预警系统',
      path: path || '/pages/home/home',
      imageUrl: imageUrl || '/images/share_cover.png'
    };
  },

  // 页面跳转
  navigateTo(url) {
    wx.navigateTo({
      url: url,
      fail: () => {
        wx.redirectTo({ url });
      }
    });
  },

  switchTab(url) {
    wx.switchTab({ url });
  },

  // 显示提示
  showToast(title, icon = 'none', duration = 2000) {
    wx.showToast({
      title,
      icon,
      duration
    });
  },

  showLoading(title = '加载中...') {
    wx.showLoading({
      title,
      mask: true
    });
  },

  hideLoading() {
    wx.hideLoading();
  },

  showModal(title, content, confirmText = '确定', cancelText = '取消') {
    return new Promise((resolve) => {
      wx.showModal({
        title,
        content,
        confirmText,
        cancelText,
        success: (res) => {
          resolve(res.confirm);
        },
        fail: () => {
          resolve(false);
        }
      });
    });
  }
});