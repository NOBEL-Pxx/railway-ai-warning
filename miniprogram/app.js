/**
 * 智驭苍穹·守路安澜 - 应用入口
 * 铁路防灾AI预警系统小程序
 * 优化版 - 增加更多全局功能和工具方法
 */

App({
  // 全局数据存储
  globalData: {
    // 用户信息
    userInfo: null,
    userLocation: null,
    
    // 系统信息
    systemInfo: null,
    windowWidth: 375,
    windowHeight: 667,
    pixelRatio: 2,
    statusBarHeight: 44,
    
    // 主题设置
    isDarkMode: false,
    theme: 'light',
    
    // 应用状态
    isFirstLaunch: true,
    launchTime: null,
    networkType: 'unknown',
    
    // 缓存数据
    cache: {
      news: null,
      stats: null,
      lastUpdate: null
    },
    
    // 配置项
    config: {
      apiBaseUrl: 'https://api.railway-ai.com',
      cdnBaseUrl: 'https://cdn.railway-ai.com',
      maxCacheAge: 3600000, // 1小时
      enableAnalytics: true
    }
  },

  /**
   * 应用启动时执行
   */
  onLaunch(options) {
    console.log('[App] Launch', options);
    
    // 记录启动时间
    this.globalData.launchTime = Date.now();
    
    // 初始化各模块
    this.getSystemInfo();
    this.checkDarkMode();
    this.initCloud();
    this.checkNetwork();
    this.loadCacheData();
    
    // 检查是否首次启动
    this.checkFirstLaunch();
    
    // 初始化分析统计
    if (this.globalData.config.enableAnalytics) {
      this.initAnalytics(options);
    }
  },

  /**
   * 应用显示时执行
   */
  onShow(options) {
    console.log('[App] Show', options);
    this.checkDarkMode();
    this.checkNetwork();
    
    // 更新在线状态
    this.globalData.isOnline = true;
  },

  /**
   * 应用隐藏时执行
   */
  onHide() {
    console.log('[App] Hide');
    this.globalData.isOnline = false;
    this.saveCacheData();
  },

  /**
   * 应用出错时执行
   */
  onError(msg) {
    console.error('[App] Error:', msg);
    this.reportError(msg);
  },

  /**
   * 页面不存在时执行
   */
  onPageNotFound(res) {
    console.error('[App] Page Not Found:', res);
    wx.redirectTo({
      url: '/pages/home/home'
    });
  },

  /**
   * 获取系统信息
   */
  getSystemInfo() {
    try {
      const systemInfo = wx.getSystemInfoSync();
      this.globalData.systemInfo = systemInfo;
      this.globalData.windowWidth = systemInfo.windowWidth;
      this.globalData.windowHeight = systemInfo.windowHeight;
      this.globalData.pixelRatio = systemInfo.pixelRatio;
      this.globalData.statusBarHeight = systemInfo.statusBarHeight;
      
      console.log('[App] System Info:', {
        brand: systemInfo.brand,
        model: systemInfo.model,
        system: systemInfo.system,
        version: systemInfo.version,
        SDKVersion: systemInfo.SDKVersion,
        platform: systemInfo.platform
      });
    } catch (e) {
      console.error('[App] Get system info failed:', e);
    }
  },

  /**
   * 检查暗黑模式
   */
  checkDarkMode() {
    const systemInfo = this.globalData.systemInfo;
    if (systemInfo) {
      const isDarkMode = systemInfo.theme === 'dark';
      this.globalData.isDarkMode = isDarkMode;
      this.globalData.theme = isDarkMode ? 'dark' : 'light';
      this.applyTheme(isDarkMode);
    }
  },

  /**
   * 应用主题
   */
  applyTheme(isDarkMode) {
    if (wx.setNavigationBarColor) {
      wx.setNavigationBarColor({
        frontColor: '#ffffff',
        backgroundColor: isDarkMode ? '#1C1C1E' : '#165DFF',
        animation: {
          duration: 300,
          timingFunc: 'easeIn'
        }
      });
    }
    
    // 设置TabBar颜色
    if (wx.setTabBarStyle) {
      wx.setTabBarStyle({
        color: isDarkMode ? '#8E8E93' : '#86909C',
        selectedColor: '#165DFF',
        backgroundColor: isDarkMode ? '#1C1C1E' : '#FFFFFF',
        borderStyle: isDarkMode ? 'black' : 'white'
      });
    }
  },

  /**
   * 初始化云开发
   */
  initCloud() {
    if (wx.cloud) {
      try {
        wx.cloud.init({
          env: 'railway-ai-warning-env',
          traceUser: true
        });
        console.log('[App] Cloud initialized');
      } catch (e) {
        console.log('[App] Cloud init failed:', e);
      }
    } else {
      console.log('[App] Cloud API not available');
    }
  },

  /**
   * 检查网络状态
   */
  checkNetwork() {
    if (wx.getNetworkType) {
      wx.getNetworkType({
        success: (res) => {
          this.globalData.networkType = res.networkType;
          console.log('[App] Network type:', res.networkType);
        }
      });
    }
    
    // 监听网络变化
    if (wx.onNetworkStatusChange) {
      wx.onNetworkStatusChange((res) => {
        this.globalData.networkType = res.networkType;
        this.globalData.isConnected = res.isConnected;
        console.log('[App] Network changed:', res);
      });
    }
  },

  /**
   * 检查是否首次启动
   */
  checkFirstLaunch() {
    try {
      const hasLaunched = wx.getStorageSync('hasLaunched');
      this.globalData.isFirstLaunch = !hasLaunched;
      if (!hasLaunched) {
        wx.setStorageSync('hasLaunched', true);
      }
    } catch (e) {
      console.error('[App] Check first launch failed:', e);
    }
  },

  /**
   * 加载缓存数据
   */
  loadCacheData() {
    try {
      const cache = wx.getStorageSync('appCache');
      if (cache) {
        const now = Date.now();
        if (now - cache.timestamp < this.globalData.config.maxCacheAge) {
          this.globalData.cache = cache.data;
          console.log('[App] Cache loaded');
        }
      }
    } catch (e) {
      console.error('[App] Load cache failed:', e);
    }
  },

  /**
   * 保存缓存数据
   */
  saveCacheData() {
    try {
      wx.setStorageSync('appCache', {
        timestamp: Date.now(),
        data: this.globalData.cache
      });
    } catch (e) {
      console.error('[App] Save cache failed:', e);
    }
  },

  /**
   * 初始化分析统计
   */
  initAnalytics(options) {
    // 记录启动场景
    console.log('[Analytics] Launch scene:', options.scene);
    
    // 可以接入第三方统计服务
    if (wx.reportAnalytics) {
      wx.reportAnalytics('app_launch', {
        scene: options.scene,
        path: options.path
      });
    }
  },

  /**
   * 上报错误
   */
  reportError(msg) {
    if (wx.reportMonitor) {
      wx.reportMonitor('error', 1);
    }
    // 可以接入错误监控服务
  },

  // ============ 全局数据操作 ============

  /**
   * 设置全局数据
   */
  setGlobalData(key, value) {
    if (typeof key === 'object') {
      Object.assign(this.globalData, key);
    } else {
      this.globalData[key] = value;
    }
  },

  /**
   * 获取全局数据
   */
  getGlobalData(key) {
    return key ? this.globalData[key] : this.globalData;
  },

  // ============ 震动反馈 ============

  /**
   * 短震动
   */
  vibrateShort() {
    if (wx.vibrateShort) {
      wx.vibrateShort({ type: 'light' });
    }
  },

  /**
   * 中等震动
   */
  vibrateMedium() {
    if (wx.vibrateShort) {
      wx.vibrateShort({ type: 'medium' });
    }
  },

  /**
   * 长震动
   */
  vibrateLong() {
    if (wx.vibrateLong) {
      wx.vibrateLong();
    }
  },

  // ============ 分享功能 ============

  /**
   * 获取分享配置
   */
  onShareAppMessage(title, path, imageUrl) {
    return {
      title: title || '智驭苍穹·守路安澜 - 铁路防灾AI预警系统',
      path: path || '/pages/home/home',
      imageUrl: imageUrl || 'https://picsum.photos/500/400?random=share',
      success: () => {
        this.showToast('分享成功', 'success');
      }
    };
  },

  /**
   * 获取朋友圈分享配置
   */
  onShareTimeline(title, imageUrl) {
    return {
      title: title || '智驭苍穹·守路安澜 - 铁路防灾AI预警系统',
      query: '',
      imageUrl: imageUrl || 'https://picsum.photos/500/400?random=share'
    };
  },

  // ============ 页面导航 ============

  /**
   * 导航到新页面
   */
  navigateTo(url, params = {}) {
    const queryString = Object.keys(params).map(key => 
      `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`
    ).join('&');
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    
    wx.navigateTo({
      url: fullUrl,
      fail: () => {
        wx.redirectTo({ url: fullUrl });
      }
    });
  },

  /**
   * 重定向到页面
   */
  redirectTo(url, params = {}) {
    const queryString = Object.keys(params).map(key => 
      `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`
    ).join('&');
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    
    wx.redirectTo({ url: fullUrl });
  },

  /**
   * 切换Tab
   */
  switchTab(url) {
    wx.switchTab({ url });
  },

  /**
   * 返回上一页
   */
  navigateBack(delta = 1) {
    wx.navigateBack({ delta });
  },

  // ============ 提示显示 ============

  /**
   * 显示Toast
   */
  showToast(title, icon = 'none', duration = 2000, mask = false) {
    wx.showToast({
      title: String(title),
      icon,
      duration,
      mask
    });
  },

  /**
   * 显示成功提示
   */
  showSuccess(title, duration = 2000) {
    this.showToast(title, 'success', duration);
  },

  /**
   * 显示错误提示
   */
  showError(title, duration = 2000) {
    this.showToast(title, 'error', duration);
  },

  /**
   * 显示加载中
   */
  showLoading(title = '加载中...', mask = true) {
    wx.showLoading({
      title,
      mask
    });
  },

  /**
   * 隐藏加载中
   */
  hideLoading() {
    wx.hideLoading();
  },

  /**
   * 显示模态框
   */
  showModal(title, content, options = {}) {
    const { confirmText = '确定', cancelText = '取消', showCancel = true } = options;
    
    return new Promise((resolve) => {
      wx.showModal({
        title,
        content,
        confirmText,
        cancelText,
        showCancel,
        confirmColor: '#165DFF',
        success: (res) => {
          resolve(res.confirm);
        },
        fail: () => {
          resolve(false);
        }
      });
    });
  },

  /**
   * 显示操作菜单
   */
  showActionSheet(itemList) {
    return new Promise((resolve, reject) => {
      wx.showActionSheet({
        itemList,
        success: (res) => {
          resolve(res.tapIndex);
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  },

  // ============ 存储操作 ============

  /**
   * 设置存储
   */
  setStorage(key, data) {
    try {
      wx.setStorageSync(key, data);
      return true;
    } catch (e) {
      console.error('[App] Set storage failed:', e);
      return false;
    }
  },

  /**
   * 获取存储
   */
  getStorage(key, defaultValue = null) {
    try {
      return wx.getStorageSync(key) || defaultValue;
    } catch (e) {
      console.error('[App] Get storage failed:', e);
      return defaultValue;
    }
  },

  /**
   * 移除存储
   */
  removeStorage(key) {
    try {
      wx.removeStorageSync(key);
      return true;
    } catch (e) {
      console.error('[App] Remove storage failed:', e);
      return false;
    }
  },

  /**
   * 清空存储
   */
  clearStorage() {
    try {
      wx.clearStorageSync();
      return true;
    } catch (e) {
      console.error('[App] Clear storage failed:', e);
      return false;
    }
  },

  // ============ 网络请求 ============

  /**
   * 发起请求
   */
  request(options) {
    const { url, method = 'GET', data = {}, header = {}, timeout = 30000 } = options;
    
    return new Promise((resolve, reject) => {
      wx.request({
        url: url.startsWith('http') ? url : this.globalData.config.apiBaseUrl + url,
        method,
        data,
        header: {
          'Content-Type': 'application/json',
          ...header
        },
        timeout,
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(res.data);
          } else {
            reject(new Error(`HTTP ${res.statusCode}`));
          }
        },
        fail: reject
      });
    });
  },

  // ============ 下载功能 ============

  /**
   * 下载文件
   */
  downloadFile(url, options = {}) {
    const { fileName, showProgress = true } = options;
    
    if (showProgress) {
      this.showLoading('下载中...');
    }
    
    return new Promise((resolve, reject) => {
      const downloadTask = wx.downloadFile({
        url,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.tempFilePath);
          } else {
            reject(new Error(`Download failed: ${res.statusCode}`));
          }
        },
        fail: reject,
        complete: () => {
          if (showProgress) {
            this.hideLoading();
          }
        }
      });
      
      if (showProgress && downloadTask) {
        downloadTask.onProgressUpdate((res) => {
          console.log('[App] Download progress:', res.progress);
        });
      }
    });
  },

  // ============ 图片操作 ============

  /**
   * 预览图片
   */
  previewImage(urls, current = 0) {
    const urlList = Array.isArray(urls) ? urls : [urls];
    wx.previewImage({
      current: urlList[current],
      urls: urlList
    });
  },

  /**
   * 保存图片到相册
   */
  saveImageToPhotosAlbum(filePath) {
    return new Promise((resolve, reject) => {
      wx.saveImageToPhotosAlbum({
        filePath,
        success: resolve,
        fail: reject
      });
    });
  },

  // ============ 位置服务 ============

  /**
   * 获取位置
   */
  getLocation(options = {}) {
    const { type = 'wgs84', altitude = false, isHighAccuracy = false } = options;
    
    return new Promise((resolve, reject) => {
      wx.getLocation({
        type,
        altitude,
        isHighAccuracy,
        success: (res) => {
          this.globalData.userLocation = res;
          resolve(res);
        },
        fail: reject
      });
    });
  },

  /**
   * 打开位置
   */
  openLocation(latitude, longitude, name, address) {
    wx.openLocation({
      latitude,
      longitude,
      name,
      address,
      scale: 18
    });
  },

  // ============ 剪贴板 ============

  /**
   * 复制到剪贴板
   */
  setClipboardData(data) {
    return new Promise((resolve, reject) => {
      wx.setClipboardData({
        data: String(data),
        success: resolve,
        fail: reject
      });
    });
  },

  /**
   * 获取剪贴板数据
   */
  getClipboardData() {
    return new Promise((resolve, reject) => {
      wx.getClipboardData({
        success: (res) => resolve(res.data),
        fail: reject
      });
    });
  },

  // ============ 电话功能 ============

  /**
   * 拨打电话
   */
  makePhoneCall(phoneNumber) {
    wx.makePhoneCall({
      phoneNumber: String(phoneNumber)
    });
  },

  // ============ 扫码功能 ============

  /**
   * 扫码
   */
  scanCode(options = {}) {
    const { onlyFromCamera = false, scanType = ['qrCode', 'barCode'] } = options;
    
    return new Promise((resolve, reject) => {
      wx.scanCode({
        onlyFromCamera,
        scanType,
        success: resolve,
        fail: reject
      });
    });
  },

  // ============ 动画工具 ============

  /**
   * 创建动画
   */
  createAnimation(options = {}) {
    const defaultOptions = {
      duration: 400,
      timingFunction: 'ease-out',
      delay: 0,
      transformOrigin: '50% 50%'
    };
    
    return wx.createAnimation({ ...defaultOptions, ...options });
  },

  // ============ 页面滚动 ============

  /**
   * 页面滚动到指定位置
   */
  pageScrollTo(scrollTop, duration = 300) {
    wx.pageScrollTo({
      scrollTop,
      duration
    });
  },

  // ============ 下拉刷新 ============

  /**
   * 开始下拉刷新
   */
  startPullDownRefresh() {
    wx.startPullDownRefresh();
  },

  /**
   * 停止下拉刷新
   */
  stopPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  // ============ 屏幕亮度 ============

  /**
   * 设置屏幕亮度
   */
  setScreenBrightness(value) {
    if (wx.setScreenBrightness) {
      wx.setScreenBrightness({ value });
    }
  },

  /**
   * 获取屏幕亮度
   */
  getScreenBrightness() {
    return new Promise((resolve, reject) => {
      if (wx.getScreenBrightness) {
        wx.getScreenBrightness({
          success: (res) => resolve(res.value),
          fail: reject
        });
      } else {
        reject(new Error('API not supported'));
      }
    });
  },

  // ============ 屏幕常亮 ============

  /**
   * 设置屏幕常亮
   */
  setKeepScreenOn(keepScreenOn = true) {
    if (wx.setKeepScreenOn) {
      wx.setKeepScreenOn({ keepScreenOn });
    }
  },

  // ============ 工具方法 ============

  /**
   * 防抖函数
   */
  debounce(fn, delay = 300) {
    let timer = null;
    return function(...args) {
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => {
        fn.apply(this, args);
      }, delay);
    };
  },

  /**
   * 节流函数
   */
  throttle(fn, interval = 300) {
    let lastTime = 0;
    return function(...args) {
      const now = Date.now();
      if (now - lastTime >= interval) {
        lastTime = now;
        fn.apply(this, args);
      }
    };
  },

  /**
   * 格式化日期
   */
  formatDate(date, format = 'YYYY-MM-DD') {
    const d = date instanceof Date ? date : new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hour = String(d.getHours()).padStart(2, '0');
    const minute = String(d.getMinutes()).padStart(2, '0');
    const second = String(d.getSeconds()).padStart(2, '0');
    
    return format
      .replace('YYYY', year)
      .replace('MM', month)
      .replace('DD', day)
      .replace('HH', hour)
      .replace('mm', minute)
      .replace('ss', second);
  },

  /**
   * 格式化数字
   */
  formatNumber(num, decimals = 0) {
    if (num === null || num === undefined) return '-';
    const n = Number(num);
    if (isNaN(n)) return '-';
    return n.toFixed(decimals);
  },

  /**
   * 格式化文件大小
   */
  formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },

  /**
   * 深拷贝
   */
  deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj);
    if (obj instanceof Array) return obj.map(item => this.deepClone(item));
    if (obj instanceof Object) {
      const cloned = {};
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          cloned[key] = this.deepClone(obj[key]);
        }
      }
      return cloned;
    }
    return obj;
  },

  /**
   * 生成唯一ID
   */
  generateId(prefix = '') {
    return prefix + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  },

  /**
   * 随机范围
   */
  randomRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  },

  /**
   * 随机颜色
   */
  randomColor() {
    const colors = ['#165DFF', '#00CC99', '#FF9500', '#7B61FF', '#FF4D4F', '#00D6B9'];
    return colors[Math.floor(Math.random() * colors.length)];
  }
});
