# 会员日 2:1 合成

Use this only for `biz_membership` A/S 2:1 heads. It never applies to `会员` B.

## Layer Contract

The AI base is `2250x1125` and contains only the brush main title, lower foreground, coins, and continuous premium material background. Use image-to-image from the approved member-day reference to preserve the coupled title-and-lower-subject composition. In both initial generation and targeted regeneration, define the brush title as vertically centered in the canvas: its visual center aligns to height 45% (allowed range 43%–47%) while remaining inside the reference title box. Before any fixed-layer composition, read `template.json.layout_coupling` and run its joint preflight: title position/size/baseline/single-line shape/vertical center and the lower product-and-coin group must pass together. In the initial generation, constrain the product-and-coin main visual to the bottom 30% of the canvas (`y=788` to `1125`); no product subject may have a visible point above `y=806` (about 72% height, matching the highest product slot). This reserves the upper area for the member-day mark, brush title, and date, and it must leave the fixed-layer zones clean. If either title or foreground fails, treat the whole main visual as a single layout failure; do not compose fixed layers or repair the two regions independently.

Without supplied product assets, the lower foreground defaults to generic gift boxes, ribbons, and coins. With supplied product assets, use `template.json` 的 `product_slots` as the single source of truth. Assign assets using `slot_assignment`: an explicit user mapping wins; otherwise classify the cut-out subject silhouette and product hierarchy, with portrait products preferentially entering the center main slot and flat products preferentially entering the two side slots. Upload order only resolves a tie. Each assigned product is a local image-to-image replacement for its matching slot and inherits the reference subject's size, center, angle, layer order, and lighting relationship. The lower group follows the reference's staggered, layered arrangement, not a complete front-facing lineup. In the reference, the phone appears half exposed because its lower part is submerged behind foreground coins and continues outside the canvas; this explains the mother-layout treatment and does not impose a fixed crop ratio. Decide whether a replacement needs partial bottom-edge emergence from its size, recognizability, and the lower visual hierarchy; smaller products may remain fully visible. If partial emergence is used, hide the transition naturally behind foreground coins rather than leaving a hard crop. Keep each slot's own visible focus; coins remain. With 1-3 assets, retain the small toy and coins; unused product slots remain empty. With four assets, replace all four slots. Do not accept more than four assets: ask the user to reduce the selection before generation.

Use the MasterGo source `195067020342135 / 119:1428` as the only layout source. Its logical coordinates are doubled for the 2250x1125 output: top member-day mark `(722,212,806,102)`, brush-title reference box `(246,412,1760,324)`, date `(842,656,568,98)`, lower foreground reference box `(484,832,1284,294)`, rule button `(2148,376,102,170)`, rule text `(2172,390,66,140)`, and bottom wave `(0,1036,2250,89)`.

| Layer | Source | Color behavior |
|-|-|-|
| member-day mark | `member-day-brand-mask.png` | fixed shape; renderer derives its color from the AI base |
| date subtitle | renderer text | renderer uses the same derived color as the member-day mark |
| rule text | renderer text | choose light text for a dark button; choose dark text for a light button |
| rule-button background | renderer left-rounded, right-square rectangle | derive a readable shade from the local AI background; its right edge is flush with the canvas |
| bottom wave | renderer curve | derive a harmonious fill from the lower AI background |

Do not use the red review boxes from the reference as production elements.

## Required Source Asset

Use the saved MasterGo `member-day-brand-mask.png` by default. The renderer uses only its alpha channel, then applies a color that contrasts with the AI base. It is not reconstructed from a screenshot. Replace it only with an approved export when the source mark shape changes.

## Renderer

```text
python3 assets/membership-head-template/membership_head_renderer.py \
  --base-image <ai-base.png> \
  --date-text <date-copy> \
  --output <final.png>
```

Use `--brand-color #RRGGBB` only when a campaign needs an approved explicit mark/date color; otherwise let the renderer derive it from the AI base.

## QA

- Before every A/S composition, without exception, run the `layout_coupling` joint preflight. The title's visible ink follows the reference title box and does not collide with the future brand/date reservations; the lower foreground is within the required region, and no product exceeds the required top boundary. Any failure blocks composition and uses one joint-layout correction on the current AI base.
- The AI base has no duplicate fixed mark, date, rule badge, rule text, or bottom wave.
- The brush main title and lower foreground keep the reference composition while allowing local product replacement.
- Each replacement inherits its slot's size, center, angle, layer order, lighting relationship, and visible focus. The product group must retain its staggered, overlapping three-quarter arrangement; no front-facing parallel arrangement or equal-ratio half crop. A bottom-edge emergence/crop is optional, based on the replacement's size, recognizability, and the lower visual hierarchy; when used, foreground coins must naturally conceal the cropped/extended lower portion. Smaller products may be fully visible. For 1-3 supplied products, the lower foreground contains the supplied products, the retained small toy, and coins; for four, it contains the four supplied products and coins.
- Rule text remains readable: dark button -> light text; light button -> dark text.
- The rule button has rounded left corners and square right corners, with its right edge flush to the canvas.
- The bottom wave separates from, but harmonizes with, the generated lower background.
- After composition, the brand, date, rule button, and bottom wave are readable and do not visibly collide with the brush title or lower foreground. A collision is `合成碰撞失败`, not a PASS.
