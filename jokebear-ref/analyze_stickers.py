#!/usr/bin/env python3
"""
贴图几何分析器 —— 在没有视觉能力的情况下，用像素统计筛出「可用」的贴图。

能测出来的（可靠）：
  - single      : 连通域个数，1 = 只有一只熊，>1 = 带道具/气泡/第二只熊
  - text_band   : 是否有日文文字条（文字 = 窄横带内大量短黑笔画，转折次数远高于熊的轮廓）
  - posture     : upright / wide / lying（由 alpha 包围盒宽高比推出）
  - head_low    : 墨迹重心是否偏下（趴着 / 低头）
  - centered    : 包围盒中心相对画布中心的偏移
  - coverage    : 主体占包围盒的比例（越低越松散/摊开）
  - accent      : 饱和色像素比例（官方熊是白+黑+极少点缀，比例高说明有道具或装饰）

测不出来的：表情语义（困 / 呆 / 开心 / 无奈）。这部分必须人眼确认。

用法：
    python3 analyze_stickers.py                 # 分析默认 6 个包，输出 sticker_geom.json
    python3 analyze_stickers.py --pick          # 额外打印各姿态类的推荐短名单
"""
import glob
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sticker_geom.json")
PACKS = [
    "10033892-comic", "10689991-somehow", "1007666-pack",
    "3542043-health", "6959173-honorifics-etc", "1310872-s-love",
]


def cc_count(mask, min_area=120):
    """连通域计数（4 邻域，迭代 flood fill，避免依赖 scipy）。"""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    n = 0
    for sy in range(0, h, 2):
        for sx in range(0, w, 2):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            stack = [(sy, sx)]
            seen[sy, sx] = True
            area = 0
            while stack:
                y, x = stack.pop()
                area += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            if area >= min_area:
                n += 1
    return n


def text_band_score(dark, bbox):
    """
    文字条检测：日文说明字 = 窄横带内很多短黑笔画。
    对每一行统计「黑白转折次数」，转折多且分布集中的行 = 文字行。
    返回 (文字行占比, 最大连续文字带高度/主体高度)
    """
    y0, y1, x0, x1 = bbox
    sub = dark[y0:y1, x0:x1]
    if sub.size == 0:
        return 0.0, 0.0
    trans = (np.abs(np.diff(sub.astype(np.int8), axis=1)) > 0).sum(axis=1)
    thr = max(8, int(np.percentile(trans, 90) * 0.55))
    is_text = trans >= thr
    if is_text.sum() == 0:
        return 0.0, 0.0
    best = cur = 0
    for v in is_text:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return float(is_text.mean()), float(best / max(1, sub.shape[0]))


def analyze(path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)
    alpha = a[..., 3]
    mask = alpha > 40
    if mask.sum() < 200:
        return None
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    bw, bh = x1 - x0, y1 - y0
    ratio = bw / bh

    rgb = a[..., :3].astype(np.int16)
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    dark = mask & (mx < 110)                       # 黑线（轮廓/五官/文字）
    sat = mask & ((mx - mn) > 55) & (mx > 110)     # 饱和色（道具/装饰/腮红）

    # 墨迹重心（相对包围盒的纵向位置，0=顶 1=底）
    dys, _ = np.where(dark)
    head_low = float(((dys.mean() - y0) / bh)) if dys.size else 0.5

    txt_rows, txt_band = text_band_score(dark, (y0, y1, x0, x1))

    cy_off = abs(((y0 + y1) / 2) - im.height / 2) / im.height
    cx_off = abs(((x0 + x1) / 2) - im.width / 2) / im.width

    posture = "upright" if ratio < 0.95 else ("wide" if ratio <= 1.3 else "lying")

    return {
        "posture": posture,
        "ratio": round(float(ratio), 3),
        "coverage": round(float(mask[y0:y1, x0:x1].mean()), 3),
        "cc": cc_count(mask),
        "text_rows": round(txt_rows, 3),
        "text_band": round(txt_band, 3),
        "ink_centroid": round(head_low, 3),
        "accent": round(float(sat.sum() / max(1, mask.sum())), 4),
        "off_center": round(float(max(cx_off, cy_off)), 3),
        "size": [int(bw), int(bh)],
    }


def main():
    res = {}
    for pack in PACKS:
        for f in sorted(glob.glob(os.path.join(HERE, "line-stickers", pack, "*.png"))):
            if "_anim" in f:
                continue
            r = analyze(f)
            if r:
                res[f"{pack}/{os.path.basename(f)}"] = r
        print(f"{pack}: 累计 {len(res)}")
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"→ {OUT}  共 {len(res)} 张")

    if "--pick" not in sys.argv:
        return

    def clean(v):
        return v["cc"] == 1 and v["text_band"] < 0.22 and v["off_center"] < 0.18 and v["accent"] < 0.12

    print("\n=== 干净单只熊（cc=1 / 无文字带 / 居中 / 少饱和色）按姿态分组 ===")
    for post in ("upright", "wide", "lying"):
        pool = [(k, v) for k, v in res.items() if v["posture"] == post and clean(v)]
        pool.sort(key=lambda kv: (kv[1]["text_band"], kv[1]["off_center"]))
        print(f"\n[{post}] {len(pool)} 张可用")
        for k, v in pool[:12]:
            print(f"  {k:44s} ratio={v['ratio']:<6} ink={v['ink_centroid']:<6} "
                  f"cov={v['coverage']:<6} accent={v['accent']}")


if __name__ == "__main__":
    main()
