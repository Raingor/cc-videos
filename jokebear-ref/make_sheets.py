#!/usr/bin/env python3
"""为 vision-agent 生成带 ID 标签的 contact sheet（每包一张，8 列）。"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

REF = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(REF, "sheets")
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
COLS, CELL, LAB = 8, 200, 30

PACKS = sys.argv[1:] or [
    "10033892-comic",
    "10689991-somehow",
    "1007666-pack",
    "3542043-health",
    "6959173-honorifics-etc",
    "1310872-s-love",
]

os.makedirs(OUT, exist_ok=True)
fnt = ImageFont.truetype(FONT, 18, index=1)
hdr = ImageFont.truetype(FONT, 26, index=2)

for pack in PACKS:
    files = sorted(f for f in glob.glob(os.path.join(REF, "line-stickers", pack, "*.png"))
                   if "_anim" not in f)
    if not files:
        print(f"skip {pack}: 无文件")
        continue
    rows = (len(files) + COLS - 1) // COLS
    sh = Image.new("RGB", (COLS * CELL, rows * (CELL + LAB) + 46), "#FFFFFF")
    d = ImageDraw.Draw(sh)
    d.text((12, 10), f"pack: {pack}   共 {len(files)} 张", fill="#111111", font=hdr)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGBA")
        im.thumbnail((CELL - 16, CELL - 16), Image.LANCZOS)
        x = (i % COLS) * CELL
        y = (i // COLS) * (CELL + LAB) + 46
        sh.paste(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2), im)
        d.rectangle([x, y, x + CELL - 1, y + CELL + LAB - 1], outline="#DDDDDD")
        d.text((x + 6, y + CELL + 5), os.path.basename(f)[:-4], fill="#222222", font=fnt)
    out = os.path.join(OUT, f"{pack}.png")
    sh.save(out)
    print(f"{out}  {sh.size}  {len(files)} 张")
