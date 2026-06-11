/**
 * 玻璃拟态卡片组件
 */
Component({
  properties: {
    title: {
      type: String,
      value: ''
    },
    subtitle: {
      type: String,
      value: ''
    },
    icon: {
      type: String,
      value: ''
    },
    gradient: {
      type: String,
      value: 'blue'
    },
    clickable: {
      type: Boolean,
      value: true
    }
  },

  data: {
    isPressed: false
  },

  methods: {
    onTap() {
      if (this.data.clickable) {
        this.triggerEvent('tap');
      }
    },

    onTouchStart() {
      if (this.data.clickable) {
        this.setData({ isPressed: true });
      }
    },

    onTouchEnd() {
      this.setData({ isPressed: false });
    }
  }
});
