Component({
  properties: {
    chartId: {
      type: String,
      value: 'chart'
    },
    width: {
      type: Number,
      value: 300
    },
    height: {
      type: Number,
      value: 200
    },
    type: {
      type: String,
      value: 'line'
    },
    data: {
      type: Object,
      value: {}
    }
  },
  data: {
    // 组件内部数据
  },
  lifetimes: {
    attached() {
      // 组件挂载时初始化图表
      this.initChart();
    }
  },
  methods: {
    initChart() {
      // 图表初始化逻辑
      console.log('Chart initialized:', this.data.chartId);
    }
  }
});