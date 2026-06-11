/**
 * 工具函数库
 */

// 格式化日期
const formatDate = (date, format = 'YYYY-MM-DD') => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hour = String(date.getHours()).padStart(2, '0');
  const minute = String(date.getMinutes()).padStart(2, '0');
  const second = String(date.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second);
};

// 格式化数字
const formatNumber = (num, decimals = 0) => {
  if (isNaN(num)) return '0';
  return Number(num).toFixed(decimals);
};

// 防抖函数
const debounce = (fn, delay = 300) => {
  let timer = null;
  return function (...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
};

// 节流函数
const throttle = (fn, interval = 300) => {
  let lastTime = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      fn.apply(this, args);
    }
  };
};

// 深拷贝
const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime());
  if (obj instanceof Array) return obj.map(item => deepClone(item));
  if (obj instanceof Object) {
    const cloned = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        cloned[key] = deepClone(obj[key]);
      }
    }
    return cloned;
  }
  return obj;
};

// 检查手机号格式
const isValidPhone = (phone) => {
  const reg = /^1[3-9]\d{9}$/;
  return reg.test(phone);
};

// 检查邮箱格式
const isValidEmail = (email) => {
  const reg = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;
  return reg.test(email);
};

// 生成唯一ID
const generateId = (prefix = 'id') => {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

// 存储本地数据
const setStorage = (key, data) => {
  try {
    wx.setStorageSync(key, data);
    return true;
  } catch (e) {
    console.error('Storage set error:', e);
    return false;
  }
};

// 获取本地数据
const getStorage = (key, defaultValue = null) => {
  try {
    const data = wx.getStorageSync(key);
    return data !== '' ? data : defaultValue;
  } catch (e) {
    console.error('Storage get error:', e);
    return defaultValue;
  }
};

// 移除本地数据
const removeStorage = (key) => {
  try {
    wx.removeStorageSync(key);
    return true;
  } catch (e) {
    console.error('Storage remove error:', e);
    return false;
  }
};

// 网络请求封装
const request = (options) => {
  return new Promise((resolve, reject) => {
    wx.request({
      ...options,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(new Error(`Request failed: ${res.statusCode}`));
        }
      },
      fail: reject
    });
  });
};

// 上传文件
const uploadFile = (options) => {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      ...options,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(new Error(`Upload failed: ${res.statusCode}`));
        }
      },
      fail: reject
    });
  });
};

// 下载文件
const downloadFile = (url) => {
  return new Promise((resolve, reject) => {
    wx.downloadFile({
      url,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.tempFilePath);
        } else {
          reject(new Error(`Download failed: ${res.statusCode}`));
        }
      },
      fail: reject
    });
  });
};

// 选择图片
const chooseImage = (options = {}) => {
  return new Promise((resolve, reject) => {
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      ...options,
      success: resolve,
      fail: reject
    });
  });
};

// 获取位置信息
const getLocation = (options = {}) => {
  return new Promise((resolve, reject) => {
    wx.getLocation({
      type: 'wgs84',
      ...options,
      success: resolve,
      fail: reject
    });
  });
};

// 扫码
const scanCode = (options = {}) => {
  return new Promise((resolve, reject) => {
    wx.scanCode({
      onlyFromCamera: false,
      ...options,
      success: resolve,
      fail: reject
    });
  });
};

module.exports = {
  formatDate,
  formatNumber,
  debounce,
  throttle,
  deepClone,
  isValidPhone,
  isValidEmail,
  generateId,
  setStorage,
  getStorage,
  removeStorage,
  request,
  uploadFile,
  downloadFile,
  chooseImage,
  getLocation,
  scanCode
};