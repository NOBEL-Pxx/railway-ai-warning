/**
 * 环形进度条组件
 */
Component({
  properties: {
    percent: {
      type: Number,
      value: 0
    },
    size: {
      type: Number,
      value: 120
    },
    strokeWidth: {
      type: Number,
      value: 8
    },
    color: {
      type: String,
      value: '#165DFF'
    },
    bgColor: {
      type: String,
      value: '#E5E6EB'
    },
    showText: {
      type: Boolean,
      value: true
    }
  },

  data: {
    circumference: 0,
    offset: 0
  },

  lifetimes: {
    attached() {
      this.calculateProgress();
    }
  },

  observers: {
    'percent': function() {
      this.calculateProgress();
    }
  },

  methods: {
    calculateProgress() {
      const { size, strokeWidth, percent } = this.data;
      const radius = (size - strokeWidth) / 2;
      const circumference = 2 * Math.PI * radius;
      const offset = circumference - (percent / 100) * circumference;
      
      this.setData({
        circumference,
        offset
      });
    }
  }
});
