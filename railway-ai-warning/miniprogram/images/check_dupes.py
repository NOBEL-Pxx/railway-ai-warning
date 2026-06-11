# -*- coding: utf-8 -*-
import os, re
from collections import defaultdict

base = r'C:\Users\lenovo\Desktop\微信小程序\railway-ai-warning\miniprogram'
img_map = defaultdict(list)

for root, dirs, files in os.walk(os.path.join(base, 'pages')):
    for fn in files:
        if fn.endswith(('.wxml', '.js')):
            fp = os.path.join(root, fn)
            page = os.path.basename(root)
            with open(fp, 'r', encoding='utf-8') as f:
                c = f.read()
            imgs = re.findall(r'/images/resources/[\w._-]+', c)
            for img in set(imgs):
                img_map[img].append(page)

cross_page = {k: sorted(set(v)) for k, v in img_map.items() if len(set(v)) > 1}
if cross_page:
    print('跨页重复图片:')
    for k, v in sorted(cross_page.items()):
        print('  %s: %s' % (k, v))
else:
    print('OK: 无跨页重复！')
