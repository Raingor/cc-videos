#!/usr/bin/env python3
"""
Download every sticker from packs.json into line-stickers/<packid-slug>/.

- Static packs  -> PNG (sticker.png / sticker@2x.png)
- Animated packs-> APNG (sticker_animation@2x.png); static fallback kept too
- Skips files already on disk, so it is safe to re-run to resume.

Usage:
    python3 download_all.py            # download all packs in packs.json
    python3 download_all.py 16024      # only packs whose id/slug matches
"""
import json
import os
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PACKS_JSON = os.path.join(HERE, "packs.json")
BASE = os.path.join(HERE, "line-stickers")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/145.0 Safari/537.36")

# Try in order; first URL that returns >1KB wins.
URL_TPLS = [
    "https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/iPhone/sticker_animation@2x.png",  # noqa: animated
    "https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/iPhone/sticker@2x.png",           # noqa: static hi-res
    "https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/android/sticker.png",             # noqa: static alt
]


# Prefer the local proxy when it is up (measurably faster than direct).
def pick_proxy():
    for host, port in (("127.0.0.1", 7897), ("127.0.0.1", 7890)):
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return f"http://{host}:{port}"
        except OSError:
            continue
    return None


PROXY = pick_proxy()


def curl(url, dst, timeout=25):
    cmd = ["curl", "-sL", "--max-time", str(timeout), "-A", UA]
    if PROXY:
        cmd += ["--proxy", PROXY]
    cmd += [url, "-o", dst]
    r = subprocess.run(cmd, check=False)
    return r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 1000


def download_pack(pack):
    out_dir = os.path.join(BASE, pack["dir"])
    os.makedirs(out_dir, exist_ok=True)
    ok = fail = skip = 0
    anim_ext = pack.get("animated") or pack.get("hasAnimation")
    for i, sid in enumerate(pack["sticker_ids"]):
        base = os.path.join(out_dir, sid)
        static_png = base + ".png"
        anim_png = base + "_anim.png"
        if os.path.exists(static_png) and os.path.getsize(static_png) > 1000:
            skip += 1
        else:
            got = False
            for tpl in URL_TPLS[1:]:
                if curl(tpl.format(sid=sid), static_png):
                    got = True
                    break
            ok += 1 if got else 0
            fail += 0 if got else 1
            if not got and os.path.exists(static_png):
                os.remove(static_png)
        # animation file (only meaningful for animated packs)
        if anim_ext and not (os.path.exists(anim_png)
                             and os.path.getsize(anim_png) > 1000):
            if curl(URL_TPLS[0].format(sid=sid), anim_png):
                ok += 1
            elif os.path.exists(anim_png):
                os.remove(anim_png)
        # gentle pacing to stay polite
        if i % 10 == 9:
            time.sleep(0.3)
    return ok, fail, skip


def main():
    packs = json.load(open(PACKS_JSON, encoding="utf-8"))
    args = sys.argv[1:]
    if args:
        packs = [p for p in packs
                 if any(a in (p["id"], p.get("slug", ""), p.get("dir", ""))
                        or a in p.get("title_en", "") for a in args)]
    print(f"packs to download: {len(packs)}")
    grand_ok = grand_fail = 0
    for pack in packs:
        ok, fail, skip = download_pack(pack)
        grand_ok += ok
        grand_fail += fail
        print(f"[{pack['dir']}] ok={ok} skip={skip} fail={fail}", flush=True)
    print(f"\n完成: 新增 {grand_ok} 张, 失败 {grand_fail} 张")
    print(f"目录: {BASE}")


if __name__ == "__main__":
    main()
