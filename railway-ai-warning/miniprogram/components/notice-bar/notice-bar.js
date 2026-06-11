/**
 * 通知栏组件
 */
Component({
  properties: {
    text: {
      type: String,
      value: ''
    },
    type: {
      type: String,
      value: 'info'
    },
    closable: {
      type: Boolean,
      value: true
    },
    scrollable: {
      type: Boolean,
      value: false
    }
  },

  data: {
    visible: true
  },

  methods: {
    onClose() {
      this.setData({ visible: false });
      this.triggerEvent('close');
    },

    onTap() {
      this.triggerEvent('tap');
    }
  }
});
