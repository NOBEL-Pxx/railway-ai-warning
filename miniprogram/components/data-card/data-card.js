/**
 * 数据卡片组件
 */
Component({
  properties: {
    title: {
      type: String,
      value: ''
    },
    value: {
      type: String,
      value: ''
    },
    unit: {
      type: String,
      value: ''
    },
    trend: {
      type: String,
      value: ''
    },
    trendType: {
      type: String,
      value: 'up'
    },
    icon: {
      type: String,
      value: ''
    },
    color: {
      type: String,
      value: '#165DFF'
    }
  },

  data: {},

  methods: {
    onTap() {
      this.triggerEvent('tap');
    }
  }
});
