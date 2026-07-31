# 会员日 2:1 合成

Use this only for `biz_membership` A/S 2:1 heads. It never applies to `会员` B.

## MasterGo Source Assets

The only layout source is `195067020342135 / 119:1428`. The required exports are now saved with the template:

| MasterGo layer | Saved asset | Purpose |
|---|---|---|
| `bg` / `119:0943` | `source/member-day-background-master.png` | title-free warm-gold background and lower-foreground composition reference for the AI base |
| `Clipboard_Screenshot_1785289995` / `126:1588` | `member-day-title-style-reference.png` | title-only brush-lettering style reference; use only when 补充要求 contains `特殊字`; it is an RGBA image, not an editable font |
| `SourceHanSerifSC-Heavy.otf` | `fonts/SourceHanSerifSC-Heavy.otf` | default font for the entire main title |
| `Clipboard_Screenshot_1785134069` / `119:1743` | `member-day-brand-mask.png` | fixed member-day mark alpha mask |

The source title reference reads `狂欢开启 惊喜到周末`. It is never copied into a task with a different main title. Use it only as the style reference for a dedicated title-only generation when `补充要求` contains `特殊字`. For this special-title route, crop to the visible alpha and scale it to exactly 268px visible height on the 2250px output canvas; do not impose a width limit.

## Layer Contract

The final canvas is `2250x1125` and has three stages:

1. **AI base** — warm-gold material background, lower foreground, coins, perspective, lighting, and shadows. No-product and single-gift-box runs use the direct gift foreground; ordinary-product runs use the inside-box slot foreground. The title area is clean and contains no readable title, member-day mark, date, rule control, or bottom wave.
2. **Title-only asset** — a transparent PNG with only the main title: render it from `SourceHanSerifSC-Heavy.otf` by default, or generate the approved brush title from the reference image only when `补充要求` contains `特殊字`. Unless the user explicitly requests another color, the compositor places it into `template.json.title_layer.box` in the bundled MasterGo reference color `#7E4504`.
3. **Fixed layers** — member-day mark, date, rule button/text, and bottom wave, drawn by the compositor.

Do not generate a title-and-foreground base and then erase the title. The MasterGo `bg` export is the title-free edit target/reference from the outset.

The lower foreground stays in the bottom 30% (`y=788` to `1125`). Only the ordinary-product slot foreground uses the inside-box close-up and the 75%-width gift-box opening and low-side-corner target; this is a soft initial-composition target, not a fixed dimension for local edits. The active local template owns title geometry: at 1125px reference width, A/S uses a 110px title size with 908px maximum visible width. A one-line title that exceeds 908px stays on one line and proportionally reduces its font size before composition. On the 2250px output canvas, the title box is `(217,360,1816,324)` and the composited title group fits within a 220px visible-height limit; its visible ink must stay clear of the future member-day mark and date reservations.

The product slots, assignment rules, partial bottom emergence, coins, and small-toy handling in `template.json.product_slots` apply only to ordinary products. With 1–3 ordinary products retain the small toy and coins; with four products replace all four slots; stop and ask the user to reduce any selection over four products.

## Title-only Generation Contract

By default, render the exact user-provided main title with `title_asset_renderer.py` and `fonts/SourceHanSerifSC-Heavy.otf` as a separate transparent title PNG. It uses the route-owned 110px / 908px policy at 1125px reference width and keeps it as one line, reducing the font size proportionally only when its one-line visible width exceeds 908px. Only when `补充要求` contains `特殊字`, pass the saved `member-day-title-style-reference.png` as a reference-image text-replacement target and generate the exact user-provided main-title text; for the bundled reference, use `将图中的“狂欢开启 惊喜到周末”改为“{main_title}”` and do not describe the brush style independently. The desired output contains no other copy or objects and has a transparent background after chroma-key removal. The exact text and selected title treatment remain subject to title QA; the brush reference is not a font and cannot guarantee a literal stroke-for-stroke copy.

For a fixed campaign title, skip title generation and use the approved transparent title PNG directly. Never use the style-reference PNG itself as a replacement title unless its visible words exactly equal the requested main title.

## Title Asset Placement

The renderer must use the title PNG's alpha channel only. First crop to its non-transparent alpha bounds, then set its visible height exactly to `title_layer.visible_height`; derive its width proportionally from its visible alpha bounds and center it. Reject a default title asset whose visible width exceeds `title_layer.max_visible_width`. When `补充要求` contains `特殊字`, pass `--special-title`: its visible alpha is scaled to the fixed 268px height and is not width-limited. Do not resize the complete source canvas directly to the title box or force a title to fill the fixed width: title-only images often contain unequal transparent padding, and non-uniform source-to-box scaling visibly compresses or widens brush strokes. Reject an asset with no visible alpha content.

## Renderer

The renderer accepts any AI-base canvas size. Before placing fixed layers, it uses cover scaling and crops the base to the 2250×1125 template: horizontal crops are centered, while vertical crops are bottom-anchored so the lower gift/product foreground is retained. A first-generation aspect-ratio mismatch alone must not trigger another AI generation; continue to composition and judge the final layout normally.

```text
python3 assets/membership-head-template/membership_head_renderer.py \
  --base-image <ai-base-without-title.png> \
  --title-asset <approved-title-only.png> \
  --date-text <date-copy> \
  --output <final.png>
```

When `补充要求` contains `特殊字`, add `--special-title` to that command. This route scales the cropped alpha to exactly 268px visible height and does not apply a maximum-width limit.

Use `--title-color #RRGGBB` only for an explicitly requested title color. Use `--brand-color #RRGGBB` only when the member-day mark/date also need an explicitly requested color. Otherwise, the compositor renders the title, member-day mark, and date in the bundled MasterGo reference color `#7E4504`; it does not auto-switch these colors by local contrast. Every text layer stays one pure color, never a gradient or segmented color.

## QA

Before composition, run two independent checks:

- **AI-base foreground check:** the base contains no readable title or fixed layers. If the input canvas was normalized, inspect the cropped base before accepting the final composition. For no-product and single-gift-box runs, check the direct gift foreground contains only the selected gift boxes, ribbons, and coins in the lower region, without an outer gift-box container. For ordinary-product runs, check the inside-box close-up, box rim behind the products, low side corners, ribbon, lower product group, in-box coins, slots, overlap, and top boundary satisfy `template.json.product_slots` and `foreground_visible_top_max_y`; on the initial AI base, also check the gift-box opening and low side corners are approximately 75% canvas width with breathing room on both sides.
- **Title-asset check:** title text exactly matches the user copy, the PNG has usable transparency, and its title style is `SourceHanSerifSC-Heavy.otf` by default or the brush reference only when `补充要求` contains `特殊字`; its visible alpha is proportionally scaled (same horizontal and vertical scale), and its content fits `title_layer.box` without colliding with the mark/date reservations. Unless the user explicitly requested a color override, check that title, member-day mark, and date each use the reference color `#7E4504`, with no gradient or segmented lettering.

Then run one final composition check: title, lower product group, member-day mark, date, rule button/text, and bottom wave are readable, harmonious, and non-overlapping. A title-only failure retries the title asset; a product-layout failure retries only the current AI base. A final collision is `合成碰撞失败`.
