"""Örnek: piksel cerrahisi — kırpılmış tepeyi kardeş görselden tamamlama (fix_top)
ve bir bloğu kaydırıp boşluğu satır-medyanı ile doldurma (fix_align).
Metin değiştirme yok; doğrudan assets/kilavuz*/ üzerinde çalışır.
"""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from PIL import Image
import numpy as np

def load(p):
    im=Image.open(p); return im.convert('RGB'), (im.split()[3] if im.mode=='RGBA' else None), im.mode
def save(base, alpha, mode, path):
    o=base.convert('RGBA') if mode=='RGBA' else base
    if mode=='RGBA': o.putalpha(alpha)
    o.save(path,'WEBP',quality=92,method=6)

def fix_top(dirpath, pad=25, dx=34):
    """c2-pastirma-1'in kesik üstünü, aynı sahnenin -2 sürümünden tamamla."""
    a,aal,amode=load(dirpath+'c2-pastirma-1.webp')
    b,_,_=load(dirpath+'c2-pastirma-2.webp')
    W,H=a.size
    new=Image.new('RGB',(W,H+pad),(255,255,255))
    new.paste(b.crop((dx,0,dx+W,pad)),(0,0))     # eksik üst şerit
    new.paste(a,(0,pad))
    if aal is not None:
        na=Image.new('L',(W,H+pad),255); na.paste(aal,(0,pad)); aal=na
    save(new,aal,amode,dirpath+'c2-pastirma-1.webp')
    return new.size

def fix_align(dirpath, dx=31, box=(1770,50,1960,410)):
    """b-okunus-renk: üstteki iki 'nazar' bloğunu sağa kaydırıp alttaki satırla hizala."""
    im,al,mode=load(dirpath+'b-okunus-renk.webp')
    x0,y0,x1,y1=box
    blk=im.crop(box)
    a=np.asarray(im).copy()
    # eski yeri satır satır temiz zeminle doldur (sağdaki boş alandan)
    for y in range(y0,y1):
        med=np.median(a[y,2100:2200],axis=0).astype(np.uint8)
        a[y,x0:x1]=med
    im2=Image.fromarray(a)
    im2.paste(blk,(x0+dx,y0))
    save(im2,al,mode,dirpath+'b-okunus-renk.webp')
    return im2.size
