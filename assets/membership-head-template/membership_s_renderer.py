#!/usr/bin/env python3
"""Render the live MasterGo membership-S text group over a 2:1 generated base."""
import argparse
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PROFILE = ROOT / 'profiles' / 'membership-s-2x1.json'
TITLE_FONT = ROOT / 'fonts' / 'SourceHanSerifSC-Heavy.otf'
SUBTITLE_FONT = ROOT / 'fonts' / 'Alibaba_PuHuiTi_2.0_55_Regular_55_Regular.ttf'


def rgb_color(value):
    value = value.lstrip('#')
    if len(value) != 6:
        raise SystemExit('--text-color must be a six-digit hex color, such as #F4E2BC')
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def hex_color(rgb):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(value))) for value in rgb)


def relative_luminance(rgb):
    channels = []
    for value in rgb[:3]:
        value /= 255
        channels.append(value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4)
    return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2]


def contrast_ratio(color, background_luminance):
    foreground = relative_luminance(color)
    return (max(foreground, background_luminance) + .05) / (min(foreground, background_luminance) + .05)


def region_luminances(image, box):
    crop = image.crop((box['x'], box['y'], box['x'] + box['width'], box['y'] + box['height'])).convert('RGB')
    crop.thumbnail((160, 80), Image.Resampling.BILINEAR)
    return sorted(relative_luminance(pixel) for pixel in crop.getdata())


def percentile(values, fraction):
    return values[round((len(values) - 1) * fraction)] if values else 0


def normalize_base(base, target_size):
    if base.size == target_size:
        return base, None
    scale = max(target_size[0] / base.width, target_size[1] / base.height)
    resized = base.resize((math.ceil(base.width * scale), math.ceil(base.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_size[0]) // 2
    top = (resized.height - target_size[1]) // 2
    crop = (left, top, left + target_size[0], top + target_size[1])
    return resized.crop(crop), {
        'sourceSize': base.size,
        'resizedSize': resized.size,
        'crop': crop,
        'anchor': 'horizontal_center_vertical_center',
    }


def wrap_lines(draw, text, font, max_width):
    """Wrap subtitle text when it exceeds the shared MasterGo text region."""
    lines = []
    for paragraph in text.splitlines() or ['']:
        line = ''
        for character in paragraph:
            candidate = line + character
            if line and draw.textbbox((0, 0), candidate, font=font)[2] > max_width:
                lines.append(line)
                line = character
            else:
                line = candidate
        lines.append(line)
    return lines


def split_title(title_text):
    pieces = [piece.strip() for piece in re.split(r'[xX×]', title_text, maxsplit=1)]
    return pieces if len(pieces) == 2 and all(pieces) else None


def fit_single_line_title_font(draw, title_parts, default_size):
    """Return the largest title font that keeps every supplied title part on one line."""
    for size in range(default_size, 0, -1):
        font = ImageFont.truetype(str(TITLE_FONT), size)
        if all(draw.textbbox((0, 0), text, font=font)[2] <= max_width
               for text, max_width in title_parts):
            return font
    raise SystemExit('Unable to fit membership-S title inside its reading region')


def resolve_layout(config, title_text, subtitle_text):
    canvas = Image.new('RGBA', (config['canvas']['width'], config['canvas']['height']))
    draw = ImageDraw.Draw(canvas)
    region = config['text_region']
    subtitle_font = ImageFont.truetype(str(SUBTITLE_FONT), config['subtitle']['font_size'])
    title_pieces = split_title(title_text)
    split_config = config['split_title']
    if title_pieces:
        title_font = fit_single_line_title_font(
            draw,
            [(title_pieces[0], split_config['left']['width']),
             (title_pieces[1], split_config['right']['width'])],
            config['title']['font_size'],
        )
    else:
        title_font = fit_single_line_title_font(
            draw, [(title_text, region['width'])], config['title']['font_size']
        )
    title_line_count = 1
    subtitle_lines = wrap_lines(draw, subtitle_text, subtitle_font, region['width'])
    vertical = config['vertical_group']
    total_height = (
        vertical['logo_visible_height']
        + vertical['logo_title_gap']
        + title_line_count * vertical['title_line_height']
        + vertical['title_subtitle_gap']
        + len(subtitle_lines) * vertical['subtitle_line_height']
    )
    group_top = round(vertical['center_y'] - total_height / 2)
    title_y = group_top + vertical['logo_visible_height'] + vertical['logo_title_gap']
    subtitle_y = title_y + title_line_count * vertical['title_line_height'] + vertical['title_subtitle_gap']
    scale = config['canvas']['width'] / config['reference_canvas']['width']
    logo_box = {
        'x': round(config['logo']['x']),
        'y': group_top,
        'width': round(config['logo']['reference_full_size']['width'] * scale),
        'height': round(config['logo']['reference_full_size']['height'] * scale),
    }
    title_reading_box = {
        'x': region['x'],
        'y': title_y,
        'width': region['width'],
        'height': title_line_count * vertical['title_line_height'],
    }
    if title_pieces:
        left_lines = [title_pieces[0]]
        right_lines = [title_pieces[1]]
        separator_font_size = max(
            1,
            round(split_config['separator']['font_size'] * title_font.size / config['title']['font_size']),
        )
        title = {
            'variant': 'split_on_x',
            'sourceSeparator': re.search(r'[xX×]', title_text).group(0),
            'readingBox': title_reading_box,
            'left': {
                'font': title_font,
                'lines': left_lines,
                'x': split_config['left']['x'],
                'y': title_y + (title_line_count - len(left_lines)) * vertical['title_line_height'] / 2,
                'width': split_config['left']['width'],
                'lineHeight': vertical['title_line_height'],
            },
            'right': {
                'font': title_font,
                'lines': right_lines,
                'x': split_config['right']['x'],
                'y': title_y + (title_line_count - len(right_lines)) * vertical['title_line_height'] / 2,
                'width': split_config['right']['width'],
                'lineHeight': vertical['title_line_height'],
            },
            'separator': {
                'text': split_config['separator']['text'],
                'font': ImageFont.truetype(str(TITLE_FONT), separator_font_size),
                'x': split_config['separator']['x'],
                'y': title_y + (title_line_count * vertical['title_line_height'] - separator_font_size) / 2,
                'width': split_config['separator']['width'],
                'height': separator_font_size,
            },
        }
    else:
        title = {
            'variant': 'plain',
            'readingBox': title_reading_box,
            'main': {
                'font': title_font,
                'lines': [title_text],
                'x': region['x'],
                'y': title_y,
                'width': region['width'],
                'lineHeight': vertical['title_line_height'],
            },
        }
    return {
        'logo': logo_box,
        'title': title,
        'subtitle': {
            'font': subtitle_font,
            'lines': subtitle_lines,
            'x': region['x'],
            'y': subtitle_y,
            'width': region['width'],
            'lineHeight': vertical['subtitle_line_height'],
        },
        'verticalGroup': {
            'alignment': vertical['alignment'],
            'centerY': vertical['center_y'],
            'top': group_top,
            'bottom': group_top + total_height,
            'height': total_height,
        },
    }


def reading_box(layout_part):
    if 'readingBox' in layout_part:
        return layout_part['readingBox']
    return {
        'x': layout_part['x'],
        'y': layout_part['y'],
        'width': layout_part['width'],
        'height': len(layout_part['lines']) * layout_part['lineHeight'],
    }


def resolve_text_color(canvas, config, boxes, override):
    if override:
        return rgb_color(override), {'source': 'explicit_override'}
    candidates = {name: rgb_color(value) for name, value in config['text_color']['candidates'].items()}
    luminances = []
    for box in boxes:
        luminances.extend(region_luminances(canvas, box))
    sampling_percentile = config['text_color'].get('sampling_percentile', .50)
    scores = {
        name: percentile(
            sorted(contrast_ratio(color, value) for value in luminances),
            sampling_percentile,
        )
        for name, color in candidates.items()
    }
    name = max(scores, key=scores.get)
    return candidates[name], {
        'source': 'background_adaptive',
        'candidate': name,
        'contrast': scores[name],
        'minimumContrast': config['text_color']['minimum_contrast'],
        'samplingPercentile': sampling_percentile,
        'scores': scores,
    }


def paste_tinted_mastergo_logo(canvas, config, color, box):
    logo = config['logo']
    asset = (PROFILE.parent / logo['asset']).resolve()
    if not asset.is_file():
        raise SystemExit(f'Missing bundled membership logo: {asset}')
    alpha = Image.open(asset).convert('RGBA').getchannel('A')
    scale = config['canvas']['width'] / config['reference_canvas']['width']
    full_size = (
        round(logo['reference_full_size']['width'] * scale),
        round(logo['reference_full_size']['height'] * scale),
    )
    alpha = alpha.resize(full_size, Image.Resampling.LANCZOS)
    tinted = Image.new('RGBA', alpha.size, color + (0,))
    tinted.putalpha(alpha)
    canvas.alpha_composite(tinted, (box['x'], box['y']))
    return asset


def render_centered_lines(draw, layout_part, color):
    visible_boxes = []
    for index, line in enumerate(layout_part['lines']):
        left, top, right, bottom = draw.textbbox((0, 0), line, font=layout_part['font'])
        text_width = right - left
        text_height = bottom - top
        row_y = layout_part['y'] + index * layout_part['lineHeight']
        x = layout_part['x'] + (layout_part['width'] - text_width) / 2 - left
        y = row_y + (layout_part['lineHeight'] - text_height) / 2 - top
        draw.text((x, y), line, font=layout_part['font'], fill=color)
        visible_boxes.append({
            'x': round(x + left),
            'y': round(y + top),
            'width': round(text_width),
            'height': round(text_height),
        })
    return {
        'lines': layout_part['lines'],
        'fontSize': layout_part['font'].size,
        'visibleBoxes': visible_boxes,
        'readingBox': reading_box(layout_part),
    }


def render_centered_text(draw, layout_part, color):
    left, top, right, bottom = draw.textbbox((0, 0), layout_part['text'], font=layout_part['font'])
    text_width = right - left
    text_height = bottom - top
    x = layout_part['x'] + (layout_part['width'] - text_width) / 2 - left
    y = layout_part['y'] + (layout_part['height'] - text_height) / 2 - top
    draw.text((x, y), layout_part['text'], font=layout_part['font'], fill=color)
    return {
        'text': layout_part['text'],
        'fontSize': layout_part['font'].size,
        'visibleBox': {
            'x': round(x + left), 'y': round(y + top),
            'width': round(text_width), 'height': round(text_height),
        },
    }


def render_title(draw, layout, color):
    title = layout['title']
    if title['variant'] == 'plain':
        trace = render_centered_lines(draw, title['main'], color)
        trace['variant'] = 'plain'
        return trace
    return {
        'variant': 'split_on_x',
        'sourceSeparator': title['sourceSeparator'],
        'left': render_centered_lines(draw, title['left'], color),
        'separator': render_centered_text(draw, title['separator'], color),
        'right': render_centered_lines(draw, title['right'], color),
        'readingBox': title['readingBox'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-image', required=True)
    parser.add_argument('--membership-theme', choices=('圣诞', '中秋'), required=True,
                        help='Selects the S background route only; it never supplies title copy.')
    parser.add_argument('--title', required=True, help='Exact live main-title copy from MasterGo.')
    parser.add_argument('--subtitle', required=True, help='Exact live subtitle copy from MasterGo.')
    parser.add_argument('--text-color', help='Optional #RRGGBB override. By default, color is selected from the background.')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    config = json.loads(PROFILE.read_text())
    canvas_size = (config['canvas']['width'], config['canvas']['height'])
    base, normalization = normalize_base(Image.open(args.base_image).convert('RGBA'), canvas_size)
    layout = resolve_layout(config, args.title, args.subtitle)
    color, color_trace = resolve_text_color(
        base,
        config,
        [layout['logo'], reading_box(layout['title']), reading_box(layout['subtitle'])],
        args.text_color,
    )
    draw = ImageDraw.Draw(base)
    title_trace = render_title(draw, layout, color)
    subtitle_trace = render_centered_lines(draw, layout['subtitle'], color)
    logo_asset = paste_tinted_mastergo_logo(base, config, color, layout['logo'])
    output = Path(args.output).with_suffix('.png')
    output.parent.mkdir(parents=True, exist_ok=True)
    base.convert('RGB').save(output, 'PNG')
    print(json.dumps({
        'mode': 'membership-s',
        'png': str(output),
        'baseNormalization': normalization,
        'membershipTheme': args.membership_theme,
        'title': title_trace,
        'subtitle': subtitle_trace,
        'verticalGroup': layout['verticalGroup'],
        'logoAsset': str(logo_asset),
        'logoBox': layout['logo'],
        'textColor': hex_color(color),
        'textColorTrace': color_trace,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
