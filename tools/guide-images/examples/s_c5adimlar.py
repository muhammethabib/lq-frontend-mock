"""Örnek: c5-adimlar — SAYDAM zeminde duran metin.

Bu görselin alttaki iki adım yazısı saydam bir bant üzerinde duruyor: harf
şekilleri RGB'de değil ALFA kanalında. Shot.save() özgün alfayı geri koyduğu
için, yalnız RGB'yi silmek Türkçe yazıyı silmiyordu; İngilizcesi üstüne binip
okunmaz hâle geliyordu (32d4ab4'te üretilen görselde böyleydi).

tool.replace_scaled artık kutunun alfasını da temizleyip yeni metnin alfasını
ekliyor, bu yüzden aynı akış saydam zeminde de doğru çalışıyor. Balon yazısı
opak zeminde; aynı çağrı onu da doğru ele alıyor.
"""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from drive import run

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'assets')
SRC = os.path.join(A, 'kilavuz', 'c5-adimlar.webp')
OUT = os.path.join(A, 'kilavuz-en', 'c5-adimlar.webp')

run(SRC, OUT, [
 # alttaki adım yazıları: saydam bant, sola hizalı
 dict(tr='Kelimenin üzerine gelin', en='Hover over the word', anchor='left',
      family='Inter', weight='700', size=17, rs=[0.78], region=(690,0,778,1380)),
 dict(tr='İşaretin üzerine gelin', en='Hover over the sign', anchor='left',
      family='Inter', weight='700', size=17, rs=[0.78], region=(690,0,778,1380)),
 # balon: opak koyu zemin, İngilizcesi daha geniş olduğu için ortalanır
 dict(tr='Hata bildir', en='Report Error', anchor='center',
      family='Inter', weight='800', size=17, rs=[0.81],
      region=(100,1100,190,1380), bg=(15,23,42)),
])
