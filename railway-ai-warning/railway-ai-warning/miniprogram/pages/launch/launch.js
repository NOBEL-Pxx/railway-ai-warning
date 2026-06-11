const app = getApp();

Page({
  data: {
    showContent: false,
    fadeOut: false,
    loadingProgress: 0,
    loadingText: '系统初始化中...'
  },

  onLoad(options) {
    console.log('Launch page loaded', options);
    this.startLaunchSequence();
  },

  onReady() {
    // 页面准备就绪
  },

  onShow() {
    // 显示页面
  },

  onHide() {
    // 隐藏页面
  },

  onUnload() {
    // 页面卸载
    if (this.loadingTimer) {
      clearInterval(this.loadingTimer);
    }
  },

  // 启动序列
  startLaunchSequence() {
    // 第一步：显示内容
    setTimeout(() => {
      this.setData({ showContent: true });
      this.startLoading();
    }, 300);
  },

  // 加载进度
  startLoading() {
    const loadingTexts = [
      '系统初始化中...',
      '加载核心模块...',
      '连接云端数据...',
      '准备就绪'
    ];
    
    let progress = 0;
    let textIndex = 0;
    
    this.loadingTimer = setInterval(() => {
      progress += Math.random() * 15 + 5;
      
      if (progress >= 100) {
        progress = 100;
        clearInterval(this.loadingTimer);
        
        setTimeout(() => {
          this.enterHomePage();
        }, 500);
      }
      
      // 更新加载文本
      if (progress > 25 && textIndex === 0) {
        textIndex = 1;
      } else if (progress > 50 && textIndex === 1) {
        textIndex = 2;
      } else if (progress > 80 && textIndex === 2) {
        textIndex = 3;
      }
      
      this.setData({
        loadingProgress: progress,
        loadingText: loadingTexts[textIndex]
      });
    }, 200);
  },

  // 进入首页
  enterHomePage() {
    // 淡出动画
    this.setData({ fadeOut: true });
    
    // 震动反馈
    app.vibrateShort();
    
    // 延迟跳转
    setTimeout(() => {
      wx.switchTab({
        url: '/pages/home/home',
        success: () => {
          console.log('Navigated to home page');
        },
        fail: (err) => {
          console.error('Navigation failed:', err);
          // 备用跳转方式
          wx.redirectTo({
            url: '/pages/home/home'
          });
        }
      });
    }, 800);
  },

  // 跳过启动页（调试用）
  skipLaunch() {
    if (this.loadingTimer) {
      clearInterval(this.loadingTimer);
    }
    this.enterHomePage();
  },

  // 分享
  onShareAppMessage() {
    return app.onShareAppMessage();
  }
});