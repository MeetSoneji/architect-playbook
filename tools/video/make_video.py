#!/usr/bin/env python3
"""make_video.py <concept id> [--fps 24] [--preview]

Turns concepts/<module>/<id>-<slug>/video/{script.json, scenes.js} into a narrated vertical MP4:

  1. Narration: each scene's `say` text is spoken by Kokoro, an open text-to-speech model that runs locally.
  2. Timing: scene lengths come from the narration, so visuals and captions follow the voice.
  3. Page: tools/video/engine.html + the concept's scenes.js, rendered frame by frame with Playwright.
  4. Music: a soft synth pad generated here (no licensing questions), ducked under the voice.
  5. ffmpeg muxes frames, voice and music into build/<id>/<id>-video.mp4.

Requirements (not needed for the rest of the repo): ffmpeg, Node + Playwright, and a venv with
`pip install kokoro-onnx soundfile numpy`. Model files are downloaded on first run into ~/.cache/playbook-tts.
--preview writes only the HTML page (silent, autoplaying) and the timing, without rendering frames.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import playbook  # noqa: E402

SR = 24000
CACHE = Path.home() / ".cache" / "playbook-tts"
MODEL_URLS = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
}
LEAD_IN, TAIL, END_HOLD = 0.35, 0.55, 1.4   # seconds of air before/after each scene's narration


def models() -> tuple[Path, Path]:
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, url in MODEL_URLS.items():
        if not (CACHE / name).exists():
            print(f"downloading {name} …")
            urllib.request.urlretrieve(url, CACHE / name)
    return CACHE / "kokoro-v1.0.onnx", CACHE / "voices-v1.0.bin"


def narrate(script: dict) -> list[np.ndarray]:
    from kokoro_onnx import Kokoro
    m, v = models()
    k = Kokoro(str(m), str(v))
    out = []
    for s in script["scenes"]:
        audio, sr = k.create(s["say"], voice=script.get("voice", "af_heart"), speed=script.get("speed", 1.0), lang="en-us")
        assert sr == SR
        out.append(np.asarray(audio, dtype=np.float32))
        print(f"  {s['id']:<8} {len(audio) / SR:5.1f}s")
    return out


def timing(clips: list[np.ndarray]) -> dict:
    t, scenes = 0.0, []
    for i, c in enumerate(clips):
        dur = len(c) / SR
        start = t
        end = start + LEAD_IN + dur + (END_HOLD if i == len(clips) - 1 else TAIL)
        scenes.append({"start": round(start, 3), "end": round(end, 3), "speech_start": round(start + LEAD_IN, 3), "speech_dur": round(dur, 3)})
        t = end
    return {"scenes": scenes, "total": round(t, 3)}


def music(total: float, speech: list[tuple[float, float]]) -> np.ndarray:
    """A slow four-chord pad (Am-F-C-G), soft sines with gentle attack, ducked under speech."""
    n = int(total * SR)
    t = np.arange(n) / SR
    chords = [[220.00, 261.63, 329.63], [174.61, 220.00, 261.63], [130.81, 196.00, 261.63], [196.00, 246.94, 293.66]]
    bar = 4.0
    y = np.zeros(n, dtype=np.float32)
    for b in range(int(total // bar) + 1):
        a, z = int(b * bar * SR), min(n, int((b + 1) * bar * SR + 1.5 * SR))
        if a >= n:
            break
        tt = t[a:z] - b * bar
        env = np.minimum(1, tt / 1.2) * np.exp(-np.maximum(0, tt - bar) / 0.6)
        for f in chords[b % 4]:
            y[a:z] += (0.6 * np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt + 0.3) + 0.4 * np.sin(2 * np.pi * f / 2 * tt)) * env
        # a soft bell on each bar for movement
        bell = chords[b % 4][-1] * 2
        y[a:z] += 0.18 * np.sin(2 * np.pi * bell * tt) * np.exp(-tt / 0.9)
    y /= np.max(np.abs(y)) + 1e-9
    duck = np.full(n, 0.16, dtype=np.float32)
    for s, d in speech:
        duck[int(s * SR):int((s + d) * SR)] = 0.06
    k = int(0.25 * SR)
    duck = np.convolve(duck, np.ones(k) / k, mode="same")
    fade = np.minimum(1, np.minimum(t / 1.5, (total - t) / 2.0))
    return (y * duck * fade).astype(np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    c = playbook.load()["by_id"][a.id]
    vdir = c["dir"] / "video"
    script = json.loads((vdir / "script.json").read_text())
    out = ROOT / "build" / a.id
    out.mkdir(parents=True, exist_ok=True)

    print("1/5 narration")
    clips = narrate(script)
    tm = timing(clips)
    (out / "timing.json").write_text(json.dumps(tm, indent=1))

    print("2/5 page")
    page = (ROOT / "tools" / "video" / "engine.html").read_text()
    page = (page.replace("__TITLE__", script["title"]).replace("__SCRIPT__", json.dumps(script))
                .replace("__TIMING__", json.dumps(tm)).replace("__SCENES__", (vdir / "scenes.js").read_text()))
    (out / "video.html").write_text(page)
    if a.preview:
        print(f"preview: {out / 'video.html'} ({tm['total']:.1f}s)")
        return 0

    print("3/5 audio")
    voice = np.zeros(int(tm["total"] * SR) + SR, dtype=np.float32)
    for clip, s in zip(clips, tm["scenes"]):
        i = int(s["speech_start"] * SR)
        voice[i:i + len(clip)] += clip
    mix = voice[: int(tm["total"] * SR)] + music(tm["total"], [(s["speech_start"], s["speech_dur"]) for s in tm["scenes"]])
    mix *= 0.89 / (np.max(np.abs(mix)) + 1e-9)
    sf.write(out / "audio.wav", mix, SR)

    print("4/5 frames")
    frames = out / "frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    env_node = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(ROOT / "tools" / "video" / "frames.js"), str(out / "video.html"), str(frames), str(a.fps)],
                   check=True, env={**__import__("os").environ, "NODE_PATH": env_node})

    print("5/5 encode")
    mp4 = out / f"{a.id}-video.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(a.fps), "-i", str(frames / "f_%05d.png"),
                    "-i", str(out / "audio.wav"), "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(mp4)], check=True)
    shutil.rmtree(frames)
    print(f"done: {mp4} ({tm['total']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
