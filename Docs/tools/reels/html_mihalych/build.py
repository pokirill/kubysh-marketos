"""Сборка рилса «Михалыч на льду» без Higgsfield: HTML-анимация → кадры Playwright → mp4 (ffmpeg).
Запуск из этой папки:  python3 build.py /путь/к/клону/pokirill/site  →  mihalych.html, audio.wav, mihalych.mp4
Картинки: mih.jpg (Михалыч), экран «Получки» и иконка — из лендинга (site/landing)."""
import base64, io, subprocess, sys
from PIL import Image
site = sys.argv[1] if len(sys.argv) > 1 else "../../../../site"
def b64(p, fmt, **kw):
    b = io.BytesIO(); Image.open(p).convert("RGB").save(b, fmt, **kw); return base64.b64encode(b.getvalue()).decode()
a = {"MIH": "data:image/jpeg;base64," + b64("mih.jpg", "JPEG", quality=90),
     "SCR": "data:image/jpeg;base64," + b64(site + "/landing/img/poluchka-1-7.webp", "JPEG", quality=90),
     "ICO": "data:image/png;base64," + b64(site + "/landing/icon-192.png", "PNG")}
s = open("template.html").read()
for k, v in a.items(): s = s.replace("{{%s}}" % k, v)
open("mihalych.html", "w").write(s)
subprocess.run([sys.executable, "synth.py"], check=True)
subprocess.run(["node", "rec.js", __import__("os").path.abspath("mihalych.html"), "mihalych.mp4"], check=True)
