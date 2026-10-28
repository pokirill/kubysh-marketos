"""Озвучка рилса «Михалыч в гараже»: реплики (wav) → сиплый Михалыч, тайминги, растяжка сюжета, титры, огибающие ртов.
python3 vo_build.py <папка с wav> <smoke|tea> <words.json> → vo.json (в страницу) и vo_track.wav (голоса)."""
import json, sys, wave, numpy as np
SR = 48000
src, mode, wj = sys.argv[1], sys.argv[2], sys.argv[3]
T = mode == "tea"; W = json.load(open(wj))
def rd(n):
    w = wave.open(f"{src}/{n}.wav"); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768; return x
def lp(x, a):
    y = np.zeros(len(x)); 
    for k in range(1, len(x)): y[k] = y[k-1] + a * (x[k] - y[k-1])
    return y
def env(x, win=480):
    n = len(x) // win; r = np.sqrt((x[:n*win].reshape(n, win) ** 2).mean(1)); return r
TEMPO = 1.15  # Михалыч чуть быстрее (Кирилл 28.10: «слишком медленно»)
# Поддатый голос без баса и сиплости: срез низов, плавающая интонация (медленное вибрато тона) и легкая «качка».
DRUNK = "highpass=f=150,equalizer=f=220:t=q:w=1.2:g=-5,atempo=%.2f,vibrato=f=0.9:d=0.22,vibrato=f=5:d=0.04,tremolo=f=1.3:d=0.12" % TEMPO
import subprocess, os
def drunk(n):
    out = f"/tmp/{n}_drunk.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{src}/{n}.wav", "-af", DRUNK, "-ar", "48000", "-ac", "1", out], check=True)
    w = wave.open(out); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    return x / max(1e-6, np.abs(x).max()) * 0.95
M = ["m1t", "m2t", "m3t", "m4"] if T else ["m1", "m2", "m3", "m4"]
lines = {"m1": M[0], "m2": M[1], "m3": M[2], "m4": "m4", "k1": "k1", "k2": "k2", "k3": "k3", "k4": "k4", "k5": "k5"}
slots = [("m1", .1, 2.6, .15), ("m2", 2.9, 5.6, .15), ("m3", 5.6, 7.6, .1), ("k1", 7.9, 9.6, .15), ("k2", 11.0, 13.5, .2),
         ("k3", 13.6, 18.9, .15), ("m4", 19.2, 20.95, .2), ("k4", 21.0, 22.9, .1), ("k5", 23.0, 26.6, .8)]
def wt(n, pre):
    for w, a, b in W[n]:
        if w.lower().strip(",.!?–—").startswith(pre): return a / (TEMPO if n.startswith("m") else 1)
    raise SystemExit(f"нет слова {pre} в {n}")
inner = {"k1": [("как", 8.55)], "k2": [("считаю", 12.2)]}
aud = {k: (drunk(v) if k.startswith("m") else rd(v) * 0.95) for k, v in lines.items()}
R, o, warp, place = 0.0, 0.0, [[0.0, 0.0]], {}
for k, a, b, lead in slots:
    R += a - o; t0 = R; d = len(aud[k]) / SR
    L = max(b - a, lead + d + .35)
    if (t0, a) != tuple(warp[-1]): warp.append([t0, a])
    for pre, old in inner.get(k, []): warp.append([t0 + lead + wt(lines[k], pre), old])
    warp.append([t0 + L, b]); place[k] = t0 + lead; R = t0 + L; o = b
R += 27 - o; warp.append([R, 27.0]); D = round(R, 2)
N = int(D * SR) + SR; vo = np.zeros(N); vm = np.zeros(N); vk = np.zeros(N)
for k, t0 in place.items():
    i = int(t0 * SR); x = aud[k]; vo[i:i+len(x)] += x; (vm if k.startswith("m") else vk)[i:i+len(x)] += x
def env100(x):
    e = env(x, 480); e = np.convolve(e, np.ones(3) / 3, "same"); return e / max(1e-6, e.max())
eM, eK = env100(vm), env100(vk)
act = np.convolve((eM > .1).astype(float), np.ones(80) / 80, "same")
P = place; m = lambda k, pre: P[k] + wt(lines[k], pre)
caps = [[P["m1"], m("m1", "а"), "Пять дней до получки, *обалдеть*" if T else "Пять дней до получки, *охренеть*", "red"],
        [m("m1", "а"), P["m1"] + len(aud["m1"]) / SR + .3, "А еще Семенычу *должок* отдать"],
        [P["m2"], P["m2"] + len(aud["m2"]) / SR + .3, "Ну огурчики, ну *по мелочи*" if T else "Бутылочка, ну сиги, ну *по мелочи*"],
        [P["m3"], m("m3", "ох" if T else "сран"), "А сколько осталось, *непонятно*", "red"],
        [m("m3", "ох" if T else "сран"), P["m3"] + len(aud["m3"]) / SR + .3, "*Ох уж эти* банки" if T else "*Сраные* банки", "red"],
        [m("k1", "как"), P["k1"] + len(aud["k1"]) / SR + .3, "как *в тумане*"],
        [P["k3"], m("k3", "и"), "Смотри, сегодня можно еще ≈3 400 ₽", "grn"],
        [m("k3", "и"), P["k3"] + len(aud["k3"]) / SR + .3, "И до получки *хватает*", "grn"]]
r = lambda a: [round(float(v), 3) for v in a]
json.dump({"D": D, "warp": [[round(a, 3), b] for a, b in warp], "caps": [[round(c[0], 3), round(c[1], 3)] + c[2:] for c in caps],
           "envM": r(eM), "envK": r(eK), "actM": r(act), "place": P}, open("vo.json", "w"), ensure_ascii=False)
pcm = (np.clip(vo, -1, 1) * 32767).astype(np.int16); w = wave.open("vo_track.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print("D", D, "place", {k: round(v, 2) for k, v in P.items()})
