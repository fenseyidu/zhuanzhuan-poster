# 会员日 2:1 合成

Use this only for `biz_membership` A/S 2:1 heads. It never applies to `会员` B.

## MasterGo Source Assets

The only layout source is `195067020342135 / 119:1428`. The required exports are now saved with the template:

| MasterGo layer | Saved asset | Purpose |
|---|---|---|
| `bg` / `119:0943` | `source/member-day-background-master.png` | title-free warm-gold background and lower-foreground composition reference for the AI base |
| `Clipboard_Screenshot_1785289995` / `126:1588` | `member-day-title-style-reference.png` | title-only brush-lettering style reference; it is an RGBA image, not an editable font |
| `Clipboard_Screenshot_1785134069` / `119:1743` | `member-day-brand-mask.png` | fixed member-day mark alpha mask |

The source title reference reads `狂欢开启 惊喜到周末`. It is never copied into a task with a different main title. It is used only as the style reference for a dedicated title-only generation.

## Layer Contract

The final canvas is `2250x1125` and has three stages:

1. **AI base** — warm-gold material background, lower product group, coins, small toy, perspective, lighting, and shadows. The title area is clean and contains no readable title, member-day mark, date, rule control, or bottom wave.
2. **Title-only asset** — a title-specific image-generation result, delivered as a transparent PNG with only the approved brush title. The compositor places it into `template.json.title_layer.box` and derives a deep warm-gold tint from the AI base unless an explicit approved color is supplied.
3. **Fixed layers** — member-day mark, date, rule button/text, and bottom wave, drawn by the compositor.

Do not generate a title-and-product base and then erase the title. The MasterGo `bg` export is the title-free edit target/reference from the outset.

The lower product-and-coin visual stays in the bottom 30% (`y=788` to `1125`); no product subject may have a visible point above `y=806`. MasterGo `119:1428` provides the original title box at `(244,380,1760,324)`; the active local template uses title `y=350` with a fixed visible height of `280`, while retaining the member-day mark at `(722,232,806,102)` and date box at `(842,670,568,98)`. Its visible ink must stay clear of the future member-day mark and date reservations.

The product slots, assignment rules, partial bottom emergence, coins, and small-toy handling in `template.json.product_slots` remain unchanged. With 1–3 supplied products retain the small toy and coins; with four products replace all four slots; stop and ask the user to reduce any selection over four products.

## Title-only Generation Contract

For a changing title, pass the saved `member-day-title-style-reference.png` as a reference-image text-replacement target and generate the exact user-provided main-title text in a separate title-only task. For the bundled default reference, use `将图中的“狂欢开启 惊喜到周末”改为“{main_title}”`; do not describe the brush style independently. The desired output is one readable horizontal line, contains no other copy or objects, and has a transparent background after chroma-key removal. The exact text and brush treatment remain subject to title QA; the reference is not a font and cannot guarantee a literal stroke-for-stroke copy.

For a fixed campaign title, skip title generation and use the approved transparent title PNG directly. Never use the style-reference PNG itself as a replacement title unless its visible words exactly equal the requested main title.

## Title Asset Placement

The renderer must use the title PNG's alpha channel only. First crop to its non-transparent alpha bounds, then set its visible height exactly to `title_layer.visible_height`; derive its width proportionally from its visible alpha bounds and center it. The current approved default is `visible_height=280` and `title_layer.box.y=350`. Do not resize the complete source canvas directly to the title box or force a title to fill the fixed width: title-only images often contain unequal transparent padding, and non-uniform source-to-box scaling visibly compresses or widens brush strokes. Reject an asset with no visible alpha content.

## Renderer

```text
python3 assets/membership-head-template/membership_head_renderer.py \
  --base-image <ai-base-without-title.png> \
  --title-asset <approved-title-only.png> \
  --date-text <date-copy> \
  --output <final.png>
```

Use `--title-color #RRGGBB` only for an approved campaign color. Use `--brand-color #RRGGBB` only when the member-day mark/date also need an approved explicit color; otherwise both colors are derived from their local AI-base areas.

## QA

Before composition, run two independent checks:

- **AI-base product check:** the base contains no readable title or fixed layers; lower products, coins, slots, overlap, and top boundary satisfy `template.json.product_slots` and `foreground_visible_top_max_y`.
- **Title-asset check:** title text exactly matches the user copy, the PNG has usable transparency, the brush style is approved, its visible alpha is proportionally scaled (same horizontal and vertical scale), and its content fits `title_layer.box` without colliding with the mark/date reservations.

Then run one final composition check: title, lower product group, member-day mark, date, rule button/text, and bottom wave are readable, harmonious, and non-overlapping. A title-only failure retries the title asset; a product-layout failure retries only the current AI base. A final collision is `合成碰撞失败`.
