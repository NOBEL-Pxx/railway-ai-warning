/**
 * 无人机页 - 智驭苍穹·守路安澜
 * 优化版 - 增加更多无人机功能和展示
 */

const app = getApp();

Page({
  data: {
    // 页面状态
    activeTab: 0,
    showSpecs: false,
    
    // 无人机规格
    uavSpecs: {
      model: 'Y3',
      fullName: 'Y3垂起固定翼无人机',
      manufacturer: '智驭科技',
      endurance: '120min',
      range: '50km',
      speed: '80km/h',
      payload: '2kg',
      wingspan: '2.4m',
      weight: '8kg',
      ceiling: '5000m',
      windResistance: 'Level 6'
    },
    
    // 规格详情
    specDetails: [
      { label: '续航时间', value: '120min', icon: '' },
      { label: '通信距离', value: '50km', icon: '' },
      { label: '巡航速度', value: '80km/h', icon: '' },
      { label: '载荷能力', value: '2kg', icon: '' },
      { label: '翼展', value: '2.4m', icon: '' },
      { label: '起飞重量', value: '8kg', icon: '' },
      { label: '升限', value: '5000m', icon: '' },
      { label: '抗风等级', value: '6级', icon: '' }
    ],
    
    // 载荷配置
    payloads: [
      { 
        name: '多光谱相机', 
        spec: '4K/60fps',
        description: '高分辨率可见光成像，支持4K视频录制',
        image: '/images/resources/sa_convlstm_unit.jpg',
        icon: '📷'
      },
      { 
        name: '红外热像仪', 
        spec: '640×512',
        description: '热成像监测，夜间及恶劣天气可用',
        image: '/images/resources/sda_tr_attention.png',
        icon: '🔴'
      },
      { 
        name: '气象传感器', 
        spec: '六要素',
        description: '温湿度、气压、风速风向、降水量',
        image: '/images/resources/scs_cn_runoff.png',
        icon: '🌡️'
      },
      { 
        name: '激光雷达', 
        spec: '100m测距',
        description: '高精度地形测绘与障碍物检测',
        image: '/images/resources/radar_cappi_product.jpg',
        icon: '📡'
      }
    ],
    
    // 应用场景时间轴
    scenarios: [
      { 
        time: 'T+0min', 
        title: '灾害预警触发', 
        desc: '系统识别高风险区域，自动调度无人机',
        icon: '',
        color: '#FF4D4F'
      },
      { 
        time: 'T+5min', 
        title: '快速部署起飞', 
        desc: '垂起设计，无需跑道准备，即刻升空',
        icon: '',
        color: '#FF9500'
      },
      { 
        time: 'T+10min', 
        title: '现场数据采集', 
        desc: '多载荷同步工作，实时获取现场数据',
        icon: '',
        color: '#165DFF'
      },
      { 
        time: 'T+15min', 
        title: '数据回传分析', 
        desc: '5G实时传输，云端AI即时分析',
        icon: '',
        color: '#00CC99'
      }
    ],
    
    // 集群管理
    fleetStats: {
      total: 12,
      standby: 8,
      flying: 2,
      maintenance: 2,
      rate: '98%'
    },
    
    // 无人机位置（模拟）
    dronePositions: [
      { id: 1, name: 'UAV-001', status: 'flying', lat: 36.05, lng: 103.86, battery: 78 },
      { id: 2, name: 'UAV-002', status: 'standby', lat: 36.06, lng: 103.87, battery: 100 },
      { id: 3, name: 'UAV-003', status: 'standby', lat: 36.04, lng: 103.85, battery: 95 },
      { id: 4, name: 'UAV-004', status: 'maintenance', lat: 36.07, lng: 103.88, battery: 0 }
    ],
    
    // 技术优势
    techAdvantages: [
      {
        title: '垂起设计',
        desc: '无需跑道，随时随地快速部署',
        icon: ''
      },
      {
        title: '长航时',
        desc: '120分钟续航，覆盖大范围区域',
        icon: ''
      },
      {
        title: '多载荷',
        desc: '支持多种传感器灵活配置',
        icon: ''
      },
      {
        title: '智能控制',
        desc: '自主规划航线，自动避障',
        icon: ''
      }
    ],
    
    // 任务统计
    missionStats: {
      total: 156,
      thisMonth: 23,
      success: 153,
      successRate: '98%'
    }
  },

  // ============ 生命周期函数 ============

  onLoad(options) {
    console.log('[UAV] Page loaded', options);
  },

  onReady() {
    console.log('[UAV] Page ready');
  },

  onShow() {
    console.log('[UAV] Page show');
  },

  onHide() {
    console.log('[UAV] Page hide');
  },

  onUnload() {
    console.log('[UAV] Page unload');
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh();
  },

  onShareAppMessage() {
    return app.onShareAppMessage(
      '空天感知平台 - 智驭苍穹·守路安澜',
      '/pages/uav/uav',
      '/images/resources/space_air_ground_arch.webp'
    );
  },

  // ============ 用户交互 ============

  // 切换Tab
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ activeTab: index });
    app.vibrateShort();
  },

  // 查看技术方案
  viewTech() {
    app.vibrateShort();
    app.switchTab('/pages/tech/tech');
  },

  // 切换规格显示
  toggleSpecs() {
    this.setData({ showSpecs: !this.data.showSpecs });
    app.vibrateShort();
  },

  // 查看载荷详情
  viewPayloadDetail(e) {
    const index = e.currentTarget.dataset.index;
    const payload = this.data.payloads[index];
    
    app.vibrateShort();
    
    wx.showModal({
      title: payload.name,
      content: `${payload.spec}\n\n${payload.description}`,
      showCancel: false,
      confirmText: '确定'
    });
  },

  // 查看场景详情
  viewScenarioDetail(e) {
    const index = e.currentTarget.dataset.index;
    const scenario = this.data.scenarios[index];
    
    app.vibrateShort();
    app.showToast(`${scenario.time} ${scenario.title}`, 'none');
  },

  // 查看无人机详情
  viewDroneDetail(e) {
    const id = e.currentTarget.dataset.id;
    const drone = this.data.dronePositions.find(d => d.id === id);
    
    app.vibrateShort();
    
    if (drone) {
      const statusMap = {
        flying: '飞行中',
        standby: '待命',
        maintenance: '维护中'
      };
      
      wx.showModal({
        title: drone.name,
        content: `状态：${statusMap[drone.status]}\n电量：${drone.battery}%\n位置：${drone.lat.toFixed(2)}, ${drone.lng.toFixed(2)}`,
        showCancel: false,
        confirmText: '确定'
      });
    }
  },

  // 预约演示 - contact是tabBar页面，用switchTab
  bookDemo() {
    app.vibrateShort();
    app.switchTab('/pages/contact/contact');
  }
});
