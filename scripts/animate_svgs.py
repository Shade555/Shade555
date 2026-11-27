#!/usr/bin/env python3
"""Add lightweight, client-side SVG motion accents to every archive illustration."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def animate_all(base=ROOT):
    count = 0
    for path in (base / 'assets').rglob('*.svg'):
        source = path.read_text(encoding='utf-8')
        # Make repeated builds idempotent.
        source = re.sub(r'<!-- ARCHIVE MOTION START -->.*?<!-- ARCHIVE MOTION END -->', '', source, flags=re.S)
        match = re.search(r'viewBox=["\']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)\s*["\']', source)
        if not match:
            continue
        width, height = float(match.group(1)), float(match.group(2))
        top_y = max(5.0, min(height - 5.0, height * 0.10))
        bottom_y = max(5.0, min(height - 5.0, height * 0.90))
        radius = max(1.1, min(4.0, min(width, height) * 0.012))
        motion = f'''<!-- ARCHIVE MOTION START -->
<circle r="{radius:.2f}" fill="#fff1c9" opacity="0" filter="url(#archive-glow)">
  <animate attributeName="opacity" values="0;0.9;0" keyTimes="0;0.5;1" dur="5.8s" repeatCount="indefinite"/>
  <animateMotion dur="11s" repeatCount="indefinite" path="M 12 {top_y:.1f} H {width-12:.1f}"/>
</circle>
<circle r="{radius*0.62:.2f}" fill="#c9eaff" opacity="0">
  <animate attributeName="opacity" values="0;0.75;0" dur="7.2s" begin="1.7s" repeatCount="indefinite"/>
  <animateMotion dur="13s" repeatCount="indefinite" path="M {width-12:.1f} {bottom_y:.1f} H 12"/>
</circle>
<!-- ARCHIVE MOTION END -->'''
        # Add a local glow filter if this asset doesn't already define one.
        if 'id="archive-glow"' not in source:
            source = source.replace('</defs>', '<filter id="archive-glow"><feGaussianBlur stdDeviation="2.2"/></filter></defs>', 1) if '</defs>' in source else source.replace('>', '><defs><filter id="archive-glow"><feGaussianBlur stdDeviation="2.2"/></filter></defs>', 1)
        source = source.replace('</svg>', motion + '\n</svg>')
        path.write_text(source, encoding='utf-8')
        count += 1
    return count

if __name__ == '__main__':
    print(f'Animated {animate_all()} SVG assets.')
