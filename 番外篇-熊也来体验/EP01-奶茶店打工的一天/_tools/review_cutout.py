#!/usr/bin/env python3
"""把4个抠图结果放在对比色底上，生成一张检查图。"""
import os
import numpy as np
from PIL import Image, ImageDraw

A = "/Users/mac-2312-r/workspace/wwwroot/CC/小红书/番外篇-熊也来体验/EP01-奶茶店打工的一天/_assets"
OUT = os.path.join(A, "_review_cutout.png")
NAMES = ["front", "left", "right", "back"]

CELL_W, CELL_H = 420, 560
sheet = Image.new("RGB", (CELL_W * len(NAMES), CELL_H), (60, 110, 150))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(NAMES):
    p = os.path.join(A, f"bear_{n}.png")
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGBA")
    sc = min((CELL_W - 30) / im.width, (CELL_H - 60) / im.height)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    x = i * CELL_W + (CELL_W - im.width) // 2
    y = CELL_H - im.height - 20
    sheet.paste(im, (x, y), im)
    d.text((i * CELL_W + 12, 12), f"{n} {Image.open(p).size}", fill=(255, 255, 255))
    d.rectangle([i * CELL_W, 0, (i + 1) * CELL_W - 1, CELL_H - 1], outline=(255, 255, 255))
sheet.save(OUT)
print(OUT, sheet.size)
