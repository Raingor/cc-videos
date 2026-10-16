#!/usr/bin/env python3
"""
Extract every frame from animated stickers (_anim.png, APNG) into
frames/<pack>/<sticker_id>_fNN.png.

PIL 11 can open APNG natively (Pillow >= 8). This multiplies the usable
reference poses: a 24-sticker animated pack often yields 200+ distinct frames.

Usage:
    python3 extract_frames.py           # extract all animated packs
"""
import glob
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "line-stickers")
FRAMES = os.path.join(HERE, "frames")


def extract(path, out_dir):
    """Save every frame of an APNG. Returns number of frames written."""
    os.makedirs(out_dir, exist_ok=True)
    sid = os.path.basename(path).replace("_anim.png", "")
    n = 0
    try:
        im = Image.open(path)
        while True:
            frame = im.convert("RGBA")
            dst = os.path.join(out_dir, f"{sid}_f{n:02d}.png")
            frame.save(dst)
            n += 1
            try:
                im.seek(im.tell() + 1)
            except EOFError:
                break
    except Exception as e:  # noqa: BLE001 - keep going on corrupt files
        print(f"  ! {path}: {e}")
    return n


def main():
    total = 0
    for anim in sorted(glob.glob(os.path.join(BASE, "*", "*_anim.png"))):
        pack = os.path.basename(os.path.dirname(anim))
        out_dir = os.path.join(FRAMES, pack)
        n = extract(anim, out_dir)
        total += n
    files = sum(len(files) for _, _, files in os.walk(FRAMES))
    print(f"拆帧完成: {total} 个动画文件 -> {FRAMES}（共 {files} 帧）")


if __name__ == "__main__":
    main()
