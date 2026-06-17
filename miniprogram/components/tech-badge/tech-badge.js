/**
 * 技术标签组件
 */
Component({
  properties: {
    name: {
      type: String,
      value: ''
    },
    icon: {
      type: String,
      value: ''
    },
    color: {
      type: String,
      value: '#165DFF'
    },
    size: {
      type: String,
      value: 'normal'
    }
  },

  data: {},

  methods: {
    onTap() {
      this.triggerEvent('tap');
    }
  }
});
