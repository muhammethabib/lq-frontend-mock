"""Örnek: b-ara-sonuclari — en kalabalık görsel (25 metin, rozetler dahil).

Çalışma dizeni: TR görselin kopyası img/ altında, EN çıktı out/ altına yazılır;
sonra out/ PNG'leri webp olarak assets/kilavuz-en/ içine konur.
Biçimler önceki turda ölçüldü; burada sabit verilerek tarama atlanıyor.
"""
import time
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import tool
from drive import run
t0=time.time()
# biçimler önceki turda ölçüldü; artık sadece uygulanıyor (tarama yok)
HDR = dict(family='Inter',weight='800',size=12,ls=0.12,rs=[0.54])
CAP = dict(family='Inter',weight='700',size=12,ls=0.12,rs=[0.51])
SEC1= dict(family='Inter',weight='600',size=11,ls=0.08,rs=[0.75])
SEC2= dict(family='Inter',weight='700',size=12,ls=0.08,rs=[0.66])
PILL= dict(family='Inter',weight='700',size=13,ls=0.04,rs=[0.54])
BADGE=[dict(family='Inter',weight=w,size=sz,ls=l) for w in ('700','800') for sz in (10,11,12) for l in (0.04,0.06)]
PGL  =[dict(family='Inter',weight=w,size=sz,ls=l) for w in ('600','700','800') for sz in (8,9,10) for l in (0.02,0.04)]

specs=[
 dict(tr='Kelime Çözücü', en='Word Decoder', anchor='center', family='Inter', weight='700', size=15, rs=[0.66], region=(20,600,80,900)),
 dict(tr='Ara', en='Search', anchor='center', family='Inter', weight='600', size=12, rs=[0.84], region=(20,880,80,1030)),
 dict(tr='Ara', en='Search', anchor='center', family='Inter', weight='700', size=15, ls=0.02, rs=[0.66], bg=(157,28,81), region=(130,1000,210,1120)),
 dict(tr='Tüm Sözlükler', en='All Dictionaries', anchor='left', family='Inter', weight='500', size=14, rs=[0.63], region=(130,1130,210,1500)),
 dict(tr='OSM', en='OTT', anchor='center', family='Inter', weight='800', size=10, ls=0.03, rs=[0.66], bg=(157,28,81), region=(140,70,200,125)),
 dict(tr='İNG', en='ENG', anchor='center', family='Inter', weight='800', size=10, ls=0.03, rs=[0.63], region=(140,120,200,180)),
 dict(tr='ARAMA SONUÇLARI', en='SEARCH RESULTS', anchor='left', region=(295,30,345,320), **CAP),
 dict(tr='YAZILIŞA GÖRE ARA', en='SEARCH BY SPELLING', anchor='left', family='Inter', weight='700', size=13, ls=0.08, rs=[0.48], region=(295,950,345,1250)),
 dict(tr='SÖZLÜK (17 CİLT) TARANDI', en='DICTIONARIES (17 VOLUMES) SCANNED.', anchor='left', family='Inter', weight='700', size=11, ls=0.02, rs=[0.60], region=(465,60,505,420)),
 dict(tr='SONUÇ BULUNDU', en='RECORDS FOUND.', anchor='left', family='Inter', weight='700', size=10, rs=[0.69], region=(435,60,470,420)),
 dict(tr='ARAMAYI GENİŞLET', en='EXPAND SEARCH', anchor='center', family='Inter', weight='700', size=13, ls=0.10, rs=[0.51], region=(405,820,495,1250)),
 dict(tr='TAM EŞLEŞME', en='EXACT MATCH', anchor='center', bg=(16,42,105), region=(405,1130,495,1380), **PILL),
 dict(tr='BENZER OKUNUŞ', en='SIMILAR PRONUNCIATION', anchor='left', region=(405,1330,495,1660), **PILL),
 dict(tr='MADDE BAŞI', en='HEADWORD', anchor='center', region=(514,900,574,1150), **HDR),
 dict(tr='KATEGORİ', en='CATEGORY', anchor='center', region=(514,540,574,720), **HDR),
 dict(tr='SONUÇ', en='RESULT', anchor='center', region=(514,200,574,420), **HDR),
 dict(tr='SÖZLÜK', en='DICTIONARY', anchor='center', region=(514,1350,574,1600), **HDR),
 dict(tr='KÖK', en='LEMMA', anchor='left', region=(598,0,668,400), **SEC1),
 dict(tr='ÇEKİMLİ BİÇİMLER', en='INFLECTED FORMS', anchor='left', region=(1158,0,1228,500), **SEC2),
 dict(tr='TÜREMİŞ BİÇİMLER', en='DERIVED FORMS', anchor='left', region=(1500,0,1570,500), **SEC2),
 dict(tr='İBARELER VE BİRLEŞİK KELİMELER', en='PHRASES AND COMPOUNDS', anchor='left', region=(1733,0,1803,700), **SEC2),
 dict(tr='KISMİ EŞLEŞMELER', en='SIMILAR SPELLINGS', anchor='left', region=(2075,0,2145,500), **SEC2),
 dict(tr='ALT MADDE BAŞI', en='SUBHEADWORD', anchor='center', grid=BADGE, region=(1900,560,2000,760)),
 dict(tr='İLİŞKİLİ', en='RELATED', anchor='center', grid=BADGE, region=(1000,560,1080,740)),
 dict(tr='MADDE BAŞI', en='HEADWORD', anchor='center', count=10, thr=0.86, grid=BADGE, region=(600,560,2350,760)),
]
for n,c in [('193',1),('92',1),('35',2),('31',4),('21',1),('16',1),('3',1)]:
    specs.append(dict(tr=f'SAYFA {n}', en=f'PAGE {n}', anchor='right', count=c, thr=0.86, grid=PGL, region=(580,1380,2400,1620)))
run('out/_asgeo.png','out/b-ara-sonuclari.png',specs)

# kısalan bölüm başlıklarında sayı balonunu metne yaklaştır
s2 = tool.Shot('out/b-ara-sonuclari.png')
for en,tr,st,y in [('DERIVED FORMS','TÜREMİŞ BİÇİMLER',SEC2,1525),
                   ('PHRASES AND COMPOUNDS','İBARELER VE BİRLEŞİK KELİMELER',SEC2,1758)]:
    r=st['rs'][0]
    w1,_=tool.text_width(tr,st,r); w2,_=tool.text_width(en,st,r)
    tool.narrow(s2, 85+w2+6, w1-w2, y-16, y+40)
    print(f"   · {tr[:14]} daraltıldı Δ={w1-w2}")
s2.save('out/b-ara-sonuclari.png')
print(f"süre: {time.time()-t0:.0f} sn")
