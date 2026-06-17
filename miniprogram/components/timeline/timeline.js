/**
 * 时间轴组件
 */
Component({
  properties: {
    items: {
      type: Array,
      value: []
    },
    direction: {
      type: String,
      value: 'vertical'
    }
  },

  data: {},

  methods: {
    onItemTap(e) {
      const index = e.currentTarget.dataset.index;
      this.triggerEvent('itemtap', { index });
    }
  }
});
