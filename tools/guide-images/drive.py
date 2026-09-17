"""Görsel başına değişim listesini uygular ve eşleşme skorlarını yazar."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tool

RS = [round(0.24+0.03*i,2) for i in range(47)]

def grid(ws=('400','500','600','700','800'), szs=(11,12,13,14,15), lss=(0,)):
    return [dict(family='Inter',weight=w,size=s,ls=l) for w in ws for s in szs for l in lss]

def run(src, out, specs, verbose=True):
    s = tool.Shot(src)
    rep = []
    for sp in specs:
        tr, en = sp['tr'], sp['en']
        bg = tuple(sp.get('bg',(255,255,255)))
        region = sp.get('region')
        rs = sp.get('rs', RS)
        if sp.get('grid'):
            best = tool.fit_grid(s, tr, sp['grid'], rs, region=region, bg=bg, top=1)[0]
            sc, y, x, r, p, style = best
            hits = [(sc,y,x)]
        else:
            style = dict(family=sp.get('family','Inter'), weight=str(sp.get('weight','400')),
                         size=sp.get('size',15), ls=sp.get('ls',0), style=sp.get('style','normal'),
                         transform=sp.get('transform','none'))
            sc, y, x, r, p, shp = tool.fit_scaled(s, tr, style, rs, region=region, bg=bg)[0]
            hits = [(sc,y,x)]
        n = sp.get('count', 1)
        if n > 1:
            pk, p, shp = tool.peaks_scaled(s, tr, style, r, thr=sp.get('thr',0.82), region=region, bg=bg, maxn=n+4)
            hits = pk[:n]
        else:
            stt = dict(style); stt.update(text=tr, dsf=2, color='#000000')
            p = tool.render_many([stt])[0]
        for (hsc,hy,hx) in hits:
            tool.replace_scaled(s, hy, hx, p, r, en, style, color=sp.get('color'), bg=sp.get('fill'),
                                anchor=sp.get('anchor','left'), pad=sp.get('pad',3),
                                dy=sp.get('dy',0), dx=sp.get('dx',0))
            rep.append((tr,en,round(hsc,3),hx,hy,round(r,3)))
            if verbose:
                flag = '  ' if hsc>=0.85 else '!!'
                print(f" {flag}{hsc:.3f} r={r:.2f} ({hx},{hy}) {tr[:34]!r} → {en[:34]!r}"
                      + (f" w={style['weight']} sz={style['size']} ls={style['ls']}" if sp.get('grid') else ''))
    s.save(out)
    return rep
