/**
 * 启动页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多动画效果和加载功能
 */

const app = getApp();

// launch 页随机背景图池（每次加载随机不同，用academic自制图专属启动画面）
const LAUNCH_BG_IMAGES = [
  '/images/academic/radar_echo.png',
  '/images/academic/neural_arch.png',
  '/images/academic/hydrology_model.png',
  '/images/academic/uav_route.png',
  '/images/academic/risk_heatmap.png',
  '/images/academic/data_fusion.png',
  '/images/academic/forecast_score.png',
  '/images/academic/satellite_ir.jpg',
  '/images/academic/precip_timeseries.png',
  '/images/academic/digital_twin.png',
  '/images/academic/sensor_payload.png',
  '/images/academic/slope_analysis.png',
];

Page({
  data: {
    // 显示状态
    showContent: false,
    fadeOut: false,
    
    // 启动画面随机背景图
    launchBgImage: '',
    
    // 加载进度
    loadingProgress: 0,
    loadingText: '系统初始化中...',
    loadingPhase: 0,
    
    // 加载阶段文本
    loadingTexts: [
      '系统初始化中...',
      '加载核心模块...',
      '连接云端数据...',
      '同步配置信息...',
      '准备就绪'
    ],
    
    // 技术标签
    techTags: [
      { icon: '', text: 'AI智能' },
      { icon: '', text: '无人机' },
      { icon: '', text: '气象预警' },
      { icon: '', text: '数字孪生' }
    ],
    
    // 功能特性
    features: [
      { icon: '', text: '精准预测' },
      { icon: '', text: '快速响应' },
      { icon: '', text: '全域覆盖' }
    ],
    
    // 动画状态
    logoAnimation: {},
    tagAnimations: [],
    featureAnimations: []
  },

  // 定时器引用
  loadingTimer: null,
  animationTimer: null,

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Launch] Page loaded', options);
    
    // 随机选取启动画面图
    const idx = Math.floor(Math.random() * LAUNCH_BG_IMAGES.length);
    this.setData({ launchBgImage: LAUNCH_BG_IMAGES[idx] });
    
    // 预加载数据
    this.preloadData();
    
    // 启动加载序列
    this.startLaunchSequence();
  },

  onReady() {
    console.log('[Launch] Page ready');
  },

  onShow() {
    console.log('[Launch] Page show');
  },

  onHide() {
    console.log('[Launch] Page hide');
  },

  onUnload() {
    console.log('[Launch] Page unload');
    // 清除所有定时器
    this.clearTimers();
  },

  // ============ 启动序列 ============

  startLaunchSequence() {
    // 第一步：显示内容
    setTimeout(() => {
      this.setData({ showContent: true });
      this.playLogoAnimation();
      this.playTagAnimations();
      this.playFeatureAnimations();
    }, 300);
    
    // 第二步：开始加载
    setTimeout(() => {
      this.startLoading();
    }, 800);
  },

  // ============ 动画效果 ============

  playLogoAnimation() {
    const animation = app.createAnimation({
      duration: 1000,
      timingFunction: 'ease-out'
    });
    
    animation.scale(1).opacity(1).step();
    this.setData({ logoAnimation: animation.export() });
  },

  playTagAnimations() {
    const animations = [];
    
    this.data.techTags.forEach((_, index) => {
      setTimeout(() => {
        const animation = app.createAnimation({
          duration: 500,
          timingFunction: 'ease-out'
        });
        animation.opacity(1).translateY(0).step();
        
        const tagAnimations = [...this.data.tagAnimations];
        tagAnimations[index] = animation.export();
        this.setData({ tagAnimations });
      }, 600 + index * 150);
    });
  },

  playFeatureAnimations() {
    const animations = [];
    
    this.data.features.forEach((_, index) => {
      setTimeout(() => {
        const animation = app.createAnimation({
          duration: 500,
          timingFunction: 'ease-out'
        });
        animation.opacity(1).scale(1).step();
        
        const featureAnimations = [...this.data.featureAnimations];
        featureAnimations[index] = animation.export();
        this.setData({ featureAnimations });
      }, 1000 + index * 100);
    });
  },

  // ============ 加载进度 ============

  startLoading() {
    let progress = 0;
    let phase = 0;
    
    this.loadingTimer = setInterval(() => {
      // 随机增加进度
      const increment = Math.random() * 12 + 3;
      progress += increment;
      
      // 更新加载阶段
      const newPhase = Math.min(Math.floor(progress / 20), 4);
      if (newPhase !== phase) {
        phase = newPhase;
        this.setData({ loadingPhase: phase });
      }
      
      // 完成加载
      if (progress >= 100) {
        progress = 100;
        clearInterval(this.loadingTimer);
        this.loadingTimer = null;
        
        this.setData({
          loadingProgress: 100,
          loadingPhase: 4
        });
        
        // 延迟进入首页
        setTimeout(() => {
          this.enterHomePage();
        }, 600);
      }
      
      this.setData({
        loadingProgress: Math.floor(progress)
      });
    }, 180);
  },

  // ============ 页面跳转 ============

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
          console.log('[Launch] Navigated to home page');
        },
        fail: (err) => {
          console.error('[Launch] Navigation failed:', err);
          // 备用跳转方式
          wx.redirectTo({
            url: '/pages/home/home'
          });
        }
      });
    }, 800);
  },

  // ============ 数据预加载 ============

  preloadData() {
    // 预加载首页数据
    console.log('[Launch] Preloading data...');
    
    // 可以在这里预加载一些关键数据
    // 例如：配置信息、用户设置等
  },

  // ============ 跳过功能 ============

  skipLaunch() {
    // 清除加载定时器
    this.clearTimers();
    
    // 直接完成加载
    this.setData({
      loadingProgress: 100,
      loadingPhase: 4
    });
    
    setTimeout(() => {
      this.enterHomePage();
    }, 300);
  },

  // ============ 工具方法 ============

  clearTimers() {
    if (this.loadingTimer) {
      clearInterval(this.loadingTimer);
      this.loadingTimer = null;
    }
    if (this.animationTimer) {
      clearTimeout(this.animationTimer);
      this.animationTimer = null;
    }
  },

  // ============ 分享功能 ============

  onShareAppMessage() {
    return {
      title: '智驭苍穹·守路安澜',
      desc: '空天地多模态铁路短临致灾风险孪生预警系统',
      path: '/pages/home/home',
      imageUrl: '/images/1.jpg'
    };
  }
});
