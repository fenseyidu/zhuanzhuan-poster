#!/usr/bin/env python3
"""Compose a membership-day AI base with code-drawn fixed layers."""
import argparse, colorsys, json, math
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parent
FONT = ROOT / 'fonts' / 'Alibaba_PuHuiTi_2.0_55_Regular_55_Regular.ttf'
SUBTITLE_POLICY = json.loads((ROOT.parent / 'subtitle-typography.json').read_text())

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
def relative_luminance(rgb):
    channels = []
    for value in rgb[:3]:
        value /= 255
        channels.append(value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4)
    return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2]
def contrast_ratio(foreground, background_luminance):
    foreground_luminance = relative_luminance(foreground)
    return (max(foreground_luminance, background_luminance) + .05) / (min(foreground_luminance, background_luminance) + .05)
def percentile(values, amount):
    if not values:
        return 0
    index = round((len(values) - 1) * amount)
    return values[index]
def region_luminances(image, box):
    crop = image.crop(box).convert('RGB')
    crop.thumbnail((160, 80), Image.Resampling.BILINEAR)
    return sorted(relative_luminance(pixel) for pixel in crop.getdata())
def contrast_score(luminances, color):
    return percentile(sorted(contrast_ratio(color, luminance) for luminance in luminances), .10)
def apply_reading_field(canvas, box, opacity, config):
    padding = config['padding']
    x0 = max(0, box['x'] - padding['x'])
    y0 = max(0, box['y'] - padding['y'])
    x1 = min(canvas.width, box['x'] + box['width'] + padding['x'])
    y1 = min(canvas.height, box['y'] + box['height'] + padding['y'])
    mask = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=config['radius'], fill=round(255 * opacity))
    mask = mask.filter(ImageFilter.GaussianBlur(config['blur_radius']))
    field = Image.new('RGBA', canvas.size, rgb_color(config['color']) + (0,))
    field.putalpha(mask)
    canvas.alpha_composite(field)
def resolve_text_color(canvas, box, target_ratio, config):
    candidates = {name: rgb_color(value) for name, value in config['candidates'].items()}
    def evaluate(image):
        luminances = region_luminances(image, (box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height']))
        scores = {name: contrast_score(luminances, color) for name, color in candidates.items()}
        name = max(scores, key=scores.get)
        return name, candidates[name], scores[name], scores
    name, color, score, scores = evaluate(canvas)
    if score >= target_ratio:
        return color, {'candidate': name, 'contrast': score, 'readingFieldOpacity': 0, 'scores': scores}
    for opacity in config['reading_field']['opacity_steps']:
        trial = canvas.copy()
        apply_reading_field(trial, box, opacity, config['reading_field'])
        name, color, score, scores = evaluate(trial)
        if score >= target_ratio:
            canvas.alpha_composite(trial)
            return color, {'candidate': name, 'contrast': score, 'readingFieldOpacity': opacity, 'scores': scores}
    apply_reading_field(canvas, box, config['reading_field']['opacity_steps'][-1], config['reading_field'])
    name, color, score, scores = evaluate(canvas)
    return color, {'candidate': name, 'contrast': score, 'readingFieldOpacity': config['reading_field']['opacity_steps'][-1], 'scores': scores}
def font(size):
    if not FONT.is_file():
        raise SystemExit(f'Missing bundled font: {FONT}')
    return ImageFont.truetype(str(FONT), size)

def subtitle_font_size(canvas_width):
    return round(SUBTITLE_POLICY['font_size'] * canvas_width / SUBTITLE_POLICY['reference_width'])

def paste_tinted_mask(canvas, source, box, color):
    """Use only the source PNG's alpha channel; the fill color is always dynamic."""
    alpha = Image.open(source).convert('RGBA').getchannel('A').resize((box['width'], box['height']), Image.Resampling.LANCZOS)
    image = Image.new('RGBA', alpha.size, color + (0,))
    image.putalpha(alpha)
    canvas.alpha_composite(image, (box['x'], box['y']))

def paste_tinted_title(canvas, source, box, color, visible_height, max_visible_width=None):
    """Crop alpha padding and fit the title inside its height and width limits."""
    alpha = Image.open(source).convert('RGBA').getchannel('A')
    bounds = alpha.getbbox()
    if not bounds:
        raise SystemExit('Title asset has no visible alpha content')
    alpha = alpha.crop(bounds)
    scale = visible_height / alpha.height
    if max_visible_width is not None:
        scale = min(scale, max_visible_width / alpha.width)
    size = (round(alpha.width * scale), round(alpha.height * scale))
    alpha = alpha.resize(size, Image.Resampling.LANCZOS)
    image = Image.new('RGBA', size, color + (0,))
    image.putalpha(alpha)
    x = box['x'] + (box['width'] - size[0]) // 2
    y = box['y'] + (box['height'] - size[1]) // 2
    canvas.alpha_composite(image, (x, y))

def paste_tinted_brand(canvas, source, box, color, visible_height):
    """Crop a transparent brand asset, preserve its ratio, and left-align it in its slot."""
    alpha = Image.open(source).convert('RGBA').getchannel('A')
    bounds = alpha.getbbox()
    if not bounds:
        raise SystemExit('Membership B brand asset has no visible alpha content')
    alpha = alpha.crop(bounds)
    scale = min(visible_height / alpha.height, box['width'] / alpha.width, box['height'] / alpha.height)
    size = (round(alpha.width * scale), round(alpha.height * scale))
    alpha = alpha.resize(size, Image.Resampling.LANCZOS)
    image = Image.new('RGBA', size, color + (0,))
    image.putalpha(alpha)
    x = box['x']
    y = box['y'] + (box['height'] - size[1]) // 2
    canvas.alpha_composite(image, (x, y))

def measure_membership_b_title(canvas, config):
    """Find the generated main-title ink inside the reserved left title region."""
    search = config['title_measurement']['search_box']
    x0, y0 = search['x'], search['y']
    x1, y1 = x0 + search['width'], y0 + search['height']
    pixels = canvas.convert('RGB').crop((x0, y0, x1, y1)).load()
    points, core_colors = [], []
    for y in range(y1 - y0):
        for x in range(x1 - x0):
            rgb = pixels[x, y]
            high, low = max(rgb), min(rgb)
            value = high / 255
            saturation = 0 if high == 0 else (high - low) / high
            lightness = relative_luminance(rgb)
            # Warm or colored title ink is separated from the pale background by
            # saturation; dark neutral title ink is accepted through luminance.
            if (value < .76 and saturation > .16) or lightness < .36:
                points.append((x + x0, y + y0))
                if value < .62:
                    core_colors.append(rgb)
    if len(points) < config['title_measurement']['minimum_pixels']:
        raise SystemExit('Could not measure Membership B main-title pixels; pass --title-color as an explicit fallback.')
    xs, ys = zip(*points)
    color_samples = core_colors or [pixels[x - x0, y - y0] for x, y in points]
    # The most frequent opaque ink pixel avoids averaging anti-aliased edges
    # into an off-color brand mark.
    title_color = Counter(color_samples).most_common(1)[0][0]
    return {
        'box': {'x': min(xs), 'y': min(ys), 'width': max(xs) - min(xs) + 1, 'height': max(ys) - min(ys) + 1},
        'color': title_color,
        'pixelCount': len(points),
    }

def resolve_membership_b_brand_layer(canvas, layer, title_color_override):
    measured = measure_membership_b_title(canvas, layer)
    title_box = measured['box']
    sizing = layer['title_measurement']
    height = layer['visible_height']
    box = dict(layer['box'])
    box['x'] = title_box['x']
    box['height'] = height
    box['y'] = max(0, title_box['y'] - sizing['vertical_gap'] - height)
    color = rgb_color(title_color_override) if title_color_override else measured['color']
    return box, color, height, {
        'titleBox': title_box,
        'titlePixelCount': measured['pixelCount'],
        'titleColorSource': 'explicit_override' if title_color_override else 'measured_generated_title',
    }

def resolve_membership_b_brand_from_layout(layer, title_layout, title_color_override):
    boxes = title_layout.get('title', {}).get('visibleBoxes', [])
    if not boxes:
        raise SystemExit('Title layout trace has no visible main-title box')
    left = min(box['x'] for box in boxes)
    top = min(box['y'] for box in boxes)
    right = max(box['x'] + box['width'] for box in boxes)
    bottom = max(box['y'] + box['height'] for box in boxes)
    title_box = {'x': left, 'y': top, 'width': right - left, 'height': bottom - top}
    color = rgb_color(title_color_override or title_layout['title']['color'])
    height = layer['visible_height']
    box = dict(layer['box'])
    box['x'] = title_box['x']
    box['height'] = height
    box['y'] = max(0, title_box['y'] - layer['title_measurement']['vertical_gap'] - height)
    return box, color, height, {
        'titleBox': title_box,
        'titleColorSource': 'explicit_override' if title_color_override else 'local_title_layout',
        'titleLayout': title_layout.get('traceOutput'),
    }

def normalize_membership_b_title_layout(title_layout, normalization):
    if not normalization:
        return title_layout
    source_width, source_height = normalization['sourceSize']
    resized_width, resized_height = normalization['resizedSize']
    crop_left, crop_top, _, _ = normalization['crop']
    scale_x = resized_width / source_width
    scale_y = resized_height / source_height
    normalized = dict(title_layout)
    normalized['title'] = dict(title_layout['title'])
    normalized['title']['visibleBoxes'] = [
        {
            'x': round(box['x'] * scale_x - crop_left),
            'y': round(box['y'] * scale_y - crop_top),
            'width': round(box['width'] * scale_x),
            'height': round(box['height'] * scale_y),
        }
        for box in title_layout['title']['visibleBoxes']
    ]
    return normalized

def normalize_base(base, target_size):
    """Cover-crop a generated base to the template while preserving its lower foreground."""
    target_width, target_height = target_size
    if base.size == target_size:
        return base, None
    scale = max(target_width / base.width, target_height / base.height)
    resized = base.resize(
        (math.ceil(base.width * scale), math.ceil(base.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_width) // 2
    top = resized.height - target_height
    crop = (left, top, left + target_width, top + target_height)
    return resized.crop(crop), {
        'sourceSize': base.size,
        'resizedSize': resized.size,
        'crop': crop,
        'anchor': 'horizontal_center_vertical_bottom',
    }

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
    p.add_argument('--mode', choices=('membership-as', 'membership-b'), default='membership-as')
    p.add_argument('--base-image', required=True)
    p.add_argument('--title-asset', help='Transparent PNG containing only the approved A/S title-only generation result.')
    p.add_argument('--title-color', help='A/S title override; for Membership B, use only as an explicit fallback when generated-title color measurement fails.')
    p.add_argument('--brand-asset', default=str(ROOT / 'member-day-brand-mask.png'), help='MasterGo top-mark alpha-mask PNG asset.')
    p.add_argument('--brand-color', help='Optional #RRGGBB override for the member-day mark and date.')
    p.add_argument('--member-b-brand-asset', help='Optional transparent Membership B brand asset override.')
    p.add_argument('--title-layout', help='JSON trace emitted by text_layout_renderer.py for Membership B local-title placement.')
    p.add_argument('--date-text')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    cfg = json.loads((ROOT / 'template.json').read_text())
    w, h = cfg['canvas']['width'], cfg['canvas']['height']
    base = Image.open(args.base_image).convert('RGBA')
    base, base_normalization = normalize_base(base, (w, h))
    output = Path(args.output).with_suffix('.png'); output.parent.mkdir(parents=True, exist_ok=True)
    if args.mode == 'membership-b':
        layer = cfg['membership_b_brand_layer']
        asset = Path(args.member_b_brand_asset) if args.member_b_brand_asset else ROOT / layer['asset']
        if not asset.is_file():
            p.error(f'Membership B brand asset does not exist: {asset}')
        title_layout = json.loads(Path(args.title_layout).read_text()) if args.title_layout else None
        title_layout = normalize_membership_b_title_layout(title_layout, base_normalization) if title_layout else None
        box, color, visible_height, trace = (
            resolve_membership_b_brand_from_layout(layer, title_layout, args.title_color)
            if title_layout else resolve_membership_b_brand_layer(base, layer, args.title_color)
        )
        paste_tinted_brand(base, asset, box, color, visible_height)
        base.convert('RGB').save(output, 'PNG')
        print(json.dumps({
            'mode': args.mode,
            'png': str(output),
            'baseNormalization': base_normalization,
            'memberBrandAsset': str(asset),
            'memberBrandColor': hex_color(color),
            'memberBrandBox': box,
            'memberBrandVisibleHeight': visible_height,
            'memberBrandPlacement': trace,
        }, ensure_ascii=False))
        return
    if not args.title_asset or not args.date_text:
        p.error('--title-asset and --date-text are required in membership-as mode')
    contrast_config = cfg['text_contrast']
    reference_colors = cfg.get('reference_text_colors')
    title = cfg['title_layer']; title_box = title['box']
    brand = cfg['brand']; date = cfg['date']; rule = cfg['rule_text']; wave_box = cfg['wave']
    if args.title_color:
        title_color, title_trace = rgb_color(args.title_color), {'candidate': 'user_override', 'contrast': None, 'readingFieldOpacity': 0}
    elif reference_colors:
        title_color, title_trace = rgb_color(reference_colors['title']), {'candidate': 'reference_default', 'contrast': None, 'readingFieldOpacity': 0}
    else:
        title_color, title_trace = resolve_text_color(base, title_box, contrast_config['minimum_contrast']['title'], contrast_config)
    if args.brand_color:
        brand_color = date_color = rgb_color(args.brand_color)
        brand_trace = date_trace = {'candidate': 'user_override', 'contrast': None, 'readingFieldOpacity': 0}
    elif reference_colors:
        brand_color = rgb_color(reference_colors['brand'])
        date_color = rgb_color(reference_colors['date'])
        brand_trace = date_trace = {'candidate': 'reference_default', 'contrast': None, 'readingFieldOpacity': 0}
    else:
        brand_color, brand_trace = resolve_text_color(base, brand, contrast_config['minimum_contrast']['brand'], contrast_config)
        date_color, date_trace = resolve_text_color(base, date, contrast_config['minimum_contrast']['date'], contrast_config)
    paste_tinted_title(
        base, args.title_asset, title_box, title_color,
        title.get('visible_height', title_box['height']), title.get('max_visible_width'),
    )
    rb = cfg['rule_button']; local = sample(base, (rb['x']-30, rb['y'], w, min(h, rb['y']+rb['height'])))
    button = shade(local, .25 if luminance(local) > .52 else .77)
    rule_text = '#FFF9EC' if luminance(button) < .52 else '#3A250E'
    lower = sample(base, (0, int(h*.9), w, h)); wave = shade(lower, .92 if luminance(lower) < .62 else .97)
    paste_tinted_mask(base, args.brand_asset, brand, brand_color)
    draw = ImageDraw.Draw(base)
    draw_centered(draw, date, args.date_text, font(subtitle_font_size(w)), hex_color(date_color))
    rule_bounds = (rb['x'], rb['y'], rb['x'] + rb['width'], rb['y'] + rb['height'])
    draw.rounded_rectangle(rule_bounds, radius=rb['radius'], fill=hex_color(button))
    draw.rectangle((rb['x'] + rb['radius'], rb['y'], rb['x'] + rb['width'], rb['y'] + rb['height']), fill=hex_color(button))
    char_height = rule['height'] // 2
    rule_font = font(66)
    draw_centered(draw, {'x': rule['x'], 'y': rule['y'], 'width': rule['width'], 'height': char_height}, '规', rule_font, rule_text)
    draw_centered(draw, {'x': rule['x'], 'y': rule['y'] + char_height, 'width': rule['width'], 'height': char_height}, '则', rule_font, rule_text)
    draw_wave(base, wave_box, hex_color(wave), wave_box['curve_height'])
    base.convert('RGB').save(output, 'PNG')
    print(json.dumps({'png': str(output), 'baseNormalization': base_normalization, 'titleColor': hex_color(title_color), 'brandColor': hex_color(brand_color), 'dateColor': hex_color(date_color), 'textContrast': {'title': title_trace, 'brand': brand_trace, 'date': date_trace}, 'ruleButton': hex_color(button), 'ruleText': rule_text, 'wave': hex_color(wave)}, ensure_ascii=False))
if __name__ == '__main__': main()
