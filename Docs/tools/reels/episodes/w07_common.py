"""Общее для роликов недели W03+: аватары-метки, реплика с липсинком рига, финал с обещанием."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import audio
from episodes.scr import STY, RK
from episodes.lib import PHONE

V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"


def badge(txt, col):
    im = Image.new("RGBA", (104, 104), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 101, 101], fill=col + (255,), outline=(255, 255, 255, 255), width=5)
    d.text((52, 54), txt, font=PH.font("Bold", 38 if len(txt) > 1 else 50), fill=(255, 255, 255), anchor="mm"); return im


def setup(ep):
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    ep.avatars["hero"] = badge("ТЫ", (230, 120, 40))


def sayer(ep, V, Y=1100, SZ=54):
    def say(who, f, cap, at=None, a=None, v=None):
        t0, t1 = ep.say(who, "", cap=cap, at=at, y=Y, size=SZ, file=(v or V) + f + "_t_48k.wav")
        if a is not None:
            smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
            for i, x in enumerate(env):
                if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], x)
        return t0, t1
    return say


def finale(ep, say, at, actors=(), pill_y=1420):
    h0, h1 = say("kubysh", "w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=at, v=V3)
    end = h1 + 1.4
    for a in actors: a.show(h0 - 0.05, False)
    ep.clip(h0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - h0)))
    ep.pill(h0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, pill_y, size=46, **STY["green"]); ep.sfx(h0 + 1.0, "pop", 0.4)
    ep.dur = end
    return h0
