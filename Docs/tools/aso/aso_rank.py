import json,urllib.request,urllib.parse,sys,concurrent.futures as cf
APP=6778792103
def rank(t):
    u="https://itunes.apple.com/search?"+urllib.parse.urlencode({"term":t,"country":__import__("os").environ.get("CC","ru"),"entity":"software","limit":50})
    try: d=json.load(urllib.request.urlopen(u,timeout=20))
    except Exception as e: return t,"err",0
    ids=[r["trackId"] for r in d["results"]]
    pos=ids.index(APP)+1 if APP in ids else None
    weak=sum(1 for r in d["results"][:10] if r.get("userRatingCount",0)<100)
    return t,pos,weak
def hints(t):
    u="https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints?"+urllib.parse.urlencode({"clientApplication":"Software","term":t})
    r=urllib.request.Request(u,headers={"X-Apple-Store-Front":"143469-16,29","User-Agent":"AppStore/3.0 iOS/17.0"})
    try:
        b=urllib.request.urlopen(r,timeout=20).read().decode()
        import re; return re.findall(r"<key>term</key>\s*<string>([^<]+)</string>",b)
    except Exception as e: return ["err "+str(e)[:40]]
mode=sys.argv[1]; terms=sys.argv[2:]
with cf.ThreadPoolExecutor(8) as ex:
    if mode=="rank":
        for t,p,w in ex.map(rank,terms): print(f"{t:32} pos={p} weak_top10={w}")
    else:
        for t,h in zip(terms,ex.map(hints,terms)): print(t,"->",", ".join(h[:8]))
