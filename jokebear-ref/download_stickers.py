#!/usr/bin/env python3
"""Download Joke Bear LINE sticker packs."""
import json
import os
import subprocess
import sys

PROXY = "http://127.0.0.1:7897"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "line-stickers")

PACKS = {
    # Custom 版 40 张 370x310（有占位符留白）
    "custom16024": {
        "meta": "https://stickershop.line-scdn.net/products/0/0/1/16024/iPhone/productInfo.meta",
        "url_tpl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/iPhone/sticker@2x.png",
    },
    # Move 动画版 24 张 370x300（静态首帧）
    "move1365252": {
        "meta": "https://stickershop.line-scdn.net/products/0/0/1/1365252/iPhone/productInfo.meta",
        "url_tpl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/iPhone/sticker@2x.png",
    },
    # Spring 静态版 40 张 259x224
    "spring1394378": {
        "meta": "https://stickershop.line-scdn.net/products/0/0/1/1394378/iPhone/productInfo.meta",
        "url_tpl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/{sid}/android/sticker.png",
    },
}

for pack_name, cfg in PACKS.items():
    out_dir = os.path.join(BASE, pack_name)
    os.makedirs(out_dir, exist_ok=True)
    meta_path = f"/tmp/meta_{pack_name}.json"
    subprocess.run(["curl", "-sL", "--proxy", PROXY, cfg["meta"], "-o", meta_path, "--max-time", "20"], check=True)
    data = json.load(open(meta_path))
    stickers = data.get("stickers", [])
    print(f"[{pack_name}] {data.get('title',{}).get('en')} — {len(stickers)} stickers")
    ok = 0
    for s in stickers:
        sid = s["id"]
        dst = os.path.join(out_dir, f"{sid}.png")
        if os.path.exists(dst) and os.path.getsize(dst) > 1000:
            ok += 1
            continue
        r = subprocess.run(
            ["curl", "-sL", "--proxy", PROXY, cfg["url_tpl"].format(sid=sid), "-o", dst, "--max-time", "20"],
            check=False,
        )
        if r.returncode == 0 and os.path.getsize(dst) > 1000:
            ok += 1
        else:
            print(f"  FAIL {sid} size={os.path.getsize(dst) if os.path.exists(dst) else 0}")
            if os.path.exists(dst):
                os.remove(dst)
    print(f"  downloaded: {ok}/{len(stickers)}")
