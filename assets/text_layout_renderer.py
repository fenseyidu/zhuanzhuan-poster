#!/usr/bin/env python3
"""Compose exact local title and subtitle copy from a registered layout profile."""
import argparse
import json
import re
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "text-layouts" / "registry.json"


def parse_color(value):
    value = value.lstrip("#")
    if len(value) != 6:
        raise SystemExit("configured colors must be six-digit hex values")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def merge_profile(parent, child):
    merged = deepcopy(parent)
    for key, value in child.items():
        if key == "extends":
            continue
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_profile(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def load_layout(profile_path, seen=None):
    profile_path = profile_path.resolve()
    seen = set() if seen is None else seen
    if profile_path in seen:
        raise SystemExit(f"cyclic text-layout inheritance at {profile_path}")
    seen.add(profile_path)
    profile = json.loads(profile_path.read_text())
    parent = profile.get("extends")
    if not parent:
        return profile
    return merge_profile(load_layout(profile_path.parent / parent, seen), profile)


def load_profile(profile_id):
    registry = json.loads(REGISTRY_PATH.read_text())
    entry = registry.get("profiles", {}).get(profile_id)
    if not entry:
        known = ", ".join(sorted(registry.get("profiles", {})))
        raise SystemExit(f"unknown text layout profile {profile_id!r}; known profiles: {known}")
    if not entry.get("pipeline") or entry["pipeline"][0] != "text_layout_renderer":
        pipeline = " -> ".join(entry.get("pipeline", []))
        raise SystemExit(f"profile {profile_id!r} uses a different pipeline: {pipeline}")
    profile_path = ROOT / "text-layouts" / entry["layout_profile"]
    return profile_path, load_layout(profile_path)


def wrap_characters(draw, text, font, max_width):
    lines = []
    line = ""
    for character in text:
        candidate = line + character
        if line and draw.textbbox((0, 0), candidate, font=font)[2] > max_width:
            lines.append(line)
            line = character
        else:
            line = candidate
    if line or not text:
        lines.append(line)
    return lines


def wrap_text(draw, text, font, max_width, prefer_semantic_breaks=False):
    lines = []
    for paragraph in text.splitlines() or [""]:
        if not prefer_semantic_breaks:
            lines.extend(wrap_characters(draw, paragraph, font, max_width))
            continue
        line = ""
        segments = re.findall(r"\S+\s*|[，。！？；：]+", paragraph)
        for segment in segments:
            candidate = line + segment
            segment_too_wide = draw.textbbox((0, 0), segment, font=font)[2] > max_width
            if line and draw.textbbox((0, 0), candidate, font=font)[2] > max_width:
                lines.append(line.rstrip())
                if segment_too_wide:
                    wrapped = wrap_characters(draw, segment, font, max_width)
                    lines.extend(wrapped[:-1])
                    line = wrapped[-1]
                else:
                    line = segment
            elif not line and segment_too_wide:
                wrapped = wrap_characters(draw, segment, font, max_width)
                lines.extend(wrapped[:-1])
                line = wrapped[-1]
            else:
                line = candidate
        if line or not paragraph:
            lines.append(line.rstrip())
    return lines


def resolve_lines(image, spec, text, scale, profile_path):
    draw = ImageDraw.Draw(image)
    font_path = str((profile_path.parent / spec["font"]).resolve())
    max_lines = spec.get("max_lines")
    min_font_size = spec.get("min_font_size", spec["font_size"])
    for source_size in range(spec["font_size"], min_font_size - 1, -1):
        font = ImageFont.truetype(font_path, round(source_size * scale))
        lines = wrap_text(
            draw,
            text,
            font,
            round(spec["max_width"] * scale),
            spec.get("prefer_semantic_breaks", False),
        )
        if not max_lines or len(lines) <= max_lines:
            break
    else:
        raise SystemExit(f"text needs more than {max_lines} lines at the profile minimum font size")
    return font, lines


def render_lines(image, spec, font, lines, scale, y_override=None):
    draw = ImageDraw.Draw(image)
    x = round((spec["x"] + spec.get("x_offset", 0)) * scale)
    base_y = spec["y"] + spec.get("y_offset", 0) if y_override is None else y_override
    y = round(base_y * scale)
    line_height = round(spec["line_height"] * scale)
    visible_boxes = []
    for index, line in enumerate(lines):
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        visible_y = y + index * line_height
        draw.text((x - left, visible_y - top), line, font=font, fill=parse_color(spec["color"]))
        visible_boxes.append({"x": x, "y": visible_y, "width": right - left, "height": bottom - top})
    return {"lines": lines, "fontSize": font.size, "color": spec["color"], "visibleBoxes": visible_boxes,
            "bottom": y + max(0, len(lines) - 1) * line_height + max((box["height"] for box in visible_boxes), default=0)}


def visible_block_height(image, font, lines, line_height):
    draw = ImageDraw.Draw(image)
    return max(
        (index * line_height + draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
         for index, line in enumerate(lines)),
        default=0,
    )


def resolve_centered_vertical_group(profile, image, title_font, title_lines, subtitle_font, subtitle_lines, scale):
    """Position a member logo/title/subtitle group by visible ink bounds."""
    group = profile.get("vertical_group")
    if not group:
        title_y = profile["title"]["y"] + profile["title"].get("y_offset", 0)
        subtitle_y = (title_y + len(title_lines) * profile["title"]["line_height"]
                      + profile["subtitle"]["title_gap"] + profile["subtitle"].get("y_offset", 0))
        return title_y, subtitle_y, None

    if group.get("alignment") != "vertical_center":
        raise SystemExit(f"unsupported vertical group alignment: {group.get('alignment')!r}")

    title_height = visible_block_height(
        image, title_font, title_lines, round(profile["title"]["line_height"] * scale)
    ) / scale
    subtitle_height = visible_block_height(
        image, subtitle_font, subtitle_lines, round(profile["subtitle"]["line_height"] * scale)
    ) / scale if subtitle_lines else 0
    subtitle_gap = profile["subtitle"]["title_gap"] if subtitle_lines else 0
    leading_height = group["brand_visible_height"] + group["brand_title_gap"]
    total_height = leading_height + title_height + subtitle_gap + subtitle_height
    group_top = group["center_y"] - total_height / 2
    title_y = group_top + leading_height
    subtitle_y = title_y + title_height + subtitle_gap
    group_trace = {
        "alignment": group["alignment"],
        "centerY": group["center_y"],
        "top": group_top,
        "bottom": group_top + total_height,
        "brandVisibleHeight": group["brand_visible_height"],
        "brandTitleGap": group["brand_title_gap"],
    }
    return title_y, subtitle_y, group_trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-image", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--profile", required=True, help="Profile ID from assets/text-layouts/registry.json.")
    parser.add_argument("--trace-output", help="Optional JSON trace for a following renderer.")
    args = parser.parse_args()

    profile_path, profile = load_profile(args.profile)
    image = Image.open(args.base_image).convert("RGBA")
    scale = image.width / profile["reference_width"]

    title_font, title_lines = resolve_lines(image, profile["title"], args.title, scale, profile_path)
    subtitle_font, subtitle_lines = resolve_lines(image, profile["subtitle"], args.subtitle, scale, profile_path)
    title_y, subtitle_y, group_trace = resolve_centered_vertical_group(
        profile, image, title_font, title_lines, subtitle_font, subtitle_lines, scale
    )
    title = render_lines(image, profile["title"], title_font, title_lines, scale, title_y)
    subtitle = render_lines(image, profile["subtitle"], subtitle_font, subtitle_lines, scale, subtitle_y)

    output = Path(args.output).with_suffix(".png")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG")
    trace = {"png": str(output), "profile": str(profile_path), "scale": scale,
             "title": title, "subtitle": subtitle, "verticalGroup": group_trace}
    if args.trace_output:
        trace_output = Path(args.trace_output).with_suffix(".json")
        trace_output.parent.mkdir(parents=True, exist_ok=True)
        trace_output.write_text(json.dumps(trace, ensure_ascii=False, indent=2))
        trace["traceOutput"] = str(trace_output)
    print(json.dumps(trace, ensure_ascii=False))


if __name__ == "__main__":
    main()
