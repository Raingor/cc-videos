#!/usr/bin/env python3
"""
EP01 奶茶店打工的一天 —— 6 帧场景图合成（1080x1440）
一帧 = 程序绘制背景 + 程序绘制道具 + 程序绘制文字 + 实拍全照抠出的熊
（熊本体 100% 来自 user 提供的实拍全照，不做 AI 生成）
"""
import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/Users/mac-2312-r/workspace/wwwroot/CC/小红书/番外篇-熊也来体验/EP01-奶茶店打工的一天"
ASSETS = os.path.join(BASE, "_assets")
OUT = BASE
W, H = 1080, 1440

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
F_IDX_LIGHT = 0   # W3 细软
F_IDX_BOLD = 2    # W6

INK = (62, 52, 42)
INK_SOFT = (138, 106, 69)
WHITE = (255, 255, 255)


# ---------------------------------------------------------------- 熊处理
_bear_cache = {}


def load_bear(name):
    if name in _bear_cache:
        return _bear_cache[name]
    im = Image.open(os.path.join(ASSETS, f"bear_{name}.png")).convert("RGBA")
    a = np.array(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    # 高调提亮：实拍白熊偏灰，抬黑位 + 提增益，让熊身接近纯白而五官仍深
    rgb = np.clip((rgb - 35.0) * 1.40, 0, 255)
    rgb[..., 0] *= 1.025          # 轻微偏暖
    rgb[..., 2] *= 0.972
    rgb = np.clip(rgb, 0, 255)
    # 边缘去灰：alpha 越低越往白里收，消掉实拍背景的灰边
    t = np.clip((al - 40) / 150.0, 0, 1)[..., None]
    rgb = rgb * (0.50 + 0.50 * t) + 255.0 * (1 - (0.50 + 0.50 * t))
    out = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), al]).astype(np.uint8), "RGBA")
    _bear_cache[name] = out
    return out


def paste_bear(canvas, bear_name, target_w, cx, bottom_y, tilt=0.0, flip=False,
               shadow=True, glow_rgb=None):
    bear = load_bear(bear_name)
    if flip:
        bear = bear.transpose(Image.FLIP_LEFT_RIGHT)
    sc = target_w / bear.width
    bear = bear.resize((target_w, max(1, int(bear.height * sc))), Image.LANCZOS)
    if tilt:
        bear = bear.rotate(tilt, resample=Image.BICUBIC, expand=True)

    x = int(cx - bear.width / 2)
    y = int(bottom_y - bear.height)

    if shadow:
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse(
            [x + bear.width * 0.10, bottom_y - 40, x + bear.width * 0.90, bottom_y + 26],
            fill=(58, 44, 30, 78))
        canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))

    # 环境遮蔽式柔光：沿熊的轮廓外一圈画「比背景略深」的软边，
    # 否则白熊贴在奶油底上会糊成一片看不出轮廓
    if glow_rgb:
        m = np.array(bear.split()[-1]).astype(np.float32) / 255.0
        grown = cv2.dilate(m, np.ones((25, 25), np.uint8))
        ring = np.clip(cv2.GaussianBlur(grown, (0, 0), 13) - m, 0, 1)
        gl = Image.new("RGBA", canvas.size, glow_rgb + (0,))
        ga = np.zeros((canvas.height, canvas.width), np.uint8)
        ga[y:y + bear.height, x:x + bear.width] = (ring * 150).astype(np.uint8)
        gl.putalpha(Image.fromarray(ga))
        canvas.alpha_composite(gl)

    canvas.alpha_composite(bear, (x, y))
    return x, y, bear.width, bear.height


# ---------------------------------------------------------------- 文字
def text_lines(draw, lines, y, fill, size, gap=1.34, idx=F_IDX_LIGHT, shadow=False):
    font = ImageFont.truetype(FONT, size, index=idx)
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=font)
        tw = bb[2] - bb[0]
        x = (W - tw) / 2 - bb[0]
        if shadow:
            draw.text((x + 3, y + 3), ln, font=font, fill=(255, 255, 255, 200))
        draw.text((x, y), ln, font=font, fill=fill)
        y += int(size * gap)
    return y


# ---------------------------------------------------------------- 道具
def prop_sealer(d, box, ink=(120, 112, 100), body=(240, 236, 228), light=(214, 76, 60)):
    """封口机：圆角方块 + 小红点"""
    x0, y0, x1, y1 = box
    r = int(min(x1 - x0, y1 - y0) * 0.22)
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=body, outline=ink, width=6)
    d.line([x0 + 14, y0 + int((y1 - y0) * 0.42), x1 - 14, y0 + int((y1 - y0) * 0.42)],
           fill=ink, width=5)
    dr = int(min(x1 - x0, y1 - y0) * 0.11)
    cx, cy = x0 + int((x1 - x0) * 0.30), y0 + int((y1 - y0) * 0.72)
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=light)


def prop_receipt(d, box, ink=(150, 145, 136), paper=(255, 253, 248)):
    """小票：细长白条 + 锯齿边"""
    x0, y0, x1, y1 = box
    n = 14
    step = (x1 - x0) / n
    pts = [(x0, y0)]
    for i in range(n):
        pts.append((x0 + step * (i + 0.5), y0 + 18))
        pts.append((x0 + step * (i + 1), y0))
    pts += [(x1, y1), (x0, y1)]
    d.polygon(pts, fill=paper, outline=ink)
    yy = y0 + 60
    ww = [0.62, 0.44, 0.70, 0.36, 0.58, 0.48, 0.66, 0.40, 0.55, 0.30]
    i = 0
    while yy < y1 - 40:
        wl = (x1 - x0 - 44) * ww[i % len(ww)]
        d.rounded_rectangle([x0 + 22, yy, x0 + 22 + wl, yy + 16], radius=8, fill=ink)
        yy += 44
        i += 1


def prop_cup(d, box, ink=(176, 166, 152), body=(255, 253, 249), seal=(226, 218, 205)):
    """杯子：上宽下窄梯形 + 一条封口线 + 吸管（不画品牌、不出现 logo）"""
    x0, y0, x1, y1 = box
    tw = x1 - x0
    bw = tw * 0.72
    bl = x0 + (tw - bw) / 2
    br = bl + bw
    lip = y0 + (y1 - y0) * 0.10
    d.polygon([(x0, lip), (x1, lip), (br, y1), (bl, y1)], fill=body, outline=ink)
    d.polygon([(x0, y0), (x1, y0), (x1, lip), (x0, lip)], fill=seal, outline=ink)
    d.line([(x0, lip), (x1, lip)], fill=ink, width=5)
    sw = max(3, int(tw * 0.065))
    sx = x0 + tw * 0.60
    d.line([(sx, y0 - tw * 0.42), (sx + tw * 0.05, lip + 2)], fill=ink, width=sw)


def prop_heart(d, cx, cy, r, fill=(232, 92, 74)):
    t = np.linspace(0, 2 * np.pi, 240)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    s = r / 16.0
    pts = [(cx + xi * s, cy + yi * s) for xi, yi in zip(x, y)]
    d.polygon(pts, fill=fill)


def prop_counter(d, y, color):
    d.rounded_rectangle([0, y, W, y + 16], radius=8, fill=color)


# ---------------------------------------------------------------- 背景
def grad_bg(top, bottom):
    g = np.linspace(0, 1, H)[:, None, None]
    a = np.array(top, np.float32)[None, None, :]
    b = np.array(bottom, np.float32)[None, None, :]
    arr = (a * (1 - g) + b * g).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, W, axis=1), "RGB")


# ---------------------------------------------------------------- 分镜
SCENES = [
    dict(file="01.png", bg="#F7F1E6", counter="#E7DBC7",
         kicker=["熊也来体验"],
         title=["奶茶店打工的一天"], size_kick=72, size_title=104,
         bear="front", bear_w=660, bottom=1360, tilt=-2,
         props=[("cup", (0.09, 0.585, 0.215, 0.655)), ("sealer", (0.80, 0.565, 0.97, 0.645))],
         prop_on_counter=True, counter_y=0.655),

    dict(file="02.png", bg="#F2EDE2", counter="#E3DACB",
         title=["09:50 开店", "熊先把封口机预热了"],
         sub=["（自己还没热）"], size_title=78, size_sub=54,
         bear="left", bear_w=545, bottom=1352, tilt=5,
         props=[("sealer", (0.06, 0.565, 0.26, 0.65))],
         prop_on_counter=True, counter_y=0.655),

    dict(file="03.png", bg="#F4D68F", counter=None,
         title=["13:00 高峰", "单子比熊高"], size_title=92,
         bear="right", bear_w=545, bottom=1372, tilt=-2,
         props=[("receipt", (0.72, 0.235, 0.875, 0.955))]),

    dict(file="04.png", bg="#DCE1E5", counter="#CDD5DA",
         title=["14:30 有人说少冰", "熊已经封好口了"], size_title=84,
         bear="front", bear_w=590, bottom=1338, tilt=0,
         props=[("cup", (0.045, 0.560, 0.205, 0.655))],
         prop_on_counter=True, counter_y=0.655),

    dict(file="05.png", bg="#F5A85C", counter=None,
         title=["16:00 有人说了谢谢", "熊今天回血了"], size_title=86,
         bear="front", bear_w=620, bottom=1352, tilt=0,
         props=[("heart", (0.815, 0.40, 52))]),

    dict(file="06.png", bg_top="#F8C383", bg="#F2A055", counter=None,
         title=["熊今天卖了三百杯", "自己一口没喝", "给熊记一功"], size_title=84,
         bear="front", bear_w=600, bottom=1290, tilt=2,
         props=[("cup_held", (0.385, 0.505, 0.575, 0.635))],
         sub=["点赞收藏｜熊也来体验 EP.01"], size_sub=50, sub_y=0.952),
]


def draw_props(canvas, d, props, counter_y):
    for kind, arg in props:
        if kind == "sealer" and arg:
            x0, y0, x1, y1 = arg
            prop_sealer(d, [int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)])
        elif kind == "cup" and arg:
            x0, y0, x1, y1 = arg
            prop_cup(d, [int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)])
        elif kind == "receipt" and arg:
            x0, y0, x1, y1 = arg
            prop_receipt(d, [int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)])
        elif kind == "heart" and arg:
            prop_heart(d, int(arg[0] * W), int(arg[1] * H), arg[2])


def build(scene):
    if scene.get("bg_top"):
        canvas = grad_bg(hex2rgb(scene["bg_top"]), hex2rgb(scene["bg"])).convert("RGBA")
    else:
        canvas = Image.new("RGBA", (W, H), hex2rgb(scene["bg"]) + (255,))
    d = ImageDraw.Draw(canvas)

    # 台面线
    if scene.get("counter"):
        prop_counter(d, int(H * scene.get("counter_y", 0.655)), hex2rgb(scene["counter"]))

    # 1) 背景层道具 -> 2) 熊 -> 3) 手持道具 -> 4) 文字（永远压在最上层）
    held = [p for p in scene["props"] if p[0] == "cup_held"]
    draw_props(canvas, d, [p for p in scene["props"] if p[0] != "cup_held"], None)

    gb = hex2rgb(scene.get("bg_top") or scene["bg"])
    gcol = tuple(max(0, int(c * 0.80)) for c in gb)
    paste_bear(canvas, scene["bear"], scene["bear_w"], W / 2, scene["bottom"],
               tilt=scene.get("tilt", 0), flip=scene.get("flip", False), glow_rgb=gcol)

    for kind, arg in held:
        x0, y0, x1, y1 = arg
        prop_cup(ImageDraw.Draw(canvas), [int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)])

    d = ImageDraw.Draw(canvas)
    y = int(H * 0.082)
    if scene.get("kicker"):
        y = text_lines(d, scene["kicker"], y, INK_SOFT, scene["size_kick"], idx=F_IDX_BOLD) + 16
    if scene.get("title"):
        y = text_lines(d, scene["title"], y, INK, scene.get("size_title", 90))
    if scene.get("sub") and not scene.get("sub_y"):
        text_lines(d, scene["sub"], y + 8, INK_SOFT, scene.get("size_sub", 60))
    if scene.get("sub_y"):
        f = ImageFont.truetype(FONT, scene["size_sub"], index=F_IDX_BOLD)
        bb = d.textbbox((0, 0), scene["sub"][0], font=f)
        d.text(((W - (bb[2] - bb[0])) / 2, int(H * scene["sub_y"])), scene["sub"][0],
               font=f, fill=INK)
    return canvas.convert("RGB")


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


for sc in SCENES:
    img = build(sc)
    img.save(os.path.join(OUT, sc["file"]))
    print("OK", sc["file"], img.size)

meta = []
for sc in SCENES:
    meta.append({k: v for k, v in sc.items() if k != "props"} |
                {"props": [p[0] for p in sc["props"]]})
with open(os.path.join(OUT, "scenes.json"), "w", encoding="utf-8") as f:
    json.dump({"_规范": "1080x1440 · 6帧 · 实拍全照抠图熊 · 程序绘制背景/道具/文字",
               "scenes": meta}, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
