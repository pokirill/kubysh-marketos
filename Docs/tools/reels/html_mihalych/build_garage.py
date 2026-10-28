"""Рилс «Михалыч в гараже» (2D, без Higgsfield): garage.html → кадры Playwright → mp4.
Запуск из этой папки:  python3 build_garage.py <клон pokirill/site>
Делает две версии: mihalych_garage.mp4 (курит, траты: бутылочка, сиги, огурцы) и mihalych_garage_tea.mp4 (чай)."""
import base64, io, os, subprocess, sys
from PIL import Image
site = sys.argv[1] if len(sys.argv) > 1 else "../../../../site"
def b64(p, fmt, **kw):
    b = io.BytesIO(); Image.open(p).convert("RGB").save(b, fmt, **kw); return base64.b64encode(b.getvalue()).decode()
a = {"SCR": "data:image/jpeg;base64," + b64(site + "/landing/img/poluchka-1-7.webp", "JPEG", quality=90),
     "ICO": "data:image/png;base64," + b64(site + "/landing/icon-192.png", "PNG")}
s = open("garage.html").read()
for k, v in a.items(): s = s.replace("{{%s}}" % k, v)
open("g.html", "w").write(s); page = os.path.abspath("g.html")
for mode, out, extra in (("smoke", "mihalych_garage.mp4", ""), ("tea", "mihalych_garage_tea.mp4", "&tea")):
    subprocess.run([sys.executable, "synth2.py", mode, f"audio_{mode}.wav"], check=True)
    subprocess.run(["node", "rec2.js", page, out, extra, f"audio_{mode}.wav"], check=True)
