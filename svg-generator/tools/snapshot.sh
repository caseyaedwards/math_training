#!/bin/sh
# Renders an SVG file to PNG with headless Chrome, for checking layout by eye.
# Usage: tools/snapshot.sh input.svg output.png
set -e
in="$1"
out="$2"
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
size=$(python3 - "$in" <<'PY'
import re, sys
head = open(sys.argv[1], encoding="utf-8").read(2000)
w = re.search(r'<svg[^>]*\swidth="([\d.]+)"', head).group(1)
h = re.search(r'<svg[^>]*\sheight="([\d.]+)"', head).group(1)
print(f"{int(float(w) + 0.99)},{int(float(h) + 0.99)}")
PY
)
abs_in=$(cd "$(dirname "$in")" && pwd)/$(basename "$in")
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size="$size" --screenshot="$out" "file://$abs_in" >/dev/null 2>&1
echo "$out"
