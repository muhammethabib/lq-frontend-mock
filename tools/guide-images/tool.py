"""Ekran görüntülerindeki Türkçe arayüz metinlerini İngilizceleriyle değiştirir.

Akış (her metin için):
 1) Türkçe metin, verilen biçim adaylarıyla Chromium'da basılır (saydam zemin).
 2) Basılan desenin alfa maskesi görselde aranır (FFT ile normalize çapraz korelasyon).
    En yüksek skoru veren biçim = görselin gerçek biçimi. Skor, ölçümün doğruluğunu
    kendiliğinden bildirir; göz kararı yok.
 3) Eşleşen kutu, çevresinden örneklenen zemin rengiyle silinir.
 4) İngilizce metin aynı biçimle basılıp aynı hizada (sol/orta/sağ) yerleştirilir.
"""
import json, os, subprocess, itertools, hashlib
import numpy as np
from PIL import Image
import ncc

SC = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(SC, 'rcache')
os.makedirs(CACHE, exist_ok=True)

def _key(j):
    return hashlib.md5(json.dumps(j, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]

def render_many(specs):
    """specs: [{text,family,weight,size,color,ls,style,transform,dsf}] -> [png path]"""
    jobs=[]; paths=[]
    for s in specs:
        s = dict(s); s.setdefault('color','#000000'); s.setdefault('ls',0)
        s.setdefault('weight','400'); s.setdefault('family','Inter'); s.setdefault('dsf',1)
        s.setdefault('style','normal'); s.setdefault('transform','none'); s.setdefault('lh',1.2)
        s.setdefault('html','')
        p = os.path.join(CACHE, _key(s)+'.png'); paths.append(p)
        if not os.path.exists(p):
            j = dict(s); j['out']=p; jobs.append(j)
    if jobs: 
        f=os.path.join(SC,'_jobs_%d.json'%os.getpid()); json.dump(jobs, open(f,'w'), ensure_ascii=False)
        r=subprocess.run(['node', os.path.join(SC,'render.js'), f], capture_output=True, text=True, cwd=SC)
        if r.returncode: raise RuntimeError(r.stderr[-2000:])
    return paths

def alpha(p):
    im = Image.open(p).convert('RGBA')
    return np.asarray(im, dtype=np.float32)[:,:,3]/255.0

class Shot:
    def __init__(self, path):
        self.path = path
        self.im = Image.open(path)
        self.mode = self.im.mode
        if self.mode=='RGBA':
            self.a = self.im.split()[3]
            flat = Image.new('RGB', self.im.size, (255,255,255)); flat.paste(self.im, (0,0), self.im)
            self.orig = self.im.convert('RGB')     # dokunulmayan pikseller için
            self.rgb = flat                        # eşleştirme ve düzenleme için
        else:
            self.rgb = self.im.convert('RGB'); self.a = None; self.orig = None
        self.arr = np.asarray(self.rgb, dtype=np.float32)
        self.log=[]

    def ink(self, bg):
        return np.abs(self.arr - np.array(bg,dtype=np.float32)).max(axis=2)/255.0

    def _scene(self, region, bg):
        d = self.ink(bg)
        return d

    def fit(self, text, region=None, families=('Inter',), weights=('400',), sizes=None,
            lss=(0,), styles=('normal',), transforms=('none',), bg=(255,255,255), dsf=1, top=3):
        """En iyi biçimi bulur. sizes: piksel boyu adayları (görsel ölçeğinde)."""
        sizes = sizes or [round(x,1) for x in np.arange(10,40,0.5)]
        specs=[]; meta=[]
        for fam,w,sz,ls,st,tt in itertools.product(families,weights,sizes,lss,styles,transforms):
            specs.append(dict(text=text,family=fam,weight=str(w),size=sz,ls=ls,style=st,transform=tt,dsf=dsf))
            meta.append((fam,w,sz,ls,st,tt))
        paths = render_many(specs)
        scene = self._scene(region, bg)
        reg = region
        out=[]
        for p,(fam,w,sz,ls,st,tt) in zip(paths,meta):
            t = alpha(p)
            if reg and (t.shape[0]>reg[2]-reg[0] or t.shape[1]>reg[3]-reg[1]): continue
            sc,y,x = ncc.best(scene, t, reg)
            out.append((sc,y,x,dict(family=fam,weight=str(w),size=sz,ls=ls,style=st,transform=tt,dsf=dsf),p))
        out.sort(key=lambda r:-r[0])
        return out[:top]

    def sample_colors(self, y, x, tpath):
        t = alpha(tpath); h,w = t.shape
        patch = self.arr[y:y+h, x:x+w]
        ink = t>0.85; bgm = t<0.02
        txt = np.median(patch[ink],axis=0) if ink.sum()>4 else None
        bg  = np.median(patch[bgm],axis=0) if bgm.sum()>4 else None
        return (None if txt is None else tuple(int(v) for v in txt),
                None if bg is None else tuple(int(v) for v in bg))

    def replace(self, y, x, tpath, en_text, style, color=None, bg=None, anchor='left', pad=2, dy=0, dx=0):
        t = alpha(tpath); h,w = t.shape
        tc, bc = self.sample_colors(y,x,tpath)
        color = color or ('#%02x%02x%02x'%tc)
        bg = bg or bc or (255,255,255)
        # sil
        box=(max(0,x-pad), max(0,y-pad), min(self.rgb.width,x+w+pad), min(self.rgb.height,y+h+pad))
        self.rgb.paste(Image.new('RGB',(box[2]-box[0],box[3]-box[1]), tuple(int(v) for v in bg)), box[:2])
        # bas
        sp = dict(style); sp.update(text=en_text, color=color)
        np_ = render_many([sp])[0]
        nim = Image.open(np_).convert('RGBA')
        nw,nh = nim.size
        if anchor=='left': px = x
        elif anchor=='right': px = x + w - nw
        else: px = x + (w-nw)//2
        py = y + (h-nh)//2 if anchor=='center-v' else y
        self.rgb.paste(nim, (px+dx, py+dy), nim)
        self.log.append(dict(en=en_text, at=(x,y), size=(w,h), new=(nw,nh), color=color, bg=tuple(int(v) for v in bg)))
        return (px,py,nw,nh)

    def save(self, out_png):
        if self.a is not None:
            base = self.orig.copy()
            for (x0,y0,x1,y1) in getattr(self, 'dirty', []):
                base.paste(self.rgb.crop((x0,y0,x1,y1)), (x0,y0))
            im = base.convert('RGBA'); im.putalpha(self.a)
        else:
            im = self.rgb
        im.save(out_png)
        return out_png

# --- ölçek uyumlu eşleştirme: özgün görseller 2x çekilip küçültülmüş ---
from PIL import Image as _I

def _alpha_im(p):
    return _I.open(p).convert('RGBA').split()[3]

def scaled_alpha(p, r):
    a = _alpha_im(p)
    w,h = a.size
    nw,nh = max(1,int(round(w*r))), max(1,int(round(h*r)))
    return np.asarray(a.resize((nw,nh), _I.LANCZOS), dtype=np.float32)/255.0

def fit_scaled(shot, text, style, rs, region=None, bg=(255,255,255)):
    """Tek render (dsf=2) + farklı küçültme oranlarıyla eşleştirme."""
    sp = dict(style); sp.update(text=text, dsf=2, color='#000000')
    p = render_many([sp])[0]
    scene = shot.ink(bg)
    out=[]
    for r in rs:
        t = scaled_alpha(p, r)
        if region and (t.shape[0]>region[2]-region[0] or t.shape[1]>region[3]-region[1]): continue
        if t.shape[0]>scene.shape[0] or t.shape[1]>scene.shape[1]: continue
        sc,y,x = ncc.best_fast(scene, t, region)
        out.append((sc,y,x,r,p,t.shape))
    out.sort(key=lambda z:-z[0])
    ref=[]
    for sc,y,x,r,p2,shp in out[:12]:
        t = scaled_alpha(p2, r)
        sc2,y2,x2 = ncc.best(scene, t, region)
        ref.append((sc2,y2,x2,r,p2,t.shape))
    ref.sort(key=lambda z:-z[0])
    return ref + out[4:]

def replace_scaled(shot, y, x, tpath, r, en_text, style, color=None, bg=None, anchor='left', pad=3, dy=0, dx=0):
    t = scaled_alpha(tpath, r); h,w = t.shape
    patch = shot.arr[y:y+h, x:x+w]
    ink = t>0.85; bgm = t<0.02
    tc = np.median(patch[ink],axis=0) if ink.sum()>4 else np.array([0,0,0])
    bc = np.median(patch[bgm],axis=0) if bgm.sum()>4 else np.array([255,255,255])
    color = color or ('#%02x%02x%02x'%tuple(int(v) for v in tc))
    bgc = tuple(int(v) for v in (bg if bg is not None else bc))
    box=(max(0,x-pad), max(0,y-pad), min(shot.rgb.width,x+w+pad), min(shot.rgb.height,y+h+pad))
    shot.rgb.paste(_I.new('RGB',(box[2]-box[0],box[3]-box[1]), bgc), box[:2])
    # Saydam zeminde yazı: harf şekilleri RGB'de değil ALFA'da duruyor. save()
    # özgün alfayı geri koyduğu için, yalnız RGB'yi silmek eski yazıyı silmiyor;
    # yenisi üstüne biniyordu. Kutunun alfası da burada sıfırlanır, yeni metnin
    # alfası aşağıda eklenir. Opak zeminde kutu tamamen opak yapılır.
    alfa_kutu = None
    if shot.a is not None:
        alfa_kutu = box
        ea = np.asarray(shot.a.crop(box), dtype=np.float32)/255.0
        seffaf = float((ea < 0.04).mean())
        shot.a.paste(0 if seffaf > 0.5 else 255, box)
    sp = dict(style); sp.update(text=en_text, dsf=2, color=color)
    np_ = render_many([sp])[0]
    nim = _I.open(np_).convert('RGBA')
    nw,nh = nim.size
    nim = nim.resize((max(1,int(round(nw*r))), max(1,int(round(nh*r)))), _I.LANCZOS)
    nw,nh = nim.size
    if anchor=='left': px = x
    elif anchor=='right': px = x + w - nw
    else: px = x + (w-nw)//2
    py = y + (h-nh)//2
    shot.rgb.paste(nim, (px+dx, py+dy), nim)
    if alfa_kutu is not None:
        # yeni metnin alfası kutudaki mevcut alfayla birleştirilir (opakta no-op)
        na = nim.split()[3]
        cur = shot.a.crop((px+dx, py+dy, px+dx+nw, py+dy+nh))
        shot.a.paste(_I.fromarray(np.maximum(np.asarray(cur), np.asarray(na))), (px+dx, py+dy))
    shot.arr = np.asarray(shot.rgb, dtype=np.float32)
    if not hasattr(shot,'dirty'): shot.dirty=[]
    shot.dirty.append((max(0,min(box[0],px+dx)-4), max(0,min(box[1],py+dy)-4),
                       min(shot.rgb.width, max(box[2], px+dx+nw)+4), min(shot.rgb.height, max(box[3], py+dy+nh)+4)))
    shot.log.append(dict(en=en_text, at=(x,y), tr_size=(w,h), new=(nw,nh), color=color, bg=bgc, r=round(r,4)))
    return (px+dx, py+dy, nw, nh)

def peaks_scaled(shot, text, style, r, thr=0.82, region=None, bg=(255,255,255), maxn=40):
    sp = dict(style); sp.update(text=text, dsf=2, color='#000000')
    p = render_many([sp])[0]
    t = scaled_alpha(p, r)
    scene = shot.ink(bg)
    reg = region or (0,0,shot.rgb.height, shot.rgb.width)
    return ncc.peaks(scene, t, thr=thr, region=reg, maxn=maxn), p, t.shape

def fit_grid(shot, text, grid, rs, region=None, bg=(255,255,255), top=4, fast=True):
    """grid: [{family,weight,size,ls,style,transform}] — biçim × ölçek taraması."""
    specs=[]
    for st in grid:
        sp = dict(st); sp.update(text=text, dsf=2, color='#000000'); specs.append(sp)
    paths = render_many(specs)
    scene = shot.ink(bg)
    out=[]
    for st,p in zip(grid,paths):
        for r in rs:
            t = scaled_alpha(p, r)
            if region and (t.shape[0]>region[2]-region[0] or t.shape[1]>region[3]-region[1]): continue
            if t.shape[0]>scene.shape[0] or t.shape[1]>scene.shape[1]: continue
            sc,y,x = (ncc.best_fast if fast else ncc.best)(scene, t, region)
            out.append((sc,y,x,r,p,st))
    out.sort(key=lambda z:-z[0])
    # ilk adayları tam çözünürlükte doğrula
    ref=[]
    for sc,y,x,r,p,st in out[:top*2]:
        t = scaled_alpha(p, r)
        sc2,y2,x2 = ncc.best(scene, t, region)
        ref.append((sc2,y2,x2,r,p,st))
    ref.sort(key=lambda z:-z[0])
    return ref[:top]

# --- kutu/pil genişletme: düz zeminli bölgede sütun ekleyip çıkarma ---
def widen(shot, x_seam, n, y0, y1):
    """y0..y1 satırlarında x_seam'den sağdaki içeriği n px sağa kaydırır,
    boşluğu x_seam sütununu tekrarlayarak doldurur (düz zemin + yatay kenarlar korunur)."""
    im = shot.rgb
    W,H = im.size
    strip = im.crop((0,y0,W,y1))
    right = strip.crop((x_seam,0,W,y1-y0))
    col = strip.crop((x_seam,0,x_seam+1,y1-y0)).resize((n, y1-y0), _I.NEAREST)
    strip.paste(col,(x_seam,0))
    strip.paste(right,(x_seam+n,0))
    im.paste(strip,(0,y0))
    shot.arr = np.asarray(im, dtype=np.float32)
    if not hasattr(shot,'dirty'): shot.dirty=[]
    shot.dirty.append((0,y0,im.size[0],y1))

def narrow(shot, x_seam, n, y0, y1):
    """x_seam'den n sütun siler, sağdaki içeriği sola çeker; sağ kenarı son sütunla doldurur."""
    im = shot.rgb
    W,H = im.size
    strip = im.crop((0,y0,W,y1))
    right = strip.crop((x_seam+n,0,W,y1-y0))
    strip.paste(right,(x_seam,0))
    tail = strip.crop((W-n-1,0,W-n,y1-y0)).resize((n,y1-y0), _I.NEAREST)
    strip.paste(tail,(W-n,0))
    im.paste(strip,(0,y0))
    shot.arr = np.asarray(im, dtype=np.float32)
    if not hasattr(shot,'dirty'): shot.dirty=[]
    shot.dirty.append((0,y0,im.size[0],y1))

def text_width(text, style, r):
    sp = dict(style); sp.update(text=text, dsf=2, color='#000000')
    p = render_many([sp])[0]
    from PIL import Image as I2
    w,h = I2.open(p).size
    return int(round(w*r)), int(round(h*r))
