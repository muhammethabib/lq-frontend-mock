"""Google Fonts paketini yerelleştirir: fonts/gf-local.css üretir.

Sitenin kullandığı aileleri Google Fonts'tan woff2 olarak indirir ve
CSS'in içine base64 gömer. Böylece hem render.js hem de sayfa denetimi,
ağ erişimi olmadan (ve TLS ayarlarıyla uğraşmadan) gerçek fontlarla çalışır.

Kullanım:  python3 fetch-fonts.py
"""
import base64, os, re, subprocess, sys

SC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SC, 'fonts')

# Sitede kullanılan aileler ve ağırlıklar (index.html + pages/*.html birleşimi)
URL = ('https://fonts.googleapis.com/css2'
       '?family=Noto+Naskh+Arabic:wght@400;500;600;700'
       '&family=Inter:wght@300;400;500;600;700;800;900'
       '&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400'
       '&family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;0,900;1,600;1,700'
       '&family=Merriweather:wght@700'
       '&display=swap')

# woff2 sunulması için modern bir tarayıcı kimliği gerekir
UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/120.0.0.0 Safari/537.36')


def curl(url):
    r = subprocess.run(['curl', '-sSL', '-A', UA, url], capture_output=True)
    if r.returncode:
        raise SystemExit('indirilemedi: %s\n%s' % (url, r.stderr.decode()[-500:]))
    return r.stdout


def main():
    os.makedirs(OUT, exist_ok=True)
    css = curl(URL).decode('utf-8')
    open(os.path.join(OUT, 'gf.css'), 'w').write(css)

    urls = sorted(set(re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', css)))
    print('%d @font-face, %d woff2 dosyası' % (css.count('@font-face'), len(urls)))
    blobs = {}
    for i, u in enumerate(urls, 1):
        blobs[u] = base64.b64encode(curl(u)).decode('ascii')
        sys.stdout.write('\r  %d/%d' % (i, len(urls))); sys.stdout.flush()
    print()

    local = re.sub(r'url\((https://fonts\.gstatic\.com/[^)]+)\)',
                   lambda m: 'url(data:font/woff2;base64,%s)' % blobs[m.group(1)], css)
    p = os.path.join(OUT, 'gf-local.css')
    open(p, 'w').write(local)
    print('yazıldı: %s (%.1f MB)' % (p, os.path.getsize(p) / 1e6))


if __name__ == '__main__':
    main()
