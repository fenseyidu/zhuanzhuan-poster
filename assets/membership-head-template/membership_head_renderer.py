#!/usr/bin/env python3
"""Compose a membership-day AI base with code-drawn fixed layers."""
import argparse, colorsys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parent
FONT = ROOT / 'fonts' / 'Alibaba_PuHuiTi_2.0_55_Regular_55_Regular.ttf'

def hex_color(rgb): return '#%02X%02X%02X' % tuple(max(0, min(255, round(x))) for x in rgb)
def rgb_color(value):
    value = value.lstrip('#')
    if len(value) != 6:
        raise SystemExit('--brand-color must be a six-digit hex color, such as #7E4504')
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
def luminance(rgb):
    r, g, b = [x / 255 for x in rgb]
    return .2126*r + .7152*g + .0722*b
def shade(rgb, target):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in rgb))
    return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, target, max(.22, min(.82, s))))
def sample(image, box):
    crop = image.crop(box).convert('RGB')
    return ImageStat.Stat(crop).mean
def font(size):
    if not FONT.is_file():
        raise SystemExit(f'Missing bundled font: {FONT}')
    return ImageFont.truetype(str(FONT), size)

def paste_tinted_mask(canvas, source, box, color):
    """Use only the source PNG's alpha channel; the fill color is always dynamic."""
    alpha = Image.open(source).convert('RGBA').getchannel('A').resize((box['width'], box['height']), Image.Resampling.LANCZOS)
    image = Image.new('RGBA', alpha.size, color + (0,))
    image.putalpha(alpha)
    canvas.alpha_composite(image, (box['x'], box['y']))

def draw_centered(draw, box, text, text_font, fill):
    left, top, right, bottom = draw.textbbox((0, 0), text, font=text_font)
    x = box['x'] + (box['width'] - (right - left)) / 2 - left
    y = box['y'] + (box['height'] - (bottom - top)) / 2 - top
    draw.text((x, y), text, font=text_font, fill=fill)

def draw_wave(canvas, box, fill, curve_height):
    """Draw the MasterGo bottom sweep as two mirrored quadratic curves."""
    half = box['width'] / 2
    points = []
    for x in range(box['width'] + 1):
        t = x / half if x <= half else (box['width'] - x) / half
        y = box['y'] + curve_height * (2 * t - t * t)
        points.append((box['x'] + x, round(y)))
    points.extend(((box['x'] + box['width'], box['y'] + box['height']), (box['x'], box['y'] + box['height'])))
    ImageDraw.Draw(canvas).polygon(points, fill=fill)
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-image', required=True)
    p.add_argument('--brand-asset', default=str(ROOT / 'member-day-brand-mask.png'), help='MasterGo top-mark alpha-mask PNG asset.')
    p.add_argument('--brand-color', help='Optional #RRGGBB override for the member-day mark and date.')
    p.add_argument('--date-text', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    cfg = json.loads((ROOT / 'template.json').read_text())
    w, h = cfg['canvas']['width'], cfg['canvas']['height']
    base = Image.open(args.base_image).convert('RGBA')
    if base.size != (w, h): raise SystemExit(f'AI base must be {w}x{h}, got {base.size[0]}x{base.size[1]}')
    output = Path(args.output).with_suffix('.png'); output.parent.mkdir(parents=True, exist_ok=True)
    rb = cfg['rule_button']; local = sample(base, (rb['x']-30, rb['y'], w, min(h, rb['y']+rb['height'])))
    button = shade(local, .25 if luminance(local) > .52 else .77)
    rule_text = '#FFF9EC' if luminance(button) < .52 else '#3A250E'
    lower = sample(base, (0, int(h*.9), w, h)); wave = shade(lower, .92 if luminance(lower) < .62 else .97)
    brand = cfg['brand']; date = cfg['date']; rule = cfg['rule_text']; wave_box = cfg['wave']
    brand_local = sample(base, (brand['x'], brand['y'], brand['x'] + brand['width'], brand['y'] + brand['height']))
    brand_color = rgb_color(args.brand_color) if args.brand_color else shade(brand_local, .25 if luminance(brand_local) > .52 else .86)
    paste_tinted_mask(base, args.brand_asset, brand, brand_color)
    draw = ImageDraw.Draw(base)
    draw_centered(draw, date, args.date_text, font(72), hex_color(brand_color))
    rule_bounds = (rb['x'], rb['y'], rb['x'] + rb['width'], rb['y'] + rb['height'])
    draw.rounded_rectangle(rule_bounds, radius=rb['radius'], fill=hex_color(button))
    draw.rectangle((rb['x'] + rb['radius'], rb['y'], rb['x'] + rb['width'], rb['y'] + rb['height']), fill=hex_color(button))
    char_height = rule['height'] // 2
    rule_font = font(66)
    draw_centered(draw, {'x': rule['x'], 'y': rule['y'], 'width': rule['width'], 'height': char_height}, '规', rule_font, rule_text)
    draw_centered(draw, {'x': rule['x'], 'y': rule['y'] + char_height, 'width': rule['width'], 'height': char_height}, '则', rule_font, rule_text)
    draw_wave(base, wave_box, hex_color(wave), wave_box['curve_height'])
    base.convert('RGB').save(output, 'PNG')
    print(json.dumps({'png': str(output), 'brandColor': hex_color(brand_color), 'ruleButton': hex_color(button), 'ruleText': rule_text, 'wave': hex_color(wave)}, ensure_ascii=False))
if __name__ == '__main__': main()
