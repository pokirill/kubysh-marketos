"""Сюжетный рилс с героем (К5, М1 и дальше): реплики идут подряд, у каждой свои кадры.
seg = dict(who, vo, cap, vis=[(path, src, speed, phone?)...] — делят время реплики поровну или по долям share,
pills=[(доля начала, текст, y, стиль)], hook=True — этот кусок целиком идет холодным открытием).
Финал A/B — как в scr.py, без «напиши „план“» (Кирилл 20.10: в комментариях никто не пишет)."""
from PIL import Image
from studio import *  # noqa
from episodes.scr import STY, CTA, VO, PH, RK, icon
from episodes.lib import PHONE

Y = 1560


def make(name, segs, cta, hook_text, hook_y=250, kub_cta=PHONE):
    ep = Ep(f"{name}_{cta}", "studio"); ep.sfxgain = 0.4
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush", "friend", "max")}
    t, hk = 0.1, None
    for s in segs:
        a0, a1 = ep.say(s["who"], "", cap=s["cap"], y=Y, size=s.get("size", 60), at=t, file=VO + s["vo"] + "_f_48k.wav")
        end = a1 + s.get("tail", 0.2); vis = s["vis"]; sh = s.get("share") or [1 / max(1, len(vis))] * len(vis)
        x0 = max(0.0, t - 0.1); x = x0; acc = 0.0
        for i, (v, k) in enumerate(zip(vis, sh)):
            path, src, sp = v[:3]; acc += k
            x1 = end if i == len(vis) - 1 else x0 + (end - x0) * acc
            ep.clip(x, x1, path, path.split("/")[-1], src_t0=src, speed=sp, phone=PH if len(v) > 3 else None); x = x1
        for k, txt, y, st in s.get("pills", ()):
            ep.pill(a0 + (a1 - a0) * k, end, txt, 540, y, size=50, **STY[st]); ep.sfx(a0 + (a1 - a0) * k, "pop", 0.4)
        if s.get("fn"): s["fn"](ep, t - 0.1, end)
        if s.get("hook"): hk = (a0 - 0.05, a1 + 0.15)
        ep.sfx(t, "swish", 0.3); t = end + 0.05
    e0, e1 = ep.say("kubysh", CTA[cta][0], cap=CTA[cta][1], y=Y, size=62, at=t, file=VO + ("t_02_cta_a" if cta == "A" else "t_03_cta_b") + "_f_48k.wav")
    end = e1 + 1.6
    icon(ep, e0, end, y=820, size=230)
    ep.pill(e1 - 0.4, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(e1 - 0.4, "pop", 0.4)   # обещание, итог 27.10
    ep.clip(t - 0.05, end, kub_cta, "kub_cta", speed=min(1.0, 4.9 / (end - t)))
    ep.dur = end
    if hk: ep.hook_clip(*hk, text=hook_text); ep.hook["y"] = hook_y
    return ep
