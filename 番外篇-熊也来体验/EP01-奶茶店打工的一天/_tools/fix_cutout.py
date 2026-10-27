#!/usr/bin/env python3
"""
抠图后处理（最终版）

要解决的问题：实拍背景（灰玻璃 / 石台）在熊身内部有少量「渗色」，表现为偏蓝的灰斑。
处理策略分两类，避免把熊身挖出洞：
  1) 贴着轮廓边的偏蓝区域  -> 是背景翻边，按透明度打掉
  2) 熊身内部的偏蓝灰斑    -> 只做「去蓝 + 提亮」中和，不动 alpha，
                             这样它会自然融进熊自身的浅灰明暗里
注意：不做任何「按暗色块擦除」——熊的眼睛/嘴也是暗的，之前那样会把脸弄没。
"""
import os
import cv2
import numpy as np

A = "/Users/mac-2312-r/workspace/wwwroot/CC/小红书/番外篇-熊也来体验/EP01-奶茶店打工的一天/_assets"

for n in ["front", "left", "right", "back"]:
    p = f"{A}/bear_{n}.png"
    rgba = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    h, w = rgba.shape[:2]
    b = rgba[..., 0].astype(np.float32)
    g = rgba[..., 1].astype(np.float32)
    r = rgba[..., 2].astype(np.float32)
    alpha = rgba[..., 3].astype(np.float32)

    bluish = ((b - r) > 9) & (alpha > 60)
    dist = cv2.distanceTransform(((alpha > 128).astype(np.uint8) * 255), cv2.DIST_L2, 5)

    # --- 1) 内部偏蓝斑：去蓝中和（b 拉回 r 的水平），并轻微提亮 ---
    inner = bluish & (dist > 30)
    inner = cv2.morphologyEx(inner.astype(np.uint8), cv2.MORPH_CLOSE,
                             np.ones((31, 31), np.uint8)).astype(bool)
    nfix = int(inner.sum())
    if nfix:
        nb = b.copy()
        nb[inner] = r[inner]                       # 去掉蓝色偏色
        lift = np.clip((nb - 18.0) * 1.10, 0, 255)
        b = np.where(inner, lift, b)
        g = np.where(inner, lift, g)
        r = np.where(inner, lift, r)

    # --- 2) 贴边的偏蓝翻边：打掉 ---
    edge_blue = (bluish & (dist <= 30)).astype(np.uint8) * 255
    edge_blue = cv2.morphologyEx(edge_blue, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    edge_blue = cv2.morphologyEx(edge_blue, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    kill = np.zeros((h, w), np.uint8)
    ncc, lab, st, _ = cv2.connectedComponentsWithStats(edge_blue, 8)
    removed = 0
    for i in range(1, ncc):
        if st[i, 4] < 1200:
            continue
        kill[lab == i] = 255
        removed += st[i, 4]
    if removed:
        kill = cv2.dilate(kill, np.ones((13, 13), np.uint8))
        soft = cv2.GaussianBlur(kill.astype(np.float32), (0, 0), 8.0) / 255.0
        alpha = alpha * (1.0 - soft)

    # --- 3) 削掉擦除残留的细边框条 ---
    am = cv2.morphologyEx((alpha > 128).astype(np.uint8) * 255,
                          cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    opened = cv2.morphologyEx(am, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))
    alpha = alpha * (cv2.GaussianBlur(opened.astype(np.float32), (0, 0), 3.0) / 255.0)

    # --- 3.5) 定向清吊牌（韩文吊牌上的字是品牌信息，不宜出现在成片里）。
    # 关键：只重绘 RGB，绝不改 alpha。
    # 一旦把这块按透明打掉，熊的下半身会被啃出一个方块缺口，比吊牌还难看。
    # 位置由「暗字连通域质心」实测得到。
    TAG_BOX = {
        "front": [(0.42, 0.83, 0.62, 1.00)],
        "left":  [(0.50, 0.76, 0.82, 0.98)],
        "right": [(0.16, 0.80, 0.33, 0.90)],
        "back":  [(0.02, 0.70, 0.28, 1.00)],
    }
    if n in TAG_BOX:
        bgr8 = np.dstack([b, g, r]).astype(np.uint8)
        mk = np.zeros((h, w), np.uint8)
        for (x0f, y0f, x1f, y1f) in TAG_BOX[n]:
            mk[int(y0f * h):int(y1f * h), int(x0f * w):int(x1f * w)] = 255
        bgr8 = cv2.inpaint(bgr8, mk, 7, cv2.INPAINT_TELEA)
        b, g, r = (bgr8[..., 0].astype(np.float32), bgr8[..., 1].astype(np.float32),
                   bgr8[..., 2].astype(np.float32))

    # --- 4) 去掉孤立小碎块 ---
    am = (alpha > 128).astype(np.uint8)
    ncc, lab, st, _ = cv2.connectedComponentsWithStats(am, 8)
    if ncc > 2:
        keep = 1 + int(np.argmax(st[1:, 4]))
        big = st[keep, 4]
        for i in range(1, ncc):
            if i != keep and st[i, 4] < 0.02 * big:
                alpha[lab == i] = 0

    out = np.dstack([np.clip(b, 0, 255), np.clip(g, 0, 255), np.clip(r, 0, 255),
                     np.clip(alpha, 0, 255)]).astype(np.uint8)
    ys, xs = np.where(out[..., 3] > 12)
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(p, out)
    print(f"[{n}] 中和内部灰斑 {nfix}px  打掉边缘翻边 {removed}px -> {out.shape[1]}x{out.shape[0]}")
print("done")
