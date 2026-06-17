/**
 * 图表组件
 */
Component({
  properties: {
    type: {
      type: String,
      value: 'bar'
    },
    data: {
      type: Array,
      value: []
    },
    width: {
      type: Number,
      value: 300
    },
    height: {
      type: Number,
      value: 200
    }
  },

  data: {
    chartData: []
  },

  lifetimes: {
    attached() {
      this.processData();
    }
  },

  observers: {
    'data': function(data) {
      this.processData();
    }
  },

  methods: {
    processData() {
      const data = this.data.data || [];
      this.setData({ chartData: data });
    }
  }
});
