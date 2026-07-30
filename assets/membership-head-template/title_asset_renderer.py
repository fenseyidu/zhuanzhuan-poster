#!/usr/bin/env python3
"""Render an A/S membership title asset using its route-owned width rule."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent


def measure(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--canvas-width", type=int, default=2250)
    args = parser.parse_args()

    cfg = json.loads((ROOT / "template.json").read_text())
    spec = cfg["title_layer"]["layout"]
    scale = args.canvas_width / spec["reference_width"]
    probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    max_width = round(spec["max_width"] * scale)
    nominal_size = round(spec["font_size"] * scale)
    font = ImageFont.truetype(str(ROOT / "fonts" / "SourceHanSerifSC-Heavy.otf"), nominal_size)
    title_width, _ = measure(draw, args.text, font)
    resolved_size = nominal_size
    if title_width > max_width:
        resolved_size = max(1, int(nominal_size * max_width / title_width))
        font = ImageFont.truetype(str(ROOT / "fonts" / "SourceHanSerifSC-Heavy.otf"), resolved_size)
        while measure(draw, args.text, font)[0] > max_width:
            resolved_size -= 1
            font = ImageFont.truetype(str(ROOT / "fonts" / "SourceHanSerifSC-Heavy.otf"), resolved_size)
    title_width, _ = measure(draw, args.text, font)
    _, glyph_height = measure(draw, "测", font)
    padding = round(12 * scale)
    image = Image.new(
        "RGBA",
        (title_width + padding * 2, glyph_height + padding * 2),
        (0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(image)
    left, top, right, _ = draw.textbbox((0, 0), args.text, font=font)
    x = (image.width - (right - left)) // 2 - left
    y = padding - top
    draw.text((x, y), args.text, font=font, fill=(255, 255, 255, 255))
    output = Path(args.output).with_suffix(".png")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(json.dumps({"png": str(output), "lines": [args.text], "fontSize": resolved_size, "maxWidth": max_width, "shrunk": resolved_size < nominal_size}, ensure_ascii=False))


if __name__ == "__main__":
    main()
