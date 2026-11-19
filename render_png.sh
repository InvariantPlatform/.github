#!/usr/bin/env bash
# Render each profile SVG to a 2x PNG fallback (the GitHub mobile app cannot
# show SVG). Motion forced off, so the PNG is the finished state. Run after
# generate.py whenever the artwork changes.
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
for svg in profile/assets/*.svg; do
  name=$(basename "$svg" .svg)
  read -r W H < <(sed -n 's/.*viewBox="0 0 \([0-9]*\) \([0-9]*\)".*/\1 \2/p' "$svg" | head -1)
  printf '<!doctype html><body style="margin:0;background:#0b0d10"><img src="file://%s" width=%s height=%s style="display:block">' \
    "$PWD/$svg" "$W" "$H" > "$tmp/$name.html"
  google-chrome --headless=new --disable-gpu --hide-scrollbars --force-prefers-reduced-motion \
    --force-device-scale-factor=2 --window-size="$W,$H" --screenshot="$tmp/$name.png" "file://$tmp/$name.html" 2>/dev/null
  magick "$tmp/$name.png" -strip -define png:compression-level=9 "profile/assets/$name.png"
  echo "rendered profile/assets/$name.png"
done
