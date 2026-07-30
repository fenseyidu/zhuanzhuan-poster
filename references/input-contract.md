# Input Contract v0.1

## Minimum Input

Use this contract as the default. Do not ask the user to fill advanced fields up front.

| Field | Required | Human Input Style | Agent Behavior |
|-|-|-|-|
| product_assets | yes, except membership A/S 2:1 | Uploaded image, local path, or product ID | Use the visible product as the product source. For membership A/S 2:1 heads, accept an empty value when the AI base has no supplied product assets. |
| label_text | no | Plain text or empty | Use only when explicitly provided. For 回收 2:1 layouts, render it as a top label above the main title with a light capsule outline style and the same text size as the subtitle; do not infer or auto-generate it. |
| main_title | yes | Plain text | Preserve as the poster's main title and infer marketing intent. For `会员` A/S, use the entire title in bundled `SourceHanSerifSC-Heavy.otf`; an A/S `补充要求` containing `特殊字` uses the bundled brush-title reference. For `会员` B, use the modern display-Heiti treatment. |
| subtitle | yes | Plain text or `无` | Preserve as subtitle when present and infer marketing intent. For `会员` B `2:1`, render it after image generation with the registered renderer and `assets/subtitle-typography.json`; for all other formats, submit it to the image model as part of the title group. A separately selected card/module carrier is exempt. |
| decorative_text | no | Plain text or empty | Use only as optional user-specified handwritten overlay text when provided; do not infer facts from it. Low-priority decorative microcopy may appear as atmosphere and is not treated as a fact. |
| visual_preset_level | no | `自动`, `B`, `A`, or `S` | Default user-facing visual route. When matched, expand through `13_visual_preset_paths.csv` into internal route factors, preferred background IDs, and a short route summary. Read concrete visual language from the selected background, product combination, and composition tables. |
| business_line | yes | `N 品类`, `消费电子`, `回收`, or `会员` | Infer only when obvious; otherwise ask. `会员` means 转转平台会员权益/会员日, never third-party recharge or coupon cards. |
| format_layout | yes | `1:1`, `4:3`, `16:9`, or `2:1` | Map to `fmt_square_1_1`, `fmt_landscape_4_3`, `fmt_landscape_16_9`, or `fmt_landscape_2_1`. |
| supplement | no | Natural language | Use for preferences, constraints, and context. |

For `会员` A/S 2:1 member-day heads, render `main_title` as a separate transparent title PNG: use the bundled `SourceHanSerifSC-Heavy.otf` by default, and use the bundled brush-title reference only when `补充要求` explicitly contains `特殊字`. Treat `subtitle` as the date/standard-font copy composited after generation through the global subtitle typography policy. The fixed member-day mark, rule text, rule-button background, and bottom wave are compositor layers. `会员` B does not use this A/S composition route. For `会员` B 2:1, follow recycle B before rendering: generate a poster base without only the main title and subtitle, preserving all source-product text and screen content. Run `text_layout_renderer.py --profile membership-b-2x1 --trace-output <title-layout.json>`, then run `membership_head_renderer.py --mode membership-b --title-layout <title-layout.json>` to add `member-b-brand.png` above the local title.

For membership A/S 2:1 heads, accept at most four `product_assets`. No product assets use the direct default foreground of gift boxes, ribbons, and coins. One visibly gift-box asset replaces that default gift foreground. Other 1-4 product assets use the fixed slots, size, angle, layering, partial-upload behavior, and automatic slot assignment in `assets/membership-head-template/template.json` under `product_slots`. The lower foreground stays in the region from 70% canvas height to the bottom edge; only the ordinary-product slot branch uses the inside-box close-up and its 75%-width gift-box target. Assign products by the visible silhouette of the cut-out subject rather than the source image canvas: portrait products preferentially occupy the center main slot, flat products occupy the two side slots, and product hierarchy resolves otherwise similar candidates. An explicit user mapping overrides this automatic assignment; upload order is only a tiebreak. The approved member-day reference is the edit target. In the ordinary-product branch, the lower part of a product may be hidden by foreground coins and extend outside the canvas according to size, recognizability, and lower visual hierarchy; smaller products may be fully visible. When 1-3 ordinary products are supplied, retain the small toy and coins; unused product slots remain empty. When four products are supplied, all four product slots are replaced. When more than four assets are supplied, do not generate and ask the user to keep at most four products.

Advanced test briefs may also include:

| Field | Human Input Style | Agent Behavior |
|-|-|-|
| visual_expression_mode | `自动`, `稳定承托`, or `场景表达` | Advanced test/internal route field. If explicitly provided, it overrides the visual preset's `visual_expression_mode`. |
| people_participation | `自动`, `否`, or `是` | Advanced test/internal route field. If explicitly provided, it overrides the visual preset's `people_participation`, except when a forced no-people rule applies: matched `B` preset routes and multi-asset / multi-subject merchandise structures still resolve to `否 / 无人物陈列`. |

## Product Images

The user may drag product images directly into the chat input. Treat attached images as product assets.

If the user only provides images, do not require detailed product data. Infer only what is visually safe:

- approximate category
- product count
- whether there is an obvious hero product
- whether products are same-category or cross-category
- whether the image suggests sale, recycle, service, or lifestyle use

Treat these as triggered fact fields, not visual inference:

- brand or exact model
- price, coupon, subsidy, ranking, or inventory
- official certification or service commitment
- whether a product is new, used, authentic, or repaired

## Triggered Fact Confirmation

Ask for confirmation only when the requested visible copy or claim contains factual risk.

Trigger confirmation for:

| Trigger | Examples | Required Source |
|-|-|-|
| price | `99 元`, `立省 500`, `补贴 20%` | user or product/task data |
| ranking | `TOP1`, `热销榜`, `销量第一` | user or business data |
| model | `iPhone 15`, exact SKU, chip, storage | user or product data |
| time | `今日`, `限时 2 小时`, activity dates | user or task data |
| service promise | `上门`, `极速打款`, `官方验`, `包邮` | user or business rule |
| bundle | `买 A 送 B`, `套装`, `组合包` | user or task data |

If these do not appear, do not ask for them.

When a triggered fact is present, include the matching negative rule IDs from `12_negative_rules.csv`:

- `neg_no_unprovided_facts`
- `neg_ranking_requires_source`
- `neg_bundle_requires_source`
- `neg_service_claims_source`

## Optional Human Preferences

Accept these as natural language, but do not require them:

- background preference: clean, outdoor, premium, promotional, card-based
- label text: optional top label, only shown when explicitly provided; especially for 回收 2:1 title groups, keep a light capsule outline style and use the same text size as the subtitle
- product arrangement: single hero, subject card carrier, product cards, cross-category, scene display
- visual preset level: automatic, B, A, or S
- advanced test visual expression mode: automatic, stable product support, or scene expression
- advanced test people participation: automatic, no people, or people using product
- tone: stronger marketing, cleaner, more professional, more lifestyle
- decorative text: seasonal word, handwritten English word, or free overlay signature-style word; low-priority decorative microcopy may appear as atmosphere when it is not a business claim or factual message
- reference image ID or style direction
- forbidden content

When optional fields are absent, infer from the main title, subtitle, business line, marketing type, product images, and format. If `visual_preset_level`, `visual_expression_mode`, or `people_participation` is absent, default to `自动`. Explicit advanced test fields override a matched visual preset; the visual preset overrides automatic inference. Apply forced no-people overrides after this initial routing: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, resolves `people_participation` to `否 / 无人物陈列`.
