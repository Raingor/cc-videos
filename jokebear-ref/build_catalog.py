#!/usr/bin/env python3
"""
Build stickers.json — a machine-searchable index of every bear asset.

Scans line-stickers/*/*.png (static) and frames/**/*.png (animation frames),
records path / size / pack / origin, and writes stickers.json next to this
script. Also renders one master contact sheet (contact_all.png) so a human
can eyeball poses.

The generated stickers.json is meant to be fed to whoever composes the
videos/grids (an agent picks a sticker id by looking at the sheet or the
index), e.g.:

    bear="line-stickers/1394378-.../15325676.png"

Usage:
    python3 build_catalog.py
"""
import glob
import json
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "line-stickers")
FRAMES = os.path.join(HERE, "frames")
PACKS_JSON = os.path.join(HERE, "packs.json")
OUT_JSON = os.path.join(HERE, "stickers.json")
SHEET = os.path.join(HERE, "contact_all.png")

PACK_TITLES = {}
if os.path.exists(PACKS_JSON):
    for p in json.load(open(PACKS_JSON, encoding="utf-8")):
        PACK_TITLES[p["dir"]] = {
            "title": p.get("title_en", ""),
            "title_zh": p.get("title_zh", ""),
            "author": p.get("author", ""),
            "animated": p.get("animated", False),
        }


def build_index():
    items = []
    for path in sorted(glob.glob(os.path.join(BASE, "*", "*.png"))):
        name = os.path.basename(path)
        if name.startswith("contact_"):
            continue
        pack = os.path.basename(os.path.dirname(path))
        animated = name.endswith("_anim.png")
        sid = name.replace("_anim.png", "").replace(".png", "")
        try:
            w, h = Image.open(path).size
        except Exception:  # noqa: BLE001
            w = h = 0
        items.append({
            "id": f"{pack}/{sid}" + ("_anim" if animated else ""),
            "file": os.path.relpath(path, HERE),
            "pack": pack,
            "sticker_id": sid,
            "kind": "animated" if animated else "static",
            "w": w, "h": h,
        })
    for path in sorted(glob.glob(os.path.join(FRAMES, "*", "*.png"))):
        pack = os.path.basename(os.path.dirname(path))
        name = os.path.basename(path)
        try:
            w, h = Image.open(path).size
        except Exception:  # noqa: BLE001
            w = h = 0
        items.append({
            "id": f"frames/{pack}/{name[:-4]}",
            "file": os.path.relpath(path, HERE),
            "pack": pack,
            "sticker_id": name.split("_f")[0],
            "kind": "frame",
            "w": w, "h": h,
        })
    return items


def build_sheet(items):
    """Contact sheet of every static sticker (frames excluded, too many)."""
    static = [it for it in items if it["kind"] == "static"]
    if not static:
        return
    COLS, CELL, PAD = 10, 160, 4
    rows = (len(static) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + 18)), "#EEEEEE")
    draw = ImageDraw.Draw(sheet)
    for i, it in enumerate(static):
        try:
            img = Image.open(os.path.join(HERE, it["file"])).convert("RGBA")
            img.thumbnail((CELL - 8, CELL - 8), Image.LANCZOS)
            x = (i % COLS) * CELL
            y = (i // COLS) * (CELL + 18)
            sheet.paste(img, (x + (CELL - img.width) // 2,
                              y + (CELL - img.height) // 2), img)
            draw.text((x + 2, y + CELL + 1),
                      it["sticker_id"], fill="#444444")
        except Exception:  # noqa: BLE001
            continue
    sheet.save(SHEET)
    print(f"contact sheet: {SHEET} ({len(static)} 张静态贴图)")


def main():
    items = build_index()
    packs = sorted({it["pack"] for it in items})
    json.dump({
        "packs": {p: PACK_TITLES.get(p, {}) for p in packs},
        "items": items,
    }, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    build_sheet(items)
    kinds = {}
    for it in items:
        kinds[it["kind"]] = kinds.get(it["kind"], 0) + 1
    print(f"索引: {OUT_JSON}")
    print(f"共 {len(items)} 条（{kinds}），{len(packs)} 个包")


if __name__ == "__main__":
    main()
