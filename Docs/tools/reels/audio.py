"""Звук рилсов: эффекты синтезируем сами (лицензионно чисто), голос — edge-tts, микс в WAV 48 кГц моно.

Русские голоса edge-tts из РФ не отдают звук (проверено 03.10.2026), работают многоязычные:
Кубыш — de-DE-FlorianMultilingualNeural (выбор Кирилла 03.10), Душная — de-DE-SeraphinaMultilingualNeural. Читают русский текст.
"""
import array, asyncio, base64, json, math, os, random, subprocess, urllib.request, wave

SR = 48000
# Кастинги: edge — бесплатные многоязычные (с акцентом), yandex — SpeechKit v3 (носители, ключ в YandexSpeechKit.env.txt)
CASTS = {
    "edge": {"kubysh": ("edge", "de-DE-FlorianMultilingualNeural", "+6%", "+20Hz"),
             "dush": ("edge", "en-US-EmmaMultilingualNeural", "-8%", "-16Hz"),
             "ksy": ("edge", "en-US-AvaMultilingualNeural", "+4%", "+0Hz")},
    "yandex": {"kubysh": ("yandex", "kirill", "good", 1.05),      # выбор Кирилла 03.10: голос 5
               "dush": ("yandex", "omazh", "evil", 1.0),          # выбор Кирилла 03.10: голос 4
               "ksy": ("yandex", "alena", "neutral", 1.05)},      # черновой голос Ксюши до живой записи
}
CAST = CASTS["edge"]
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "YandexSpeechKit.env.txt")


def _env(n, a=0.004, d=0.2):
    na = max(1, int(a * SR)); out = []
    for i in range(n):
        out.append(min(1.0, i / na) * math.exp(-max(0, i - na) / (d * SR)))
    return out


def _noise(n, seed):
    r = random.Random(seed); return [r.uniform(-1, 1) for _ in range(n)]


def _lp(x, k):
    y = 0.0; out = []
    for v in x:
        y += k * (v - y); out.append(y)
    return out


def sfx(name):
    if name == "clink":
        n = int(0.5 * SR); out = [0.0] * n
        for delay, g in ((0, 1.0), (0.07, 0.45)):
            o = int(delay * SR); e = _env(n - o, 0.001, 0.16)
            for i in range(n - o):
                t = i / SR
                out[o + i] += g * e[i] * (math.sin(2 * math.pi * 2637 * t) + .6 * math.sin(2 * math.pi * 3951 * t)
                                          + .4 * math.sin(2 * math.pi * 5274 * t) + .25 * math.sin(2 * math.pi * 7034 * t)) / 2.25
        return out
    if name == "thwip":
        n = int(0.12 * SR); e = _env(n, 0.002, 0.04); ph = 0; nz = _lp(_noise(n, 1), 0.3); out = []
        for i in range(n):
            f = 1400 - 1100 * i / n; ph += 2 * math.pi * f / SR; out.append(e[i] * (0.8 * math.sin(ph) + 0.3 * nz[i]))
        return out
    if name == "crunch":
        out = []
        for k in range(3):
            n = int(0.05 * SR); e = _env(n, 0.001, 0.015); nz = _lp(_noise(n, 10 + k), 0.45)
            out += [e[i] * nz[i] * (1 - 0.2 * k) * 1.6 for i in range(n)] + [0.0] * int(0.05 * SR)
        return out
    if name == "gulp":
        n = int(0.2 * SR); e = _env(n, 0.01, 0.09); ph = 0; out = []
        for i in range(n):
            f = 420 - 280 * i / n; ph += 2 * math.pi * f / SR; out.append(0.9 * e[i] * math.sin(ph))
        return out
    if name == "boing":
        n = int(0.38 * SR); e = _env(n, 0.003, 0.14); ph = 0; out = []
        for i in range(n):
            t = i / SR; f = 170 + 260 * min(1, t / 0.12) + 25 * math.sin(2 * math.pi * 16 * t); ph += 2 * math.pi * f / SR
            out.append(0.7 * e[i] * math.sin(ph))
        return out
    if name == "whoosh":
        n = int(0.36 * SR); nz = _noise(n, 5); out = []; y = 0.0
        for i in range(n):
            t = i / n; k = 0.04 + 0.25 * math.sin(math.pi * t); y += k * (nz[i] - y); out.append(0.9 * math.sin(math.pi * t) ** 2 * y * 2.2)
        return out
    if name == "pop":
        n = int(0.07 * SR); e = _env(n, 0.004, 0.025); ph = 0; out = []
        for i in range(n):
            f = 620 - 260 * i / n; ph += 2 * math.pi * f / SR; out.append(0.35 * e[i] * math.sin(ph))
        return out
    if name == "ding":
        n = int(0.6 * SR); e = _env(n, 0.008, 0.2)
        return [0.2 * e[i] * (math.sin(2 * math.pi * 784 * i / SR) + 0.35 * math.sin(2 * math.pi * 1175 * i / SR)) for i in range(n)]
    if name == "hop":
        n = int(0.12 * SR); e = _env(n, 0.002, 0.04); ph = 0; out = []
        for i in range(n):
            f = 260 - 120 * i / n; ph += 2 * math.pi * f / SR; out.append(0.5 * e[i] * math.sin(ph))
        return out
    if name == "swish":
        n = int(0.22 * SR); nz = _noise(n, 9); out = []; y = 0.0
        for i in range(n):
            t = i / n; k = 0.08 + 0.4 * t; y += k * (nz[i] - y); out.append(0.7 * math.sin(math.pi * t) ** 2 * y * 2)
        return out
    if name == "scribble":
        out = []; r = random.Random(4)
        for k in range(7):
            n = int(r.uniform(0.04, 0.08) * SR); nz = _noise(n, 20 + k); y = 0.0
            for i in range(n):
                y += 0.6 * (nz[i] - y); out.append(0.35 * math.sin(math.pi * i / n) * (nz[i] - y))
            out += [0.0] * int(0.02 * SR)
        return out
    if name == "thump":
        n = int(0.25 * SR); e = _env(n, 0.001, 0.07); ph = 0; nz = _lp(_noise(n, 30), 0.2); out = []
        for i in range(n):
            f = 110 - 50 * i / n; ph += 2 * math.pi * f / SR; out.append(e[i] * (0.9 * math.sin(ph) + 0.5 * nz[i]))
        return out
    if name == "marker":
        n = int(0.32 * SR); nz = _noise(n, 40); out = []; y = 0.0
        for i in range(n):
            y += 0.35 * (nz[i] - y); out.append(0.25 * math.sin(math.pi * i / n) * (nz[i] - y))
        return out
    if name == "tick":
        n = int(0.04 * SR); e = _env(n, 0.003, 0.01)
        return [0.18 * e[i] * math.sin(2 * math.pi * 900 * i / SR) for i in range(n)]
    if name == "msg":
        out = []
        for f, d in ((523, 0.08), (659, 0.12)):
            n = int(d * SR); e = _env(n, 0.006, d / 3); out += [0.22 * e[i] * math.sin(2 * math.pi * f * i / SR) for i in range(n)]
        return out
    if name == "boom":
        n = int(0.9 * SR); e = _env(n, 0.003, 0.3); ph = 0; nz = _lp(_noise(n, 50), 0.05); out = []
        for i in range(n):
            f = 70 - 30 * i / n; ph += 2 * math.pi * f / SR; out.append(e[i] * (0.9 * math.sin(ph) + 0.6 * nz[i]))
        return out
    if name == "kaching":
        out = sfx("tick") + [0.0] * int(0.04 * SR)
        n = int(0.7 * SR); e = _env(n, 0.002, 0.25)
        out += [0.35 * e[i] * (math.sin(2 * math.pi * 2093 * i / SR) + 0.6 * math.sin(2 * math.pi * 2637 * i / SR) + 0.4 * math.sin(2 * math.pi * 3136 * i / SR)) for i in range(n)]
        return out
    if name == "heartbeat":
        out = []
        for g in (1.0, 0.7):
            n = int(0.16 * SR); e = _env(n, 0.004, 0.05); out += [g * e[i] * math.sin(2 * math.pi * 55 * i / SR) for i in range(n)] + [0.0] * int(0.1 * SR)
        return out
    if name == "room":  # тихий гул кофейни/помещения, 30 с
        n = int(30 * SR); nz = _noise(n, 77); out = []; y = 0.0; z = 0.0
        for i in range(n):
            y += 0.02 * (nz[i] - y); z += 0.3 * (nz[i] - z); out.append(0.9 * y + 0.04 * z)
        return out
    if name == "beep":  # писк терминала оплаты
        out = []
        for d in (0.09, 0.09):
            m = int(d * SR); e = _env(m, 0.003, 0.05); out += [0.35 * e[i] * math.sin(2 * math.pi * 2350 * i / SR) for i in range(m)] + [0.0] * int(0.05 * SR)
        return out
    raise ValueError(name)


def yandex_tts(text, voice, role, speed, out_wav):
    """SpeechKit API v3 (REST): ответ — поток JSON-объектов с кусками WAV в base64."""
    key = open(KEY_PATH).read().strip()
    hints = [{"voice": voice}] + ([{"role": role}] if role else []) + [{"speed": str(speed)}]
    body = json.dumps({"text": text, "hints": hints, "loudnessNormalizationType": "LUFS",
                       "outputAudioSpec": {"containerAudio": {"containerAudioType": "WAV"}}}).encode()
    req = urllib.request.Request("https://tts.api.cloud.yandex.net/tts/v3/utteranceSynthesis", data=body,
                                 headers={"Authorization": "Api-Key " + key, "Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=60).read().decode()
    dec = json.JSONDecoder(); i = 0; chunks = []
    while i < len(raw):
        while i < len(raw) and raw[i].isspace(): i += 1
        if i >= len(raw): break
        obj, i = dec.raw_decode(raw, i)
        chunks.append(base64.b64decode(obj["result"]["audioChunk"]["data"]))
    with open(out_wav, "wb") as f: f.write(b"".join(chunks))


def tts(text, who, out_path):
    c = CAST[who]
    if c[0] == "yandex":
        yandex_tts(text, c[1], c[2], c[3], out_path)
    else:
        import edge_tts, re
        text = re.sub(r"\+([аеёиоуыэюяАЕЁИОУЫЭЮЯ])", "\\1\u0301", text)
        asyncio.run(edge_tts.Communicate(text, c[1], rate=c[2], pitch=c[3]).save(out_path))


def load(path):
    """Любой аудиофайл → список float, 48 кГц моно (через afconvert)."""
    wav = path.rsplit(".", 1)[0] + "_48k.wav"
    if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(path):  # исходник новее кэша — пересчитать
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@48000", "-c", "1", path, wav], check=True)
    try:
        with wave.open(wav) as w:
            a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
    except wave.Error:  # WAVE_FORMAT_EXTENSIBLE от afconvert: внутри тот же PCM 16 бит моно
        b = open(wav, "rb").read(); i = b.find(b"data")
        n = int.from_bytes(b[i + 4:i + 8], "little"); a = array.array("h"); a.frombytes(b[i + 8:i + 8 + n - n % 2])
    # срезаем тишину по краям, чтобы реплика начиналась ровно в свою секунду
    th = 300; i0 = next((i for i, v in enumerate(a) if abs(v) > th), 0); i1 = len(a) - next((i for i, v in enumerate(reversed(a)) if abs(v) > th), 0)
    return [v / 32768 for v in a[max(0, i0 - 480):min(len(a), i1 + 2400)]]


def voice(text, who, cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
    import hashlib
    c = CAST[who]
    key = f"{who}_{hashlib.md5(repr((text, c)).encode()).hexdigest()[:10]}"
    path = os.path.join(cache_dir, key + (".wav" if c[0] == "yandex" else ".mp3"))
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        tts(text, who, path)
    return load(path)


def envelope(samples, fps=30):
    """Громкость по кадрам 0..1 — двигает рот/челюсть в такт голосу."""
    hop = SR // fps; out = []
    for i in range(0, len(samples), hop):
        seg = samples[i:i + hop]; out.append(math.sqrt(sum(v * v for v in seg) / max(1, len(seg))))
    m = max(out) if out else 1
    return [min(1.0, v / (0.6 * m)) for v in out]


def mix(events, dur, out_wav):
    """events: (секунда, сэмплы, громкость). Мягкий лимитер, 16 бит."""
    n = int(dur * SR); buf = array.array("f", [0.0]) * n
    for t, smp, g in events:
        o = int(t * SR)
        for i, v in enumerate(smp):
            j = o + i
            if 0 <= j < n: buf[j] += v * g
    pcm = array.array("h", (int(32000 * math.tanh(v * 1.1)) for v in buf))
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def mux(video, wav, out):
    """Склеить видео из mp4enc и звук: WAV → AAC, затем mux (AVFoundation, без ffmpeg)."""
    m4a = wav.rsplit(".", 1)[0] + ".m4a"
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "192000", wav, m4a], check=True)
    tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mux")
    subprocess.run([tool, video, m4a, out], check=True)


def beat(dur, bpm=100, start_hit=True):
    """Синтетическая подложка lo-fi: бочка, хлопок на 2 и 4, хэт восьмыми, бас и мягкий пэд Am–F–C–G.
    Своя, без лицензий. Громкость сводить низко (0.25–0.35), под голосами еще ниже через Ep.duck."""
    import random
    random.seed(7)
    n = int(dur * SR); out = [0.0] * n; beat_s = 60 / bpm
    def add(t, sig, g):
        o = int(t * SR)
        for i, v in enumerate(sig):
            if o + i < n: out[o + i] += v * g
    kick = [math.sin(2 * math.pi * (45 + 75 * math.exp(-i / SR * 18)) * i / SR) * math.exp(-i / SR * 9) for i in range(int(0.35 * SR))]
    clap = [(random.random() * 2 - 1) * math.exp(-i / SR * 28) for i in range(int(0.18 * SR))]
    hat = [(random.random() * 2 - 1) * math.exp(-i / SR * 90) for i in range(int(0.05 * SR))]
    hp = 0.0; hat2 = []
    for v in hat: hp = 0.6 * hp + v; hat2.append(v - hp * 0.6)
    roots = [57, 53, 48, 55]; chords = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = 4 * beat_s; t = 0.0; k = 0
    while t < dur:
        r = roots[k % 4]; ch = chords[k % 4]
        for b in range(4):
            tb = t + b * beat_s
            if b in (0, 2) or (b == 3 and k % 2): add(tb, kick, 0.9)
            if b in (1, 3): add(tb, clap, 0.35)
            add(tb, hat2, 0.12); add(tb + beat_s / 2, hat2, 0.08)
        bass = [math.sin(2 * math.pi * f(r - 12) * i / SR) * min(1, i / 400) * math.exp(-i / SR * 1.2) for i in range(int(bar * SR))]
        add(t, bass, 0.35)
        L = int(bar * SR); pad = [0.0] * L; lp = 0.0
        for i in range(L):
            x = sum(((f(m + 12) * i / SR + d) % 1.0) * 2 - 1 for m in ch for d in (0.0, 0.31)) / 6
            lp += (x - lp) * 0.04
            pad[i] = lp * min(1, i / (0.3 * SR)) * min(1, (L - i) / (0.2 * SR))
        add(t, pad, 0.22)
        t += bar; k += 1
    if start_hit:
        add(0.0, [(random.random() * 2 - 1) * math.exp(-i / SR * 6) for i in range(int(0.6 * SR))], 0.25)
    m = max(1e-6, max(abs(v) for v in out))
    return [v / m * 0.9 for v in out]
