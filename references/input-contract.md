# Input Contract v0.1

## Minimum Input

Use this contract as the default. Do not ask the user to fill advanced fields up front.

| Field | Required | Human Input Style | Agent Behavior |
|-|-|-|-|
| product_assets | yes | Uploaded image, local path, or product ID | Use the visible product as the product source. |
| label_text | no | Plain text or empty | Use only when explicitly provided. For 回收 2:1 layouts, render it as a top label above the main title with a light capsule outline style and the same text size as the subtitle; do not infer or auto-generate it. |
| main_title | yes | Plain text | Preserve as the poster's main title and infer marketing intent. |
| subtitle | yes | Plain text or `无` | Preserve as subtitle when present and infer marketing intent. |
| decorative_text | no | Plain text or empty | Use only as optional user-specified handwritten overlay text when provided; do not infer facts from it. Low-priority decorative microcopy may appear as atmosphere and is not treated as a fact. |
| visual_preset_level | no | `自动`, `B`, `A`, or `S` | Default user-facing visual route. When matched, expand through `13_visual_preset_paths.csv` into internal route factors, preferred background IDs, and a short route summary. Read concrete visual language from the selected background, product combination, and composition tables. |
| business_line | yes | `N 品类`, `消费电子`, or `回收` | Infer only when obvious; otherwise ask. |
| format_layout | yes | `1:1`, `4:3`, `16:9`, or `2:1` | Map to `fmt_square_1_1`, `fmt_landscape_4_3`, `fmt_landscape_16_9`, or `fmt_landscape_2_1`. |
| supplement | no | Natural language | Use for preferences, constraints, and context. |

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
