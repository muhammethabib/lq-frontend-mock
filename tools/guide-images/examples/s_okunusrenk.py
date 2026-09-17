"""Örnek: b-okunus-renk — metin uzadığı için önce kutuyu genişletme (widen/narrow),
sonra metinleri değiştirme. Çalışma dizeni s_arasonuc.py ile aynı.
"""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import tool
from drive import run, grid
SM  =grid(('600','700','800'),(9,10,11,12),(0.02,0.04,0.06,0.08))
BODY=grid(('400','500','600','700'),(12,13,14,15),(0,))

# efsane satırı: "Editör onaylı" → "Editor-approved" için yer aç
s=tool.Shot('img/b-okunus-renk.png')
ST=dict(family='Inter',weight='700',size=15,ls=0)
sc,y,x,r,p,shp = tool.fit_scaled(s,'Editör onaylı',ST,[1.05],region=(670,1240,730,1560))[0]
wt,_=tool.text_width('Editör onaylı',ST,r); we,_=tool.text_width('Editor-approved',ST,r); d=we-wt
print(f"efsane: ({x},{y}) skor {sc:.3f} Δ={d}")
Y0,Y1=660,750
tool.narrow(s, 300, d//2, Y0, Y1)
tool.widen(s, x-d//2+wt+6, d, Y0, Y1)
s.save('out/_orgeo.png')

run('out/_orgeo.png','out/b-okunus-renk.png',[
 dict(tr='MADDE BAŞI', en='HEADWORD', anchor='center', count=2, thr=0.84, grid=SM, region=(90,930,380,1180)),
 dict(tr='ALT MADDE', en='SUBHEADWORD', anchor='center', grid=SM, region=(500,930,600,1180)),
 dict(tr='Otomatik üretim', en='Auto-generated', anchor='left', grid=BODY, region=(660,650,740,1030)),
 dict(tr='soluk', en='pale', anchor='left', grid=BODY, region=(660,1000,740,1140)),
 dict(tr='Editör onaylı', en='Editor-approved', anchor='left', grid=BODY, region=(660,1200,740,1560)),
 dict(tr='koyu', en='dark', anchor='left', family='Inter', weight='700', size=17, rs=[0.96], region=(660,1500,740,1800)),
])
from PIL import Image
Image.open('out/b-okunus-renk.png').convert('RGB').crop((400,600,2260,772)).save('out/_z3.png')
