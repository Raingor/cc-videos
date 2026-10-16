#!/usr/bin/env python3
"""
Compose Xiaohongshu 9-grid Joke Bear posters using OFFICIAL LINE stickers.
100% original bear + custom background + custom text.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
STICKERS = os.path.join(HERE, "line-stickers")
OUT = os.path.normpath(os.path.join(HERE, "..", "2026-08-28-打工人周五", "v3"))
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1440
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_IDX = 2  # W6
INK = "#2B2B2B"

GRAY_BLUE = "#A8BCC4"
KRAFT = "#E8DCC4"
WARM_ORANGE = "#F5A85C"


def load_bear(rel_path):
    """Keep only the bear: largest connected component (body) plus nearby
    small decorations (blush/sweat/flowers). Remove right-side caption text
    and placeholder stars which are separate components far from the body."""
    img = Image.open(os.path.join(STICKERS, rel_path)).convert("RGBA")
    arr = np.array(img)
    mask = arr[..., 3] > 10
    lbl, n = ndimage.label(mask, structure=np.ones((3, 3)))
    if n <= 1:
        bbox = img.split()[-1].getbbox()
        return img.crop(bbox) if bbox else img
    sizes = ndimage.sum(mask, lbl, range(1, n + 1))
    main_id = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lbl == main_id)
    mx0, mx1, my0, my1 = xs.min(), xs.max(), ys.min(), ys.max()
    PAD = 6
    keep = np.zeros_like(mask)
    keep[lbl == main_id] = True
    for cid in range(1, n + 1):
        if cid == main_id:
            continue
        ys, xs = np.where(lbl == cid)
        cx0, cx1, cy0, cy1 = xs.min(), xs.max(), ys.min(), ys.max()
        area = sizes[cid - 1]
        intersects = not (cx0 > mx1 + PAD or cx1 < mx0 - PAD or
                          cy0 > my1 + PAD or cy1 < my0 - PAD)
        center_x = (cx0 + cx1) / 2
        on_right = center_x > mx1 + PAD
        # bbox overlap ratio with the body — real attachments (wings, blush)
        # overlap deeply; arrows/text barely touch (1-2px).
        ow = max(0, min(cx1, mx1) - max(cx0, mx0))
        oh = max(0, min(cy1, my1) - max(cy0, my0))
        comp_area = max(1, (cx1 - cx0) * (cy1 - cy0))
        overlap_ratio = (ow * oh) / comp_area
        if intersects and (overlap_ratio > 0.15 or area < 500):
            keep[lbl == cid] = True            # blush / wings / sweat hugging the body
        elif on_right and area >= 80:
            pass                                # caption text, arrows, placeholder stars
        else:
            keep[lbl == cid] = True            # sparkles, flowers, small decorations
    arr[..., 3] = np.where(keep, arr[..., 3], 0).astype(np.uint8)
    img = Image.fromarray(arr, "RGBA")
    bbox = img.split()[-1].getbbox()
    return img.crop(bbox) if bbox else img


def paste_bear(canvas, bear, target_w, cx, cy, flip=False):
    if flip:
        bear = bear.transpose(Image.FLIP_LEFT_RIGHT)
    ratio = target_w / bear.width
    bear = bear.resize((target_w, int(bear.height * ratio)), Image.LANCZOS)
    bear = bear.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    canvas.paste(bear, (int(cx - bear.width / 2), int(cy - bear.height / 2)), bear)


def draw_centered_text(draw, lines, y_start, font, fill, line_gap=1.45):
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), line, font=font, fill=fill)
        y += int(font.size * line_gap)
    return y


SCENES = [
    dict(file="01-封面-周五的熊和周一的熊是两种物种.png", type="split"),
    dict(file="02-周一的熊熊快撑不住了.png", bg=GRAY_BLUE,
         bear="move1365252/14406085.png",
         title=["周一的熊：", "熊快撑不住了"]),
    dict(file="03-周五的熊熊原谅全世界.png", bg=KRAFT,
         bear="custom16024/253818635.png",
         title=["周五的熊：", "熊原谅全世界"]),
    dict(file="04-今天也顺利地把自己骗到了工位.png", bg=GRAY_BLUE,
         bear="spring1394378/15325702.png",
         title=["今天也顺利地", "把自己骗到了工位"]),
    dict(file="05-摸鱼不是懒是给灵魂放个带薪假.png", bg=KRAFT,
         bear="spring1394378/15325687.png",
         title=["摸鱼不是懒，", "是给灵魂放个带薪假"]),
    dict(file="06-熊今天的目标活着下班.png", bg=GRAY_BLUE,
         bear="spring1394378/15325676.png",
         title=["熊今天的目标：", "活着下班"]),
    dict(file="07-熊很忙忙着假装很忙.png", bg=KRAFT,
         bear="move1365252/14406082.png",
         title=["熊很忙，", "忙着假装很忙"]),
    dict(file="08-打工不寒碜寒碜的是还没发工资.png", bg=GRAY_BLUE,
         bear="spring1394378/15325674.png",
         title=["打工不寒碜，", "寒碜的是还没发工资"]),
    dict(file="09-尾图-熊今天没崩溃给熊记一功.png", bg=WARM_ORANGE,
         bear="move1365252/14406096.png",
         title=["熊今天没崩溃", "给熊记一功"],
         subtitle="点赞收藏不迷路"),
]


def compose_normal(scene):
    canvas = Image.new("RGB", (W, H), scene["bg"])
    draw = ImageDraw.Draw(canvas)
    n = len(scene["title"])
    fsize = 100 if n <= 2 else 88
    font = ImageFont.truetype(FONT_PATH, fsize, index=FONT_IDX)
    y_start = 120 if n <= 2 else 100
    draw_centered_text(draw, scene["title"], y_start, font, INK)
    if scene.get("subtitle"):
        sub_font = ImageFont.truetype(FONT_PATH, 54, index=FONT_IDX)
        bbox = draw.textbbox((0, 0), scene["subtitle"], font=sub_font)
        draw.text(((W - (bbox[2] - bbox[0])) / 2, H - 190), scene["subtitle"], font=sub_font, fill=INK)
    bear = load_bear(scene["bear"])
    bear_w = 640 if n <= 2 else 580
    bear_cy = 880 if not scene.get("subtitle") else 830
    paste_bear(canvas, bear, bear_w, W / 2, bear_cy)
    return canvas


def compose_split():
    canvas = Image.new("RGB", (W, H))
    # left gray-blue, right warm orange
    canvas.paste(Image.new("RGB", (W // 2, H), GRAY_BLUE), (0, 0))
    canvas.paste(Image.new("RGB", (W // 2, H), WARM_ORANGE), (W // 2, 0))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_PATH, 92, index=FONT_IDX)
    y = 130
    for line in ["周五的熊", "和周一的熊", "是两种物种"]:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        # white pill behind text for readability across split
        pad_x, pad_y = 28, 14
        x0 = (W - tw) / 2 - pad_x
        draw.rounded_rectangle([x0, y - pad_y, x0 + tw + 2 * pad_x, y + font.size + pad_y + 10],
                               radius=36, fill="white")
        draw.text(((W - tw) / 2, y), line, font=font, fill=INK)
        y += int(font.size * 1.55)
    sub_font = ImageFont.truetype(FONT_PATH, 48, index=FONT_IDX)
    sub = "↓文案可自取"
    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, y + 6), sub, font=sub_font, fill=INK)
    # bears: left slumped (slightly darker side), right joy dance
    left_bear = load_bear("move1365252/14406087.png")
    right_bear = load_bear("move1365252/14406078.png")
    paste_bear(canvas, left_bear, 500, W * 0.25, 1090)
    paste_bear(canvas, right_bear, 500, W * 0.75, 1070)
    return canvas


for scene in SCENES:
    if scene.get("type") == "split":
        img = compose_split()
    else:
        img = compose_normal(scene)
    img.save(os.path.join(OUT, scene["file"]))
    print("OK", scene["file"])

print("done ->", OUT)
