import numpy as np

def _integral(a):
    return np.pad(a.cumsum(0).cumsum(1), ((1,0),(1,0)))

def ncc(scene, tmpl):
    """Normalize edilmiş çapraz korelasyon haritası (FFT). scene>=tmpl boyutunda."""
    H,W = scene.shape; h,w = tmpl.shape
    if h>H or w>W: return None
    t = tmpl - tmpl.mean()
    tn = np.sqrt((t*t).sum())
    if tn < 1e-9: return None
    fh, fw = 1<<int(np.ceil(np.log2(H+h))), 1<<int(np.ceil(np.log2(W+w)))
    F = np.fft.rfft2(scene, s=(fh,fw))
    T = np.fft.rfft2(t[::-1,::-1], s=(fh,fw))
    num = np.fft.irfft2(F*T, s=(fh,fw))[h-1:H, w-1:W]
    I1 = _integral(scene); I2 = _integral(scene*scene)
    def winsum(I):
        return I[h:H+1, w:W+1] - I[0:H-h+1, w:W+1] - I[h:H+1, 0:W-w+1] + I[0:H-h+1, 0:W-w+1]
    s1 = winsum(I1); s2 = winsum(I2); n = h*w
    var = np.maximum(s2 - s1*s1/n, 0.0)
    sd = np.sqrt(var/n)
    den = np.sqrt(var)*tn
    out = np.where((den>1e-9) & (sd>0.02), num/np.maximum(den,1e-9), -1.0)
    return out

def best(scene, tmpl, region=None):
    if region:
        y0,x0,y1,x1 = region
        sub = scene[y0:y1, x0:x1]
        m = ncc(sub, tmpl)
        if m is None: return (-1,0,0)
        i = int(m.argmax()); y,x = divmod(i, m.shape[1])
        return (float(m[y,x]), y+y0, x+x0)
    m = ncc(scene, tmpl)
    if m is None: return (-1,0,0)
    i = int(m.argmax()); y,x = divmod(i, m.shape[1])
    return (float(m[y,x]), y, x)

def peaks(scene, tmpl, thr=0.8, region=None, maxn=40):
    """Eşiği aşan tüm eşleşmeler (üst üste binmeyen)."""
    y0,x0 = (region[0],region[1]) if region else (0,0)
    sub = scene[region[0]:region[2], region[1]:region[3]] if region else scene
    m = ncc(sub, tmpl)
    if m is None: return []
    h,w = tmpl.shape; res=[]
    mm = m.copy()
    for _ in range(maxn):
        i = int(mm.argmax()); y,x = divmod(i, mm.shape[1]); sc = float(mm[y,x])
        if sc < thr: break
        res.append((sc, y+y0, x+x0))
        mm[max(0,y-h//2):y+h//2+1, max(0,x-w//2):x+w//2+1] = -2
    return res

def _half(a):
    h,w = a.shape
    h2,w2 = h//2, w//2
    if h2<2 or w2<2: return None
    return a[:h2*2,:w2*2].reshape(h2,2,w2,2).mean(axis=(1,3))

def best_fast(scene, tmpl, region=None, pad=8):
    """Kaba-ince arama: önce yarı çözünürlükte, sonra tam çözünürlükte küçük pencerede."""
    y0,x0,y1,x1 = region or (0,0,scene.shape[0],scene.shape[1])
    sub = scene[y0:y1, x0:x1]
    h,w = tmpl.shape
    if h>sub.shape[0] or w>sub.shape[1]: return (-1,0,0)
    s2, t2 = _half(sub), _half(tmpl)
    if s2 is None or t2 is None or t2.shape[0]<2 or t2.shape[1]<2 or \
       t2.shape[0]>s2.shape[0] or t2.shape[1]>s2.shape[1]:
        sc,y,x = best(sub, tmpl); return (sc, y+y0, x+x0)
    m = ncc(s2,t2)
    if m is None:
        sc,y,x = best(sub, tmpl); return (sc, y+y0, x+x0)
    i=int(m.argmax()); cy,cx = divmod(i, m.shape[1])
    ry0,rx0 = max(0,cy*2-pad), max(0,cx*2-pad)
    ry1 = min(sub.shape[0]-h, cy*2+pad); rx1 = min(sub.shape[1]-w, cx*2+pad)
    bestv=(-2,0,0)
    t = tmpl - tmpl.mean(); tn = np.sqrt((t*t).sum()) or 1e-6
    for y in range(ry0, ry1+1):
        for x in range(rx0, rx1+1):
            p = sub[y:y+h, x:x+w]
            pm = p - p.mean(); pn = np.sqrt((pm*pm).sum()) or 1e-6
            if pn/np.sqrt(h*w) < 0.02: continue
            v = float((pm*t).sum()/(pn*tn))
            if v > bestv[0]: bestv=(v,y,x)
    return (bestv[0], bestv[1]+y0, bestv[2]+x0)
