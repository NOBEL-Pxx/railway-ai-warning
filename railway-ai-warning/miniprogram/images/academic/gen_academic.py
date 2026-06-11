"""生成学术风格占位图，用于微信小程序非轮播图占位"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r'C:\Users\lenovo\Desktop\微信小程序\railway-ai-warning\miniprogram\images\academic'
os.makedirs(OUT, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.facecolor'] = '#0a0e27'
plt.rcParams['figure.facecolor'] = '#080c20'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

# ── 1. 雷达回波图（降水预测）──
def gen_radar():
    fig, ax = plt.subplots(figsize=(6, 5))
    np.random.seed(42)
    x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
    z = np.exp(-0.3*(x**2 + y**2)) * (np.sin(2*x) + np.cos(2*y)) * 0.5
    z += np.exp(-0.8*((x-1)**2 + (y+0.5)**2)) * 0.8
    z += np.exp(-0.6*((x+0.8)**2 + (y-1)**2)) * 0.6
    c = ax.contourf(x, y, z, levels=20, cmap='RdYlGn_r')
    plt.colorbar(c, ax=ax, label='Reflectivity (dBZ)')
    ax.set_title('Radar Reflectivity Nowcast', color='white', fontsize=13, fontweight='bold')
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.contour(x, y, z, levels=[0.3, 0.6], colors='white', linewidths=0.5, alpha=0.4)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'radar_echo.png'), dpi=120, bbox_inches='tight')
    plt.close(); print('OK radar_echo.png')

# ── 2. 神经网络架构图（MambaSwin-UNet）──
def gen_neural_arch():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor('#0a0e27')
    blocks = [
        (0.5, 3.5, 1.2, 1.2, '#1a3a6b', 'Input\n(T×H×W)'),
        (2.0, 3.5, 1.4, 1.2, '#7B61FF', 'Mamba\nBlock'),
        (3.8, 4.2, 1.2, 1.0, '#165DFF', 'Swin\nEncoder'),
        (3.8, 2.8, 1.2, 1.0, '#0496C7', 'Skip\nConnect'),
        (5.6, 3.5, 1.4, 1.2, '#FF6B9D', 'UNet\nDecoder'),
        (7.4, 3.5, 1.2, 1.2, '#00D4FF', 'STA\nModule'),
        (9.0, 3.5, 0.8, 1.2, '#FFD700', 'Pred\nOutput'),
    ]
    for x, y, w, h, color, label in blocks:
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.1',
                                        facecolor=color, edgecolor='white', alpha=0.85, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h/2, label, ha='center', va='center', color='white',
                fontsize=8, fontweight='bold')
    arrows = [(1.7, 4.1), (3.4, 4.1), (5.0, 4.1), (7.0, 4.1), (8.8, 4.1)]
    for ax_x, ax_y in arrows:
        ax.annotate('', xy=(ax_x+0.2, ax_y), xytext=(ax_x, ax_y),
                    arrowprops=dict(arrowstyle='->', color='#00E5FF', lw=1.5))
    ax.text(5.0, 7.5, 'MambaSwin-UNet-STA Architecture', ha='center', va='top',
            color='white', fontsize=11, fontweight='bold')
    ax.text(5.0, 7.0, 'Short-term Precipitation Nowcasting', ha='center', va='top',
            color='#aaaaaa', fontsize=9)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'neural_arch.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK neural_arch.png')

# ── 3. SCS-CN水文模型示意图 ──
def gen_hydrology():
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    # 左图：CN曲线关系
    ax = axes[0]
    P = np.linspace(0, 120, 200)
    for cn, color, label in [(70,'#00D4FF','CN=70'), (80,'#FFD700','CN=80'), (90,'#FF6B9D','CN=90')]:
        S = 25400/cn - 254
        Ia = 0.2 * S
        Q = np.where(P > Ia, (P - Ia)**2 / (P - Ia + S), 0)
        ax.plot(P, Q, color=color, lw=2, label=label)
    ax.set_xlabel('Rainfall P (mm)')
    ax.set_ylabel('Runoff Q (mm)')
    ax.set_title('SCS-CN Runoff Curve', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)
    # 右图：径流过程线
    ax2 = axes[1]
    t = np.linspace(0, 12, 200)
    hydro = 80 * t * np.exp(-0.5*t)
    ax2.fill_between(t, hydro, alpha=0.6, color='#165DFF')
    ax2.plot(t, hydro, color='#00D4FF', lw=2)
    ax2.axvline(t[np.argmax(hydro)], color='#FFD700', lw=1.5, linestyle='--', label='Peak Flow')
    ax2.set_xlabel('Time (h)')
    ax2.set_ylabel('Discharge (m³/s)')
    ax2.set_title('Unit Hydrograph', fontsize=10, fontweight='bold')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.2)
    fig.suptitle('SCS-CN Hydrological Model', color='white', fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'hydrology_model.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK hydrology_model.png')

# ── 4. UAV路径规划图 ──
def gen_uav_route():
    fig, ax = plt.subplots(figsize=(6, 5))
    x = np.linspace(0, 10, 500)
    y1 = 2 + 0.5*np.sin(0.8*x) + 0.2*np.cos(1.5*x)
    y2 = 5 + 0.4*np.cos(0.6*x) + 0.3*np.sin(x)
    ax.plot(x, y1, color='#00D4FF', lw=2.5, label='UAV-1 Route', linestyle='-')
    ax.plot(x, y2, color='#FFD700', lw=2.5, label='UAV-2 Route', linestyle='--')
    ax.scatter([0, 5, 10], [2, 2.3, 1.9], color='#FF6B9D', s=80, zorder=5, label='Waypoints')
    ax.scatter([0, 5, 10], [5, 5.2, 4.8], color='#FF9500', s=80, zorder=5)
    terrain_x = np.linspace(0, 10, 100)
    terrain_y = 0.3*np.sin(0.5*terrain_x) + 0.8
    ax.fill_between(terrain_x, 0, terrain_y, color='#3a2a1a', alpha=0.8, label='Terrain')
    ax.plot(terrain_x, terrain_y, color='#8B6914', lw=1.5)
    ax.set_xlabel('Longitude (km)'); ax.set_ylabel('Altitude (km)')
    ax.set_title('UAV Patrol Route Planning\nRailway Monitoring System', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.15)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'uav_route.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK uav_route.png')

# ── 5. 铁路沿线风险热力图 ──
def gen_risk_heatmap():
    fig, ax = plt.subplots(figsize=(7, 4))
    np.random.seed(7)
    risk = np.zeros((8, 24))
    for i in range(8):
        risk[i] = np.abs(np.random.randn(24)) * 0.5
        risk[i, 6:12] += np.exp(-0.2*np.arange(6)) * 0.8
    risk[2:5, 14:20] += 0.9
    im = ax.imshow(risk, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1.5,
                   interpolation='bilinear')
    plt.colorbar(im, ax=ax, label='Risk Index')
    ax.set_yticks(range(8))
    ax.set_yticklabels([f'K{300+i*50}' for i in range(8)], fontsize=8)
    ax.set_xticks(range(0, 24, 4))
    ax.set_xticklabels([f'{h}:00' for h in range(0, 24, 4)], fontsize=8)
    ax.set_xlabel('Time (UTC+8)'); ax.set_ylabel('Railway Mileage')
    ax.set_title('Railway Disaster Risk Heatmap (24h Forecast)', fontsize=10, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'risk_heatmap.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK risk_heatmap.png')

# ── 6. 多源数据融合流程图 ──
def gen_data_fusion():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
    sources = [
        (0.3, 6.5, '#165DFF', 'Satellite\nRemote Sensing'),
        (0.3, 4.5, '#7B61FF', 'UAV\nImagery'),
        (0.3, 2.5, '#0496C7', 'Ground\nSensor'),
        (0.3, 0.5, '#00D4FF', 'NWP\nModel'),
    ]
    for x, y, c, label in sources:
        rect = mpatches.FancyBboxPatch((x, y), 1.8, 0.9, boxstyle='round,pad=0.08',
                                        facecolor=c, edgecolor='white', alpha=0.85)
        ax.add_patch(rect)
        ax.text(x+0.9, y+0.45, label, ha='center', va='center', color='white', fontsize=7.5)
        ax.annotate('', xy=(3.0, 3.7), xytext=(x+1.8, y+0.45),
                    arrowprops=dict(arrowstyle='->', color='#aaaaaa', lw=1.0, connectionstyle='arc3,rad=0.1'))
    rect_fusion = mpatches.FancyBboxPatch((3.0, 2.8), 2.2, 1.8, boxstyle='round,pad=0.12',
                                           facecolor='#FF6B9D', edgecolor='white', alpha=0.9, linewidth=1.5)
    ax.add_patch(rect_fusion)
    ax.text(4.1, 3.7, 'OpenClaw\nFusion Engine', ha='center', va='center', color='white', fontsize=9, fontweight='bold')
    ax.annotate('', xy=(6.2, 3.7), xytext=(5.2, 3.7),
                arrowprops=dict(arrowstyle='->', color='#FFD700', lw=2))
    rect_out = mpatches.FancyBboxPatch((6.2, 2.8), 2.0, 1.8, boxstyle='round,pad=0.12',
                                        facecolor='#FFD700', edgecolor='white', alpha=0.85)
    ax.add_patch(rect_out)
    ax.text(7.2, 3.7, 'Warning\nOutput', ha='center', va='center', color='black', fontsize=9, fontweight='bold')
    ax.text(5.0, 7.6, 'Multi-Source Data Fusion Framework', ha='center', va='top',
            color='white', fontsize=11, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'data_fusion.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK data_fusion.png')

# ── 7. 降水预测评分曲线 ──
def gen_forecast_score():
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    lead_times = [10, 30, 60, 90, 120, 150, 180]
    ts_ours = [0.78, 0.71, 0.63, 0.55, 0.48, 0.42, 0.36]
    ts_wrf  = [0.62, 0.54, 0.46, 0.40, 0.35, 0.30, 0.25]
    ts_ext  = [0.70, 0.61, 0.52, 0.44, 0.38, 0.32, 0.26]
    ax = axes[0]
    ax.plot(lead_times, ts_ours, 'o-', color='#00D4FF', lw=2.5, label='Our Model', markersize=6)
    ax.plot(lead_times, ts_wrf,  's--', color='#FF9500', lw=1.8, label='WRF', markersize=5)
    ax.plot(lead_times, ts_ext,  '^--', color='#B366FF', lw=1.8, label='Extrapolation', markersize=5)
    ax.axhline(0.5, color='white', lw=0.8, linestyle=':', alpha=0.4, label='Skill threshold')
    ax.set_xlabel('Lead Time (min)'); ax.set_ylabel('TS Score')
    ax.set_title('Threat Score Comparison', fontsize=10, fontweight='bold')
    ax.legend(fontsize=7.5); ax.grid(True, alpha=0.2)
    ax2 = axes[1]
    pod = [0.92, 0.85, 0.76, 0.68, 0.59, 0.52, 0.45]
    far = [0.18, 0.22, 0.28, 0.33, 0.39, 0.44, 0.50]
    sc = ax2.scatter(far, pod, c=lead_times, cmap='cool', s=80, zorder=5)
    ax2.plot(far, pod, color='#00D4FF', lw=1.5, alpha=0.6)
    plt.colorbar(sc, ax=ax2, label='Lead time (min)')
    ax2.set_xlabel('False Alarm Rate'); ax2.set_ylabel('Probability of Detection')
    ax2.set_title('POD vs FAR (ROC-like)', fontsize=10, fontweight='bold')
    ax2.grid(True, alpha=0.2)
    fig.suptitle('Forecast Performance Metrics', color='white', fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'forecast_score.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK forecast_score.png')

# ── 8. 卫星云图风格（伪彩色）──
def gen_satellite_ir():
    fig, ax = plt.subplots(figsize=(6, 5))
    np.random.seed(2024)
    x, y = np.meshgrid(np.linspace(0, 10, 300), np.linspace(0, 10, 300))
    cloud = (np.sin(0.5*x)*np.cos(0.4*y) + 0.5*np.sin(x+y) +
             np.exp(-0.1*((x-5)**2+(y-5)**2))*0.8 +
             np.random.randn(300,300)*0.1)
    im = ax.imshow(cloud, cmap='Blues_r', extent=[0,10,0,10], origin='lower')
    plt.colorbar(im, ax=ax, label='Brightness Temperature (K)')
    ax.contour(x, y, cloud, levels=[-0.2, 0.0, 0.5], colors=['yellow','orange','red'],
               linewidths=1, alpha=0.6)
    ax.set_title('Infrared Satellite Cloud Image\n(Simulated Convective System)',
                 fontsize=10, fontweight='bold')
    ax.set_xlabel('Longitude (°E)'); ax.set_ylabel('Latitude (°N)')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'satellite_ir.jpg'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK satellite_ir.jpg')

# ── 9. 降水量时序图 ──
def gen_precip_timeseries():
    fig, ax = plt.subplots(figsize=(7, 4))
    np.random.seed(100)
    hours = np.arange(0, 24)
    obs   = np.clip(np.random.exponential(2, 24), 0, 15)
    obs[6:10] += [8, 12, 10, 6]
    pred  = obs * (1 + np.random.randn(24)*0.15)
    pred = np.clip(pred, 0, None)
    ax.bar(hours, obs, color='#165DFF', alpha=0.7, label='Observed', width=0.6)
    ax.step(hours, pred, color='#FF6B9D', lw=2.5, label='Predicted', where='mid')
    ax.fill_between(hours, pred*0.8, pred*1.2, color='#FF6B9D', alpha=0.15, label='±20% CI')
    ax.set_xlabel('Hour (UTC+8)'); ax.set_ylabel('Precipitation (mm/h)')
    ax.set_title('24h Hourly Precipitation: Observed vs Predicted', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.2)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'precip_timeseries.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK precip_timeseries.png')

# ── 10. 边坡失稳分析图 ──
def gen_slope_analysis():
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
    # 山坡轮廓
    slope_x = [0, 2, 4, 7, 8, 10]
    slope_y = [5, 5, 4, 1.5, 1, 1]
    ax.fill_between(slope_x, 0, slope_y, color='#3a2a10', alpha=0.8)
    ax.plot(slope_x, slope_y, color='#8B6914', lw=2.5)
    # 铁路
    ax.fill_between([6.5, 10], [0.8, 0.8], [1.2, 1.2], color='#888888', alpha=0.9)
    ax.plot([6.5, 10], [1.0, 1.0], color='#cccccc', lw=4, solid_capstyle='round')
    ax.plot([7, 7.5, 8, 8.5, 9, 9.5], [1.0]*6, '|', color='#666666', markersize=12, mew=2)
    # 滑坡范围
    slide_x = np.linspace(2.5, 6.5, 100)
    slide_y = 4.5 - 0.5*(slide_x-2.5)**1.2
    ax.fill_between(slide_x, slide_y-0.3, slide_y, color='#FF4444', alpha=0.5)
    ax.plot(slide_x, slide_y, color='#FF4444', lw=2.5, linestyle='--', label='Failure Surface')
    # 雨水
    for xi in np.linspace(1, 5, 12):
        ax.annotate('', xy=(xi, slide_y[int((xi-1)/4*99)]-0.1),
                    xytext=(xi, slide_y[int((xi-1)/4*99)]+0.8),
                    arrowprops=dict(arrowstyle='->', color='#00D4FF', lw=1.0))
    ax.text(5.0, 7.2, 'Rainfall-induced Slope Failure Analysis', ha='center',
            color='white', fontsize=9, fontweight='bold')
    ax.text(8.5, 1.5, 'Railway', ha='center', color='white', fontsize=8)
    ax.text(3.5, 5.2, 'Rainfall', ha='center', color='#00D4FF', fontsize=8)
    ax.text(4.0, 3.0, 'Slide Body', ha='center', color='#FF9999', fontsize=8)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'slope_analysis.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK slope_analysis.png')

# ── 11. 数字孪生可视化概念图 ──
def gen_digital_twin():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
    # 物理世界
    rect1 = mpatches.FancyBboxPatch((0.2, 1.0), 3.8, 5.5, boxstyle='round,pad=0.15',
                                     facecolor='#0a1a3a', edgecolor='#165DFF', linewidth=2, alpha=0.9)
    ax.add_patch(rect1)
    ax.text(2.1, 7.0, 'Physical World', ha='center', color='#165DFF', fontsize=9, fontweight='bold')
    # 数字世界
    rect2 = mpatches.FancyBboxPatch((6.0, 1.0), 3.8, 5.5, boxstyle='round,pad=0.15',
                                     facecolor='#0a1a3a', edgecolor='#7B61FF', linewidth=2, alpha=0.9)
    ax.add_patch(rect2)
    ax.text(7.9, 7.0, 'Digital Twin', ha='center', color='#7B61FF', fontsize=9, fontweight='bold')
    # 物理世界内容
    for i, (label, color) in enumerate([('Railway Sensor', '#00D4FF'), ('UAV Camera', '#FFD700'), ('Ground Station', '#00FF88')]):
        y = 5.5 - i*1.5
        mini = mpatches.FancyBboxPatch((0.6, y-0.35), 3.0, 0.7, boxstyle='round,pad=0.06',
                                        facecolor=color, alpha=0.25, edgecolor=color)
        ax.add_patch(mini)
        ax.text(2.1, y, label, ha='center', color=color, fontsize=8)
    # 数字世界内容
    for i, (label, color) in enumerate([('3D Model', '#00D4FF'), ('Prediction Engine', '#FFD700'), ('Risk Map', '#FF6B9D')]):
        y = 5.5 - i*1.5
        mini = mpatches.FancyBboxPatch((6.4, y-0.35), 3.0, 0.7, boxstyle='round,pad=0.06',
                                        facecolor=color, alpha=0.25, edgecolor=color)
        ax.add_patch(mini)
        ax.text(7.9, y, label, ha='center', color=color, fontsize=8)
    # 双向同步箭头
    for y in [5.5, 4.0, 2.5]:
        ax.annotate('', xy=(6.0, y+0.1), xytext=(4.0, y+0.1),
                    arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.8))
        ax.annotate('', xy=(4.0, y-0.1), xytext=(6.0, y-0.1),
                    arrowprops=dict(arrowstyle='->', color='#00D4FF', lw=1.8))
    ax.text(5.0, 0.4, 'Real-time Synchronization', ha='center', color='#aaaaaa', fontsize=8)
    ax.set_title('Digital Twin Framework for Railway Safety', color='white', fontsize=11, fontweight='bold', pad=5)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'digital_twin.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK digital_twin.png')

# ── 12. 多模态传感器载荷示意 ──
def gen_sensor_payload():
    fig, axes = plt.subplots(2, 2, figsize=(7, 6))
    np.random.seed(55)
    # 可见光图（模拟）
    ax = axes[0,0]
    img_vis = np.random.rand(50, 80, 3) * 0.4 + 0.1
    img_vis[20:30, 30:50] = [0.6, 0.5, 0.3]  # 铁路
    ax.imshow(img_vis)
    ax.set_title('RGB Camera (4K)', fontsize=9, fontweight='bold', color='white')
    ax.axis('off')
    # 红外图
    ax2 = axes[0,1]
    x, y = np.meshgrid(range(80), range(50))
    ir = np.exp(-0.02*((x-40)**2+(y-25)**2)) * 300 + 200 + np.random.randn(50,80)*5
    ir[20:30, 30:50] += 30
    ax2.imshow(ir, cmap='inferno')
    ax2.set_title('Thermal IR (640×512)', fontsize=9, fontweight='bold', color='white')
    ax2.axis('off')
    # 气象传感器数据
    ax3 = axes[1,0]
    t = np.linspace(0, 12, 100)
    ax3.plot(t, 15 + 8*np.sin(0.5*t) + np.random.randn(100)*0.5, color='#FF6B9D', lw=1.5, label='Temp(°C)')
    ax3.plot(t, 50 + 20*np.cos(0.3*t) + np.random.randn(100), color='#00D4FF', lw=1.5, label='Humidity(%)')
    ax3.set_title('Met Sensor (6-element)', fontsize=9, fontweight='bold', color='white')
    ax3.legend(fontsize=7); ax3.grid(True, alpha=0.2)
    # LiDAR点云（散点模拟）
    ax4 = axes[1,1]
    n = 500
    px = np.random.randn(n)*2
    py = np.random.randn(n)*2
    pz = np.random.randn(n) - np.abs(px)*0.5
    sc = ax4.scatter(px, py, c=pz, cmap='viridis', s=3, alpha=0.7)
    ax4.set_title('LiDAR Point Cloud', fontsize=9, fontweight='bold', color='white')
    ax4.axis('off')
    for ax_ in axes.flat:
        ax_.set_facecolor('#0a0e27')
    fig.suptitle('Multi-modal UAV Sensor Payload', color='white', fontsize=11, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'sensor_payload.png'), dpi=120, bbox_inches='tight',
                facecolor='#080c20')
    plt.close(); print('OK sensor_payload.png')

# 运行所有生成器
gen_radar()
gen_neural_arch()
gen_hydrology()
gen_uav_route()
gen_risk_heatmap()
gen_data_fusion()
gen_forecast_score()
gen_satellite_ir()
gen_precip_timeseries()
gen_slope_analysis()
gen_digital_twin()
gen_sensor_payload()
print('\n全部生成完毕！')
