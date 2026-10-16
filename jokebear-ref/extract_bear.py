#!/usr/bin/env python3
"""
从官方贴图里抽出「纯熊本体」，去掉贴图自带的日文说明文字和箭头。

背景：自嘲熊贴图的原生格式就是「熊 + 箭头 + 日文吐槽文字」（这是该 IP 的设计），
240 张样本里只有 9 张是单连通域，其余都带日文字。直接拿来配中文文案会串味。

原理（实测有效）：熊本体是最大的连通域，占总 alpha 的 69%–84%；
日文字是一簇小连通域，聚在主体某一侧。保留主体（含贴近主体的零件），
其余全部丢弃 → 得到纯熊 PNG，熊本体仍是官方原图，还原度不受影响。

用法：
    python3 extract_bear.py                    # 处理默认 6 个包 → bears/
    python3 extract_bear.py 10033892-comic     # 只处理指定包
    python3 extract_bear.py --verify           # 处理完顺便量化验收
"""
import glob
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "bears")
PACKS_DEFAULT = [
    "10033892-comic", "10689991-somehow", "1007666-pack",
    "3542043-health", "6959173-honorifics-etc", "1310872-s-love",
]
KEEP_RATIO = 0.06      # 面积达到主体 6% 才有资格保留
NEAR_PAD = 0.10        # 主体包围盒膨胀 10%，落在其中的域视为熊的零件


def components(mask, min_area=60):
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for sy in range(0, h, 2):
        for sx in range(0, w, 2):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            stack = [(sy, sx)]
            seen[sy, sx] = True
            px = []
            while stack:
                y, x = stack.pop()
                px.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            if len(px) >= min_area:
                arr = np.array(px)
                out.append({
                    "px": arr, "area": len(px),
                    "y0": arr[:, 0].min(), "y1": arr[:, 0].max(),
                    "x0": arr[:, 1].min(), "x1": arr[:, 1].max(),
                })
    out.sort(key=lambda c: -c["area"])
    return out


def extract(path, out_path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)
    mask = a[..., 3] > 40
    if mask.sum() < 200:
        return None
    comps = components(mask)
    if not comps:
        return None
    main = comps[0]
    total = int(mask.sum())

    ph = (main["y1"] - main["y0"]) * NEAR_PAD
    pw = (main["x1"] - main["x0"]) * NEAR_PAD
    ry0, ry1 = main["y0"] - ph, main["y1"] + ph
    rx0, rx1 = main["x0"] - pw, main["x1"] + pw

    keep = [main]
    for c in comps[1:]:
        if c["area"] < main["area"] * KEEP_RATIO:
            continue
        cy = (c["y0"] + c["y1"]) / 2
        cx = (c["x0"] + c["x1"]) / 2
        if ry0 <= cy <= ry1 and rx0 <= cx <= rx1:
            keep.append(c)

    new = np.zeros_like(a)
    for c in keep:
        ys, xs = c["px"][:, 0], c["px"][:, 1]
        new[ys, xs] = a[ys, xs]

    kept_area = sum(c["area"] for c in keep)
    ys, xs = np.where(new[..., 3] > 40)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    Image.fromarray(new[y0:y1, x0:x1]).save(out_path)

    return {
        "comps_in": len(comps),
        "comps_kept": len(keep),
        "kept_ratio": round(kept_area / total, 3),
        "dropped": len(comps) - len(keep),
        "out_size": [int(x1 - x0), int(y1 - y0)],
    }


def text_band(path):
    """粗测残留文字条：黑像素行内转折次数集中程度。"""
    a = np.array(Image.open(path).convert("RGBA"))
    m = a[..., 3] > 40
    if m.sum() < 100:
        return 0.0
    dark = m & (a[..., :3].astype(np.int16).max(axis=2) < 110)
    tr = (np.abs(np.diff(dark.astype(np.int8), axis=1)) > 0).sum(axis=1)
    if tr.size == 0:
        return 0.0
    thr = max(8, int(np.percentile(tr, 90) * 0.55))
    it = tr >= thr
    best = cur = 0
    for v in it:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return round(best / len(it), 3)


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    packs = args or PACKS_DEFAULT
    report = {}
    for pack in packs:
        od = os.path.join(OUTDIR, pack)
        os.makedirs(od, exist_ok=True)
        n = 0
        for f in sorted(glob.glob(os.path.join(HERE, "line-stickers", pack, "*.png"))):
            if "_anim" in f:
                continue
            out = os.path.join(od, os.path.basename(f))
            r = extract(f, out)
            if r:
                report[f"{pack}/{os.path.basename(f)}"] = r
                n += 1
        print(f"{pack}: {n} 张 → bears/{pack}/")
    json.dump(report, open(os.path.join(HERE, "bears_report.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n共 {len(report)} 张 → {OUTDIR}")

    if "--verify" not in sys.argv:
        return
    kept = [v["kept_ratio"] for v in report.values()]
    drop = [v["dropped"] for v in report.values()]
    print("\n=== 量化验收 ===")
    print(f"保留面积占原图 alpha：中位 {np.median(kept):.1%}  最低 {min(kept):.1%}  最高 {max(kept):.1%}")
    print(f"平均丢弃连通域数：{np.mean(drop):.1f} 个/张（= 被去掉的日文字与箭头）")
    lo = sorted(report.items(), key=lambda kv: kv[1]["kept_ratio"])[:6]
    print("\n保留比例最低的 6 张（可能主体被切，需人工看一眼）：")
    for k, v in lo:
        print(f"  {k:44s} 保留 {v['kept_ratio']:.1%}  丢弃 {v['dropped']} 域")
    print("\n残留文字条抽查（原图 → 抽取后，越低越干净）：")
    for k in list(report)[:6]:
        src = os.path.join(HERE, "line-stickers", k)
        dst = os.path.join(OUTDIR, k)
        print(f"  {k:44s} {text_band(src):.3f} → {text_band(dst):.3f}")


if __name__ == "__main__":
    main()
