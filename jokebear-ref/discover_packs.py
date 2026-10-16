#!/usr/bin/env python3
"""
Discover all official Joke Bear (自分ツッコミくま / 對自己吐槽的白熊) LINE sticker packs.

Queries the LINE STORE search API, keeps packs whose title/author matches the
Joke Bear IP, and writes packs.json next to this script.

Usage:
    python3 discover_packs.py            # discover + write packs.json
    python3 discover_packs.py --show     # print the table only
"""
import json
import os
import re
import socket
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
PACKS_JSON = os.path.join(HERE, "packs.json")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/145.0 Safari/537.36")

# Search terms that surface the IP under its different names.
QUERIES = [
    "自分ツッコミくま",      # JP original name
    "joke bear",             # EN name used on LINE
    "對自己吐槽的白熊",       # zh-Hant name
    "自分ツッコミくま ナガノ",
]

# A pack is kept when its title or author matches one of these.
KEEP = re.compile(
    r"(自分ツッコミくま|對自己吐槽的白熊|对自己吐槽的白熊|joke\s*bear|jokebear)",
    re.I,
)

# Broad queries like "joke bear" claim totalCount=5000; paging everything is
# pointless (the IP's own packs all sit in the first pages) and hammers the
# API. Hard cap per query.
MAX_PAGES = 5

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

SEARCH_TPL = ("https://store.line.me/api/search/sticker"
              "?query={q}&offset={off}&limit={lim}&type=ALL")
META_TPL = ("https://stickershop.line-scdn.net/stickershop/v1/product/"
            "{pid}/iphone/productInfo.meta")


def get_json(url, timeout=20):
    """Fetch JSON via curl (avoids the LibreSSL/urllib3 warning noise)."""
    cmd = ["curl", "-sL", "--max-time", str(timeout), "-A", UA]
    if PROXY:
        cmd += ["--proxy", PROXY]
    cmd.append(url)
    out = subprocess.run(cmd, capture_output=True, check=False).stdout
    if not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def search_all():
    """Paginate every query, return {pack_id: search_item}."""
    found = {}
    for q in QUERIES:
        qq = urllib.parse.quote(q)
        offset, total, page = 0, None, 0
        while True:
            data = get_json(SEARCH_TPL.format(q=qq, off=offset, lim=40))
            if not data or "items" not in data:
                break
            if total is None:
                total = data.get("totalCount", 0)
                print(f"[search] {q!r} -> totalCount={total} (cap {MAX_PAGES} pages)",
                      flush=True)
            items = data["items"]
            if not items:
                break
            for it in items:
                found.setdefault(str(it["id"]), it)
            offset += len(items)
            page += 1
            if page >= MAX_PAGES or offset >= (total or 0):
                break
    return found


def enrich(pack_id):
    """Pull productInfo.meta for authoritative title/author/sticker list."""
    meta = get_json(META_TPL.format(pid=pack_id))
    if not meta:
        return None
    title = meta.get("title", {}) or {}
    author = meta.get("author", {}) or {}
    return {
        "id": str(meta.get("packageId", pack_id)),
        "title_en": title.get("en") or title.get("ja") or "",
        "title_zh": title.get("zh-Hant") or title.get("zh-Hans") or "",
        "title_ja": title.get("ja") or "",
        "author": author.get("en") or author.get("ja") or "",
        "count": len(meta.get("stickers", [])),
        "sticker_ids": [str(s["id"]) for s in meta.get("stickers", [])],
        "animated": bool(meta.get("hasAnimation")),
        "sound": bool(meta.get("hasSound")),
        "resource_type": meta.get("stickerResourceType", ""),
    }


def slug(pack):
    """Short filesystem-safe folder suffix."""
    base = pack["title_en"] or pack["title_ja"] or pack["id"]
    base = re.sub(r"joke\s*bear", "", base, flags=re.I)
    base = re.sub(r"[^0-9A-Za-z]+", "-", base).strip("-").lower()
    return base[:34] or "pack"


def main():
    if "--show" in sys.argv and os.path.exists(PACKS_JSON):
        packs = json.load(open(PACKS_JSON, encoding="utf-8"))
    else:
        hits = search_all()
        print(f"[search] {len(hits)} unique packs across {len(QUERIES)} queries")
        packs = []
        for pid, item in sorted(hits.items(), key=lambda kv: int(kv[0])):
            title = item.get("title") or ""
            if not KEEP.search(title):
                p = enrich(pid)
                blob = " ".join([title, (p or {}).get("title_ja", ""),
                                 (p or {}).get("title_zh", ""),
                                 (p or {}).get("author", "")])
                if not KEEP.search(blob):
                    continue
            else:
                p = enrich(pid)
            if not p or not p["count"]:
                print(f"  skip {pid}: no meta")
                continue
            p["slug"] = slug(p)
            p["dir"] = f"{p['id']}-{p['slug']}"
            packs.append(p)
            print(f"  + {p['id']:>8}  {p['count']:>3} 张  "
                  f"{'动画' if p['animated'] else '静态'}  {p['title_en'][:44]}")
        json.dump(packs, open(PACKS_JSON, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    total = sum(p["count"] for p in packs)
    anim = sum(p["count"] for p in packs if p["animated"])
    print(f"\n共 {len(packs)} 个官方贴图包 / {total} 张静态贴图"
          f"（其中 {anim} 张来自动画包，可再拆帧）")
    print(f"写入: {PACKS_JSON}")


if __name__ == "__main__":
    main()
