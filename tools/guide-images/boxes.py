"""Görseldeki metin satırlarını otomatik bulur, numaralı bir teşhis görseli üretir."""
import sys, json
import numpy as np
from PIL import Image, ImageDraw

def line_boxes(path, thr=0.18, gap=14, minw=8, minh=6, bg=None):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im, dtype=np.float32)
    if bg is None:
        # en sık renk = zemin
        q = (a // 8).astype(np.int32)
        flat = q[:,:,0]*4096 + q[:,:,1]*64 + q[:,:,2]
        vals, cnt = np.unique(flat, return_counts=True)
        top = vals[cnt.argmax()]
        bg = ((top//4096)*8+4, ((top//64)%64)*8+4, (top%64)*8+4)
    d = np.abs(a - np.array(bg, dtype=np.float32)).max(axis=2)/255.0
    m = d > thr
    rows = m.any(axis=1)
    # satır bantları
    bands=[]; y=0; H=len(rows)
    while y < H:
        if rows[y]:
            y2=y
            while y2+1 < H and (rows[y2+1] or (y2+2<H and rows[y2+2]) or (y2+3<H and rows[y2+3])): y2+=1
            bands.append((y,y2)); y=y2+1
        else: y+=1
    out=[]
    for (y1,y2) in bands:
        sub = m[y1:y2+1]
        cols = sub.any(axis=0)
        x=0; W=len(cols)
        while x < W:
            if cols[x]:
                x2=x
                while x2+1 < W:
                    nxt = cols[x2+1:min(W,x2+1+gap)]
                    if nxt.any(): x2 += 1 + int(np.argmax(nxt))
                    else: break
                sb = m[y1:y2+1, x:x2+1]
                ys = np.where(sb.any(axis=1))[0]; xs = np.where(sb.any(axis=0))[0]
                bx = (x+int(xs[0]), y1+int(ys[0]), x+int(xs[-1]), y1+int(ys[-1]))
                if bx[2]-bx[0]+1 >= minw and bx[3]-bx[1]+1 >= minh: out.append(bx)
                x = x2+1
            else: x += 1
    return im, bg, out

if __name__ == '__main__':
    p = sys.argv[1]; thr=float(sys.argv[2]) if len(sys.argv)>2 else 0.18
    gap=int(sys.argv[3]) if len(sys.argv)>3 else 14
    im, bg, bs = line_boxes(p, thr=thr, gap=gap)
    print('bg', bg, 'size', im.size, 'boxes', len(bs))
    dbg = im.copy(); dr = ImageDraw.Draw(dbg)
    for i,(x1,y1,x2,y2) in enumerate(bs):
        dr.rectangle([x1-2,y1-2,x2+2,y2+2], outline=(255,0,0), width=2)
        dr.text((x1, max(0,y1-16)), str(i), fill=(255,0,255))
        print(i, (x1,y1,x2-x1+1,y2-y1+1))
    dbg.save(p.replace('.png','_dbg.png'))
