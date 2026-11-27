#!/usr/bin/env bash
# One-time setup for the video pipeline on a fresh machine or cloud container.
# Creates a venv with the TTS model runtime, and checks ffmpeg and Playwright.
# Afterwards: ~/.cache/playbook-tts/venv/bin/python tools/video/make_video.py <id>
set -euo pipefail
VENV="$HOME/.cache/playbook-tts/venv"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet kokoro-onnx soundfile numpy
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg missing: install it (apt-get install -y ffmpeg)"; exit 1; }
node -e "require('playwright')" 2>/dev/null || { echo "Playwright missing: npm i -g playwright && npx playwright install chromium"; exit 1; }
echo "video pipeline ready: $VENV/bin/python tools/video/make_video.py <id>"
