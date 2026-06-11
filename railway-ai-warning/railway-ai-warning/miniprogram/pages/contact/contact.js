const app = getApp();

Page({
  data: {
    form: {
      name: '',
      company: '',
      phone: '',
      type: 'demo',
      message: ''
    },
    isFormValid: false,
    contactInfo: {
      phone: '400-888-9999',
      email: 'business@railway-ai.com',
      address: '兰州市城关区兰州大学'
    }
  },

  onLoad(options) {
    console.log('Contact page loaded', options);
  },

  onReady() {
    // 页面首次渲染完成
  },

  onShow() {
    // 页面显示
  },

  onHide() {
    // 页面隐藏
  },

  onUnload() {
    // 页面卸载
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '联系我们 - 智驭苍穹・守路安澜',
      '/pages/contact/contact'
    );
  },

  // 输入处理
  onInput(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail.value;
    this.setData({
      [`form.${field}`]: value
    }, () => {
      this.checkFormValid();
    });
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
    const { name, company, phone } = this.data.form;
    const isValid = name.trim() !== '' && company.trim() !== '' && phone.trim() !== '';
    this.setData({
      isFormValid: isValid
    });
  },

  // 提交表单
  submitForm() {
    if (!this.data.isFormValid) {
      app.showToast('请填写必填项');
      return;
    }

    const { name, company, phone, type, message } = this.data.form;
    
    app.showLoading('提交中...');
    
    // 模拟提交
    setTimeout(() => {
      app.hideLoading();
      
      wx.showModal({
        title: '提交成功',
        content: '感谢您的预约，我们的工作人员将在24小时内与您联系。',
        showCancel: false,
        success: () => {
          // 重置表单
          this.setData({
            form: {
              name: '',
              company: '',
              phone: '',
              type: 'demo',
              message: ''
            },
            isFormValid: false
          });
        }
      });
    }, 1500);
  },

  // 拨打电话
  makePhoneCall() {
    wx.makePhoneCall({
      phoneNumber: this.data.contactInfo.phone
    });
  },

  // 复制邮箱
  copyEmail() {
    wx.setClipboardData({
      data: this.data.contactInfo.email,
      success: () => {
        app.showToast('邮箱已复制', 'success');
      }
    });
  },

  // 打开位置
  openLocation() {
    wx.openLocation({
      latitude: 36.0533,
      longitude: 103.8608,
      name: '兰州大学',
      address: this.data.contactInfo.address
    });
  },

  // 下载BP
  downloadBP() {
    app.showLoading('准备下载...');
    setTimeout(() => {
      app.hideLoading();
      app.showToast('下载链接已发送');
    }, 1000);
  },

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
          wx.setClipboardData({
            data: 'www.railway-ai.com',
            success: () => {
              app.showToast('网址已复制', 'success');
            }
          });
        }
      }
    });
  }
});