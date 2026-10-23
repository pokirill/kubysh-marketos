"""Загрузка видео-превью (App Preview) в App Store Connect ключом API.
python3 asc_preview.py <версия> <файл.mp4> [preview_type=IPHONE_67] [locale=ru]
Шаги: версия → локализация → appPreviewSets (создать при отсутствии) → резерв appPreviews → PUT частей → PATCH uploaded+md5.
Видео: H.264, 886×1920 (6,7"/6,9"), до 30 с, со звуковой дорожкой (можно тихой)."""
import base64, hashlib, json, os, subprocess, sys, time, urllib.request

KEY = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/fastlane/AuthKey_35A4N9KDXZ.p8"
KID, ISS, APP = "35A4N9KDXZ", "76df59ff-440e-4c9d-91c3-c749beab2fc1", "6778792103"
API = "https://api.appstoreconnect.apple.com"


def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def jwt():
    h = b64(json.dumps({"alg": "ES256", "kid": KID, "typ": "JWT"}).encode())
    p = b64(json.dumps({"iss": ISS, "iat": int(time.time()), "exp": int(time.time()) + 1100, "aud": "appstoreconnect-v1"}).encode())
    der = subprocess.run(["openssl", "dgst", "-sha256", "-sign", KEY], input=f"{h}.{p}".encode(), capture_output=True, check=True).stdout
    # DER → r||s
    i = 4 if der[1] < 0x80 else 5; rl = der[i - 1]; r = der[i:i + rl]; sl = der[i + rl + 1]; s = der[i + rl + 2:i + rl + 2 + sl]
    r = r[-32:].rjust(32, b"\0"); s = s[-32:].rjust(32, b"\0")
    return f"{h}.{p}.{b64(r + s)}"


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Bearer " + jwt(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        t = r.read(); return json.loads(t) if t else {}


def main(version, path, ptype="IPHONE_67", locale="ru"):
    v = [x for x in call("GET", f"/v1/apps/{APP}/appStoreVersions?filter[platform]=IOS&limit=20")["data"] if x["attributes"]["versionString"] == version][0]
    loc = [x for x in call("GET", f"/v1/appStoreVersions/{v['id']}/appStoreVersionLocalizations")["data"] if x["attributes"]["locale"] == locale][0]
    sets = call("GET", f"/v1/appStoreVersionLocalizations/{loc['id']}/appPreviewSets")["data"]
    ps = [s for s in sets if s["attributes"]["previewType"] == ptype]
    ps = ps[0] if ps else call("POST", "/v1/appPreviewSets", {"data": {"type": "appPreviewSets", "attributes": {"previewType": ptype},
        "relationships": {"appStoreVersionLocalization": {"data": {"type": "appStoreVersionLocalizations", "id": loc["id"]}}}}})["data"]
    data = open(path, "rb").read()
    pv = call("POST", "/v1/appPreviews", {"data": {"type": "appPreviews", "attributes": {"fileName": os.path.basename(path), "fileSize": len(data), "mimeType": "video/mp4", "previewFrameTimeCode": "00:00:00:01"},
        "relationships": {"appPreviewSet": {"data": {"type": "appPreviewSets", "id": ps["id"]}}}}})["data"]
    for op in pv["attributes"]["uploadOperations"]:
        req = urllib.request.Request(op["url"], method=op["method"], data=data[op["offset"]:op["offset"] + op["length"]],
                                     headers={h["name"]: h["value"] for h in op["requestHeaders"]})
        urllib.request.urlopen(req).read()
    call("PATCH", f"/v1/appPreviews/{pv['id']}", {"data": {"type": "appPreviews", "id": pv["id"], "attributes": {"uploaded": True, "sourceFileChecksum": hashlib.md5(data).hexdigest()}}})
    print("загружено:", version, locale, ptype, pv["id"], "· версия в состоянии", v["attributes"]["appStoreState"])


if __name__ == "__main__":
    main(*sys.argv[1:])
