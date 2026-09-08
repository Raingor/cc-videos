#!/usr/bin/env python3
"""Kling video generator for the jokebear "last coffee delivery" story.

Strategy:
  The source script (jokebear-videos-log.md) packs a lot of action into 30s.
  Kling ignores most of it when given 10s of dense action, so the story is
  split into 6 x 5s beats with ONE clear action each. Each beat after the
  first is seeded with the previous beat's last frame via image2video, so
  character / clothing / lighting stay continuous. ffmpeg concatenates.

Usage:
  python3 kling_gen.py                    # full run (resumes, skips existing)
  python3 kling_gen.py --concat           # only re-concat existing clips
  python3 kling_gen.py --redo 3 5         # delete + regenerate beats 3 and 5
  python3 kling_gen.py --model kling-v1-6 # override model
  python3 kling_gen.py --out DIR          # override output dir
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

API = "https://agentrs.jd.com/api/saas/plugin-u/v1/exec"
TOKEN = os.environ.get(
    "KLING_API_KEY", "RsCenterCH-wos2rpj/Z+OaspXkNL8fqwUG3AxCIhdZ7gRUYOE67ss="
)
ROOT = os.path.dirname(os.path.abspath(__file__))

# --- shared prompt fragments -------------------------------------------------

BEAR = (
    "a cute minimalist cartoon polar bear: big round white head, small round ears, "
    "two tiny black bean dot eyes, a completely flat black nose and flat simple "
    "smile printed on the face surface with no protruding muzzle or snout even in "
    "side view, short chubby white body, tiny stubby arms and legs, flat matte white "
    "shading, clean minimalist flat cartoon illustration, "
    "wearing a bright yellow delivery vest with a tiny white bear-head logo and a "
    "bright yellow delivery helmet with the same tiny bear-head logo"
)
BAG = (
    "a tall blue paper delivery bag with white twisted handles, printed with white "
    "clouds, a green grass strip, small orange and yellow flowers and a white "
    "cartoon bear head"
)
CUP = (
    "a tall dark blue paper coffee cup with a white plastic lid and a blue diamond "
    "lattice pattern"
)
SCOOTER = (
    "a small yellow and white electric delivery scooter with a tiny bear-head sticker"
)
STYLE = (
    "warm late afternoon golden hour sunlight, cozy quiet urban residential street, "
    "soft warm cinematic light, slow smooth cinematic camera, relaxed pacing, "
    "flat cartoon animation"
)
CONT = "Exact same bear, same yellow vest and helmet, same street, same golden light."
NEGATIVE = (
    "protruding muzzle, snout, realistic bear face, photorealistic, live action, "
    "plush toy photograph, glossy 3D render, changing character design, changing "
    "clothing color, changing helmet design, changing scooter design, different "
    "coffee bag, different coffee cup, giant oversized props, distorted logo, "
    "extra limbs, malformed hands, text overlay, subtitles, watermark, scene cut, "
    "camera shake, abrupt movement, chaotic motion, duplicated character"
)

# --- 6 beats x 5s = 30s ------------------------------------------------------

BEATS = [
    (
        "beat1",
        f"{BEAR} sits slumped and tired on the stone step at the entrance of a "
        "residential building. An empty fried chicken box and an empty instant "
        "noodle cup lie beside it. The bear slowly pats its full round belly once "
        f"and lets out a relaxed breath. {STYLE}. Slow gentle push-in.",
    ),
    (
        "beat2",
        f"{CONT} The delivery phone lying next to the bear suddenly lights up and "
        "buzzes with a new order notification. The bear slowly opens its eyes, "
        "reaches out with one stubby arm, picks up the small phone and looks at the "
        f"screen. {STYLE}.",
    ),
    (
        "beat3",
        f"{CONT} Holding the phone, the bear realizes there is one last coffee order. "
        "It droops its head in reluctance, sighs deeply, then slowly pushes itself up "
        f"and stands on its short legs. {STYLE}.",
    ),
    (
        "beat4",
        f"{CONT} The standing bear carefully lowers {CUP} into {BAG} placed on the "
        "step, then lifts the bag by its handles with both arms and turns toward "
        f"{SCOOTER} parked at the curb. {STYLE}.",
    ),
    (
        "beat5",
        f"{CONT} The bear hangs the blue printed coffee delivery bag securely on the "
        "front of the electric scooter, sits on the saddle and rides slowly down the "
        "quiet golden-hour street. It looks exhausted but determined. Side tracking "
        f"camera follows the scooter. {STYLE}.",
    ),
    (
        "beat6",
        f"{CONT} The bear stands at the doorway of another residential building and "
        "gently hands the blue printed coffee delivery bag to a happy waiting "
        "customer. The bear gives one small satisfied nod, then turns and walks slowly "
        f"back toward its parked electric scooter, tired but relieved. {STYLE}.",
    ),
]

# --- api helpers -------------------------------------------------------------


def post(tool, payload, timeout=180):
    req = urllib.request.Request(
        f"{API}/{tool}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN},
    )
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def submit(model, prompt, image_b64=None, duration="5"):
    body = {
        "model_name": model,
        "prompt": prompt[:2400],
        "negative_prompt": NEGATIVE[:2400],
        "cfg_scale": 0.5,
        "mode": "std",
        "duration": duration,
    }
    if image_b64:
        body["image"] = image_b64
        tool = "image2video"
    else:
        body["aspect_ratio"] = "16:9"
        tool = "text2video"
    r = post(tool, body)
    if r.get("code") != 0:
        raise RuntimeError(f"submit failed: {r.get('msg') or r.get('message')}")
    return r["data"]["task_id"]


def wait(task_id, timeout=2400):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        r = post("query_text2video", {"task_id": task_id}, timeout=90)
        if r.get("code") != 0:
            # transient plugin/quota errors: keep polling, the task still runs
            last = r.get("msg") or r.get("message")
            time.sleep(30)
            continue
        d = r["data"]
        if d["task_status"] == "succeed":
            return d["task_result"]["videos"][0]["url"]
        if d["task_status"] == "failed":
            raise RuntimeError(f"{task_id} failed: {d.get('task_status_msg')}")
        time.sleep(20)
    raise TimeoutError(f"{task_id} timed out (last api msg: {last})")


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(path, "wb") as f:
        f.write(r.read())
    return path


# --- ffmpeg helpers ----------------------------------------------------------


def duration_of(path):
    return float(
        subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    )


def last_frame_b64(video, png):
    seek = max(duration_of(video) - 0.1, 0)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", f"{seek:.3f}", "-i", video,
         "-frames:v", "1", "-vf", "scale=1280:-2", png],
        check=True,
    )
    return base64.b64encode(open(png, "rb").read()).decode()


def concat(paths, out, outdir):
    lst = os.path.join(outdir, "concat.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
         "-r", "30", "-an", out],
        check=True,
    )
    return out


def contact_sheet(video, out, tiles="4x3"):
    cols, rows = (int(x) for x in tiles.split("x"))
    step = duration_of(video) / (cols * rows)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", video,
         "-vf", f"fps=1/{step:.3f},scale=400:-2,tile={tiles}",
         "-frames:v", "1", out],
        check=True,
    )
    return out


# --- main --------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="kling-v2-1-master")
    ap.add_argument("--out", default=os.path.join(ROOT, "out_jokebear_v2"))
    ap.add_argument("--concat", action="store_true")
    ap.add_argument("--redo", nargs="*", type=int, default=[])
    args = ap.parse_args()

    outdir = args.out
    os.makedirs(outdir, exist_ok=True)
    final = os.path.join(outdir, "jokebear_last_coffee_30s.mp4")
    paths = [os.path.join(outdir, f"{n}.mp4") for n, _ in BEATS]

    for i in args.redo:
        p = paths[i - 1]
        if os.path.exists(p):
            os.remove(p)
            print(f"[redo] removed {p}", flush=True)

    if not args.concat:
        seed = None
        for (name, prompt), path in zip(BEATS, paths):
            if os.path.exists(path):
                print(f"[skip] {name}", flush=True)
            else:
                tid = submit(args.model, prompt, image_b64=seed)
                print(f"[{name}] task {tid}", flush=True)
                download(wait(tid), path)
                print(f"[{name}] saved ({duration_of(path):.1f}s)", flush=True)
            seed = last_frame_b64(path, os.path.join(outdir, f"{name}_last.png"))

    concat(paths, final, outdir)
    sheet = contact_sheet(final, os.path.join(outdir, "contact_sheet.jpg"))
    print(f"FINAL {final} {duration_of(final):.2f}s")
    print(f"SHEET {sheet}")


if __name__ == "__main__":
    main()
