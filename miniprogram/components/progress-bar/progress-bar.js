/**
 * 进度条组件
 */
Component({
  properties: {
    percent: {
      type: Number,
      value: 0
    },
    height: {
      type: Number,
      value: 12
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
    },
    animated: {
      type: Boolean,
      value: true
    }
  },

  data: {
    currentPercent: 0
  },

  lifetimes: {
    attached() {
      this.animateProgress();
    }
  },

  observers: {
    'percent': function() {
      this.animateProgress();
    }
  },

  methods: {
    animateProgress() {
      if (this.data.animated) {
        const duration = 600;
        const start = this.data.currentPercent;
        const end = this.data.percent;
        const startTime = Date.now();
        
        const animate = () => {
          const elapsed = Date.now() - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const easeProgress = 1 - Math.pow(1 - progress, 3);
          const current = start + (end - start) * easeProgress;
          
          this.setData({ currentPercent: current });
          
          if (progress < 1) {
            requestAnimationFrame(animate);
          }
        };
        
        animate();
      } else {
        this.setData({ currentPercent: this.data.percent });
      }
    }
  }
});
