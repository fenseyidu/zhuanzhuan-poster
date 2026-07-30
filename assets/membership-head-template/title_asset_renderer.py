#!/usr/bin/env python3
"""Render an A/S membership title asset using its route-owned width rule."""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent


def measure(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def wrap(draw, text, font, max_width):
    lines = []
    for paragraph in text.splitlines() or [""]:
        words = re.findall(r"\S+", paragraph)
        if not words:
            lines.append("")
            continue
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if line and measure(draw, candidate, font)[0] > max_width:
                lines.append(line)
                if measure(draw, word, font)[0] <= max_width:
                    line = word
                    continue
                chunks, chunk = [], ""
                for char in word:
                    candidate = chunk + char
                    if chunk and measure(draw, candidate, font)[0] > max_width:
                        chunks.append(chunk)
                        chunk = char
                    else:
                        chunk = candidate
                lines.extend(chunks)
                line = chunk
            else:
                line = candidate
        lines.append(line)
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--canvas-width", type=int, default=2250)
    args = parser.parse_args()

    cfg = json.loads((ROOT / "template.json").read_text())
    spec = cfg["title_layer"]["layout"]
    scale = args.canvas_width / spec["reference_width"]
    font = ImageFont.truetype(str(ROOT / "fonts" / "SourceHanSerifSC-Heavy.otf"), round(spec["font_size"] * scale))
    probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    lines = wrap(draw, args.text, font, round(spec["max_width"] * scale))
    if len(lines) > spec["max_lines"]:
        raise SystemExit(f'title needs {len(lines)} lines; configured maximum is {spec["max_lines"]}')
    widths = [measure(draw, line, font)[0] for line in lines]
    _, glyph_height = measure(draw, "测", font)
    line_height = round(spec["line_height"] * scale)
    padding = round(12 * scale)
    image = Image.new(
        "RGBA",
        (max(widths, default=0) + padding * 2, glyph_height + max(0, len(lines) - 1) * line_height + padding * 2),
        (0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(image)
    for index, line in enumerate(lines):
        left, top, right, _ = draw.textbbox((0, 0), line, font=font)
        x = (image.width - (right - left)) // 2 - left
        y = padding + index * line_height - top
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
    output = Path(args.output).with_suffix(".png")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(json.dumps({"png": str(output), "lines": lines, "fontSize": round(spec["font_size"] * scale), "maxWidth": round(spec["max_width"] * scale)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
