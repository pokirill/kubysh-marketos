#!/bin/bash
# Сборка озвученной версии (в облаке Higgsfield): run_vo.sh <smoke|tea> <папка wav> <words.json> <site> <out.mp4>
set -e; H=$(cd "$(dirname "$0")" && pwd); M=$1; V=$2; WJ=$3; SITE=$4; OUT=$5
W=$(mktemp -d); cd $W
python3 $H/vo_build.py $V $M $WJ
python3 $H/synth3.py $M audio.wav
python3 - "$H" "$SITE" <<'P'
import base64,io,sys,json
from PIL import Image
H,site=sys.argv[1],sys.argv[2]
def b64(p,fmt,**kw):
    b=io.BytesIO(); Image.open(p).convert("RGB").save(b,fmt,**kw); return base64.b64encode(b.getvalue()).decode()
a={"SCR":"data:image/jpeg;base64,"+b64(site+"/landing/img/poluchka-1-7.webp","JPEG",quality=90),
   "ICO":"data:image/png;base64,"+base64.b64encode(open(H+"/kubysh_icon.png","rb").read()).decode(),
   "AVA":"data:image/png;base64,"+base64.b64encode(open(H+"/kubysh_ava.png","rb").read()).decode(),
   "VO":open("vo.json").read()}
s=open(H+"/garage.html").read()
for k,v in a.items(): s=s.replace("{{%s}}"%k,v)
open("g.html","w").write(s)
P
EX=""; [ "$M" = tea ] && EX="&tea"
node $H/rec2.js $W/g.html $OUT "$EX" $W/audio.wav
echo built $OUT
