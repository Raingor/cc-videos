#!/usr/bin/env python3
"""Build contact sheets for downloaded sticker packs."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "line-stickers")
CELL = 200
COLS = 8
LABEL_H = 24

for pack in ["custom16024", "move1365252", "spring1394378"]:
    pack_dir = os.path.join(BASE, pack)
    files = sorted(f for f in os.listdir(pack_dir) if f.endswith(".png"))
    if not files:
        continue
    rows = (len(files) + COLS - 1) // COLS
    from PIL import ImageDraw, ImageFont
    sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + LABEL_H)), "#F0F0F0")
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        img = Image.open(os.path.join(pack_dir, f)).convert("RGBA")
        img.thumbnail((CELL - 10, CELL - 10), Image.LANCZOS)
        x = (i % COLS) * CELL
        y = (i // COLS) * (CELL + LABEL_H)
        sheet.paste(img, (x + (CELL - img.width) // 2, y + (CELL - img.height) // 2), img)
        draw.text((x + 5, y + CELL + 2), f.replace(".png", ""), fill="#333333")
    out = os.path.join(BASE, f"contact_{pack}.png")
    sheet.save(out)
    print(f"{pack}: {len(files)} stickers -> {out} ({sheet.size})")
