# -*- coding: utf-8 -*-
import os

# uav.wxml - fleet-map 从 railway_debris_simulation -> space_air_ground_arch
fp = r'C:\Users\lenovo\Desktop\微信小程序\railway-ai-warning\miniprogram\pages\uav\uav.wxml'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()
c2 = c.replace(
    'src="/images/resources/railway_debris_simulation.jpg" mode="aspectFill" lazy-load="true"',
    'src="/images/resources/space_air_ground_arch.webp" mode="aspectFill" lazy-load="true"'
)
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c2)
print('uav.wxml done, changed:', c.count('railway_debris_simulation'))

# uav.js
fp2 = r'C:\Users\lenovo\Desktop\微信小程序\railway-ai-warning\miniprogram\pages\uav\uav.js'
with open(fp2, 'r', encoding='utf-8') as f:
    c = f.read()
c2 = c.replace(
    "'/images/resources/railway_debris_simulation.jpg'",
    "'/images/resources/space_air_ground_arch.webp'"
)
with open(fp2, 'w', encoding='utf-8') as f:
    f.write(c2)
print('uav.js done, changed:', c.count('railway_debris_simulation'))
