"""Живые жабы поверх клипов (замечание Кирилла 12.10: «не надуваются пузырьками, а открывают рот»).
Кадры: cut_<who>.png (база), cut_<who>_mouth.png (приоткрытый рот), cut_<who>_blink.png (моргание) — `frogcut.py`.
Рот открывается по громкости собственной реплики (окно 50 мс), в паузах закрыт; моргание раз в ~3 с, когда молчит;
дыхание ±1,2 %, при речи — лёгкое покачивание головой ±2°. Вход — прыжок с отскоком."""
import math
from PIL import Image
from studio import back, ease, seg, scaled, comp
import audio

REF = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/Референсы/"


def load(who):
    f = lambda tag: Image.open(REF + f"cut_{who}{tag}.png").convert("RGBA")
    return {"base": f(""), "mouth": f("_mouth"), "blink": f("_blink")}


class Mascot:
    def __init__(self, ep, who, x, y, s, t0, t1, blink_phase=0.0):
        self.ep, self.who, self.x, self.y, self.s, self.t0, self.t1 = ep, who, x, y, s, t0, t1
        self.fr = load(who); self.lines = []; self.bp = blink_phase
        ep.add(t0, t1, "screen", self.draw); ep.sfx(t0, "pop", 0.4)

    def say(self, a, b):
        """Реплика уже добавлена через ep.say: берём ее сэмплы из ep.voice по времени начала."""
        smp = next(s for t, s in self.ep.voice if abs(t - a) < 1e-6)
        blk = audio.SR // 100  # огибающая блоками по 10 мс, сглаженная по 5 блокам (50 мс)
        raw = [math.sqrt(sum(v * v for v in smp[i:i + blk]) / blk) for i in range(0, len(smp), blk)]
        env = [sum(raw[max(0, j - 2):j + 3]) / len(raw[max(0, j - 2):j + 3]) for j in range(len(raw))]
        self.lines.append((a, b, env, max(env) or 1.0))

    def _talk(self, t):
        for a, b, env, peak in self.lines:
            if a <= t < b:
                i = min(len(env) - 1, int((t - a) * 100))
                return env[i] / peak
        return None

    def draw(self, img, t, cam):
        k = self.s * back(seg(t, self.t0, self.t0 + 0.35)) * (1 - ease(seg(t, self.t1 - 0.25, self.t1)))
        if k < 0.02: return
        lvl = self._talk(t)
        if lvl is not None:
            frame = "mouth" if lvl > 0.28 else "base"
            rot = 2.0 * math.sin((t - self.t0) * 5.5); k *= 1 + 0.015 * lvl
        else:
            frame = "blink" if ((t + self.bp) % 3.1) < 0.12 else "base"
            rot = 0.0
        k *= 1 + 0.012 * math.sin(t * 2 * math.pi * 0.55)
        hop = -40 * math.sin(math.pi * seg(t, self.t0, self.t0 + 0.35))
        im = scaled(self.fr[frame], k, rot)
        comp(img, im, self.x - im.width / 2, self.y - im.height + hop)
