/**
 * 联系我们页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多联系功能和交互
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeTab: 0,
    isSubmitting: false,
    
    // 表单数据
    form: {
      name: '',
      company: '',
      phone: '',
      email: '',
      type: 'demo',
      message: ''
    },
    
    // 表单验证
    isFormValid: false,
    formErrors: {
      name: '',
      phone: '',
      email: ''
    },
    
    // 咨询类型
    consultTypes: [
      { value: 'demo', label: '预约演示', icon: '' },
      { value: 'consult', label: '产品咨询', icon: '' },
      { value: 'cooperation', label: '商务合作', icon: '' },
      { value: 'job', label: '加入我们', icon: '' }
    ],
    
    // 联系信息
    contactInfo: {
      phone: '400-888-9999',
      email: 'business@railway-ai.com',
      address: '兰州市城关区兰州大学',
      workTime: '周一至周五 9:00-18:00',
      latitude: 36.0533,
      longitude: 103.8608
    },
    
    // 社交媒体
    socialMedia: [
      { 
        name: '微信公众号', 
        icon: '',
        account: '智驭苍穹',
        qrCode: '/images/5.jpg'
      },
      { 
        name: '企业微信', 
        icon: '',
        account: 'RailwayAI',
        qrCode: '/images/5.jpg'
      },
      { 
        name: '官方网站', 
        icon: '',
        account: 'www.railway-ai.com',
        url: 'https://www.railway-ai.com'
      }
    ],
    
    // 常见问题
    faqs: [
      {
        question: '系统支持哪些灾害类型预警？',
        answer: '目前支持暴雨洪涝、山体滑坡、大风预警、冰雪灾害等多种铁路常见灾害类型的预警。',
        expanded: false
      },
      {
        question: '预警响应时间是多少？',
        answer: '系统可实现分钟级预警响应，从数据采集到预警发布平均耗时不超过10分钟。',
        expanded: false
      },
      {
        question: '如何预约产品演示？',
        answer: '您可以通过本页面表单提交预约申请，或直接拨打客服电话400-888-9999。',
        expanded: false
      },
      {
        question: '是否支持私有化部署？',
        answer: '是的，我们提供企业版私有化部署方案，满足数据安全要求较高的客户需求。',
        expanded: false
      }
    ],
    
    // 提交成功
    submitSuccess: false
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[Contact] Page loaded', options);
    
    // 根据参数设置默认咨询类型
    if (options.type) {
      this.setData({
        'form.type': options.type
      });
    }
  },

  onReady() {
    console.log('[Contact] Page ready');
  },

  onShow() {
    console.log('[Contact] Page show');
  },

  onHide() {
    console.log('[Contact] Page hide');
  },

  onUnload() {
    console.log('[Contact] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '联系我们 - 智驭苍穹·守路安澜',
      '/pages/contact/contact',
      '/images/2.jpg'
    );
  },

  // ============ 表单处理 ============

  // 输入处理
  onInput(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail.value;
    
    this.setData({
      [`form.${field}`]: value
    }, () => {
      this.validateField(field, value);
      this.checkFormValid();
    });
  },

  // 验证单个字段
  validateField(field, value) {
    let error = '';
    
    switch (field) {
      case 'name':
        if (!value.trim()) {
          error = '请输入姓名';
        } else if (value.trim().length < 2) {
          error = '姓名至少2个字符';
        }
        break;
      case 'phone':
        if (!value.trim()) {
          error = '请输入手机号';
        } else if (!/^1[3-9]\d{9}$/.test(value)) {
          error = '请输入正确的手机号';
        }
        break;
      case 'email':
        if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          error = '请输入正确的邮箱';
        }
        break;
    }
    
    this.setData({
      [`formErrors.${field}`]: error
    });
    
    return !error;
  },

  // 选择类型
  selectType(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({
      'form.type': type
    });
    app.vibrateShort();
  },

  // 检查表单有效性
  checkFormValid() {
    const { name, phone } = this.data.form;
    const isValid = name.trim().length >= 2 && /^1[3-9]\d{9}$/.test(phone);
    
    this.setData({
      isFormValid: isValid
    });
    
    return isValid;
  },

  // 提交表单
  submitForm() {
    if (!this.data.isFormValid) {
      // 显示第一个错误
      const errors = this.data.formErrors;
      for (const field in errors) {
        if (errors[field]) {
          app.showToast(errors[field]);
          return;
        }
      }
      app.showToast('请填写必填项');
      return;
    }

    const { name, company, phone, email, type, message } = this.data.form;
    
    this.setData({ isSubmitting: true });
    app.showLoading('提交中...');
    
    // 模拟提交
    setTimeout(() => {
      app.hideLoading();
      this.setData({ isSubmitting: false });
      
      // 显示成功状态
      this.setData({ submitSuccess: true });
      
      // 重置表单
      setTimeout(() => {
        this.setData({
          form: {
            name: '',
            company: '',
            phone: '',
            email: '',
            type: 'demo',
            message: ''
          },
          isFormValid: false,
          submitSuccess: false
        });
        
        app.showToast('提交成功，我们会尽快联系您', 'success');
      }, 2000);
    }, 1500);
  },

  // ============ 联系方式 ============

  // 拨打电话
  makePhoneCall() {
    app.makePhoneCall(this.data.contactInfo.phone);
  },

  // 复制邮箱
  copyEmail() {
    app.setClipboardData(this.data.contactInfo.email).then(() => {
      app.showToast('邮箱已复制', 'success');
    });
  },

  // 打开位置
  openLocation() {
    const { latitude, longitude, address } = this.data.contactInfo;
    app.openLocation(latitude, longitude, '兰州大学', address);
  },

  // 复制地址
  copyAddress() {
    app.setClipboardData(this.data.contactInfo.address).then(() => {
      app.showToast('地址已复制', 'success');
    });
  },

  // ============ 下载功能 ============

  // 打开项目书PDF
  downloadBP() {
    wx.showLoading({ title: '正在打开...' });
    
    const fs = wx.getFileSystemManager();
    const targetPath = `${wx.env.USER_DATA_PATH}/项目书.pdf`;
    
    try {
      fs.copyFile('/项目书.pdf', targetPath, () => {
        wx.openDocument({
          filePath: targetPath,
          fileType: 'pdf',
          showMenu: true,
          success: () => { wx.hideLoading(); },
          fail: () => {
            wx.hideLoading();
            app.showToast('打开失败，请稍后重试', 'none');
          }
        });
      }, () => {
        wx.hideLoading();
        app.showToast('文件读取失败', 'none');
      });
    } catch (e) {
      wx.hideLoading();
      app.showToast('打开失败', 'none');
    }
  },

  // 下载产品手册
  downloadBrochure() {
    app.showLoading('准备下载...');
    
    setTimeout(() => {
      app.hideLoading();
      app.showToast('产品手册下载成功', 'success');
    }, 1000);
  },

  // ============ 社交功能 ============

  // 添加微信
  addWechat() {
    wx.showModal({
      title: '添加微信',
      content: '微信号：RailwayAI2024\n请备注单位名称',
      showCancel: false,
      confirmText: '知道了'
    });
  },

  // 关注公众号
  followOfficial() {
    app.showToast('公众号：智驭苍穹');
  },

  // 访问官网
  visitWebsite() {
    wx.showModal({
      title: '访问官网',
      content: '官网地址：www.railway-ai.com',
      confirmText: '复制',
      success: (res) => {
        if (res.confirm) {
          app.setClipboardData('www.railway-ai.com').then(() => {
            app.showToast('网址已复制', 'success');
          });
        }
      }
    });
  },

  // 预览二维码
  previewQRCode(e) {
    const index = e.currentTarget.dataset.index;
    const social = this.data.socialMedia[index];
    
    if (social.qrCode) {
      app.previewImage([social.qrCode]);
    }
  },

  // ============ FAQ ============

  // 展开/收起FAQ
  toggleFaq(e) {
    const index = e.currentTarget.dataset.index;
    const faqs = this.data.faqs.map((faq, i) => ({
      ...faq,
      expanded: i === index ? !faq.expanded : false
    }));
    
    this.setData({ faqs });
    app.vibrateShort();
  },

  // ============ 其他功能 ============

  // 切换Tab
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeTab: index });
    app.vibrateShort();
  },

  // 在线客服
  onlineService() {
    app.showToast('在线客服即将上线', 'none');
  },

  // 意见反馈
  feedback() {
    app.navigateTo('/pages/feedback/feedback');
  }
});
