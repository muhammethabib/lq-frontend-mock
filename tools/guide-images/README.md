# Kılavuz görselleri: arayüz metinlerini dile çevirme

`assets/kilavuz/` (TR) ve `assets/kilavuz-en/` (EN) altındaki kılavuz ekran
görüntüleri aynı sahnelerin iki dildeki hâlidir. Bu klasör, bir ekran
görüntüsünün **içindeki** arayüz metinlerini elle photoshoplamadan, ölçerek
değiştirmeye yarayan araçları içerir: metin sitedeki gerçek font ve boyutla
yeniden basılır, yerine yapıştırılır; sonuç gözle değil, eşleşme skoruyla
doğrulanır.

## Nasıl çalışır

Her metin için:

1. Türkçe metin, aday biçimlerle (aile / ağırlık / punto / harf aralığı)
   Chromium'da saydam zemine basılır — sayfayı çizen motorun aynısı.
2. Basılan desenin alfa maskesi, görselin içinde FFT tabanlı **normalize
   çapraz korelasyon** (`ncc.py`) ile aranır. En yüksek skoru veren aday,
   görselin gerçek biçimidir. Skor ölçümün doğruluğunu kendiliğinden bildirir:
   **≥ 0.85 = biçim ve konum doğru**, altı şüphelidir (`drive.run` düşük
   skorları `!!` ile işaretler).
3. Bulunan kutu, çevresinden örneklenen zemin rengiyle silinir.
4. İngilizce metin aynı biçimle basılıp aynı hizada (sol / orta / sağ)
   yerleştirilir.

Özgün görseller 2x çekilip küçültüldüğü için render de `dsf=2` yapılıp
`r` oranıyla LANCZOS ile küçültülür; `r` de aramanın bir parçasıdır.

## Kurulum

```bash
pip install numpy pillow
npm install playwright          # ya da sistemde global kurulu olması yeterli
python3 fetch-fonts.py          # fonts/gf-local.css üretir (~5 MB, repoya girmez)
```

Chromium: `CHROMIUM_PATH` ya da `PLAYWRIGHT_BROWSERS_PATH` ile bulunur; ikisi
de yoksa Playwright kendi indirdiğini kullanır.

## Dosyalar

| Dosya | İş |
| --- | --- |
| `tool.py` | Çekirdek: render önbelleği, `Shot`, biçim arama (`fit_scaled`, `fit_grid`), değiştirme (`replace_scaled`), `widen`/`narrow`, `text_width` |
| `ncc.py` | Normalize çapraz korelasyon: `best`, `best_fast` (kaba-ince), `peaks` (aynı metnin tüm kopyaları) |
| `drive.py` | Bir görsel için değişim listesini uygular, skorları yazar |
| `render.js` | Metni Chromium'da saydam zemine basar |
| `lib.js` | Chromium'u bulur, yerel font paketini okur, sayfayı font yönlendirmesiyle açar |
| `verify.js` | Sayfa denetimi: kırık görsel, kırık iç bağlantı, konsol hatası |
| `boxes.py` | Teşhis: görseldeki metin satırlarını bulup numaralı kutularla işaretler |
| `fetch-fonts.py` | Google Fonts paketini indirip `fonts/gf-local.css` içine gömer |
| `examples/` | Gerçek işler: `s_arasonuc.py` (en kalabalık görsel), `s_okunusrenk.py` (kutu genişletme), `imgfix.py` (kırpılmış tepe tamamlama, blok hizalama) |

## Kullanım

```bash
python3 examples/s_arasonuc.py          # TR görselden EN görsel üretir
node verify.js pages/user-guide-en.html # sayfayı denetler
python3 boxes.py /yol/gorsel.png 0.18   # metin kutularını çıkarır (teşhis)
```

Tipik bir değişim listesi (`drive.run`):

```python
from drive import run
run('img/b-ara-sonuclari.png', 'out/b-ara-sonuclari.png', [
  dict(tr='ARAMA SONUÇLARI', en='SEARCH RESULTS', anchor='left',
       family='Inter', weight='700', size=12, ls=0.12, rs=[0.51],
       region=(295, 30, 345, 320)),
  dict(tr='MADDE BAŞI', en='HEADWORD', anchor='center', count=10, thr=0.86,
       grid=BADGE, region=(600, 560, 2350, 760)),
])
```

- `region=(y0, x0, y1, x1)` aramayı daraltır — hem hızlandırır hem yanlış
  eşleşmeyi engeller.
- `rs=[...]` bilinen ölçek; `grid=[...]` biçim bilinmiyorsa aday kümesi.
  **Hız için önce bir kez ölçün, sonra ölçülen biçimi sabit verin**: kör
  tarama (biçim × 47 ölçek) bir görselde dakikalar sürer, sabit biçim
  saniyeler.
- `count=n` aynı metnin n kopyasını birden değiştirir (`thr` eşiğiyle).
- `anchor`: İngilizce metin Türkçesinden uzun/kısa olduğunda hizayı korur.

### Kutular ve rozetler taşınca

İngilizce metin kutuya sığmıyorsa metni küçültmek yerine kutuyu büyütün:
`widen(shot, x_seam, n, y0, y1)` dikişten sağdakini n piksel sağa iter,
`narrow` tersini yapar. İkisini birlikte kullanarak kutunun dış kenarını
sabit tutup iç boşluktan yer çalabilirsiniz. Sıra önemlidir: metin
uzuyorsa **önce `widen`, sonra değiştirme**; kısalıyorsa değiştirmeden
sonra `narrow`.

## Notlar

- `fonts/`, `rcache/`, `_jobs_*.json` üretilir ve repoya girmez (bkz.
  `.gitignore`); `fetch-fonts.py` istendiğinde yeniden üretir.
- RGBA görsellerde eşleştirme beyaz zemine düzleştirilmiş kopya üzerinde
  yapılır; kaydederken yalnızca dokunulan kutular (`shot.dirty`) özgün
  görsele geri yazılır, kalan pikseller bit bit korunur.
- Sayfadaki `?v=N` sorgu eki görsel değiştikçe artırılmalıdır, yoksa
  tarayıcı eskisini gösterir.
