# Field Taxonomy v0.1

## Stable ID Rule

Use stable English IDs for table joins. Chinese names can change; IDs should not.

Examples:

```text
business_line_id = biz_consumer_electronics
marketing_type_id = m_flash_sale
format_id = fmt_square_1_1
composition_id = comp_card_grid
background_recipe_id = bg_light_tech_product_space
```

## Core Layers

| Layer | Main CSV | Purpose |
|-|-|-|
| input | `00_fields.csv` | Define human-provided, inferred, and triggered fields. |
| business | `01_business_lines.csv` | Business boundaries, base visual tone, visual priority, and default risk rules. |
| category | `02_product_categories.csv`, `03_business_category_map.csv` | Product entities, visual traits, and business-role cues. |
| marketing | `04_marketing_types.csv` | Infer reusable marketing intent and information structure from title/subtitle. |
| format | `05_format_layouts.csv` | Ratio, reading flow, composition tendency, and safe area. |
| game visual asset | `00_fields.csv`, `references/agent-workflow.md` | Infer game-related asset role before product relation and visual routing. |
| visual preset path | `00_fields.csv`, `13_visual_preset_paths.csv`, `references/agent-workflow.md` | Optional user-facing B/A/S preset. Maps a business line + category + preset level into internal route factors, preferred background IDs, and a short route summary. Concrete visual language stays in background, product combination, and composition tables. |
| membership composition | `references/membership-head-composition.md`, `references/prompt-assembly.md`, `assets/membership-head-template/` | A member-day 2:1 route: image-to-image base plus fixed code-drawn composition. S resolves its node background and product relation independently, then uses `membership-s-2x1` to render the MasterGo text group with background-adaptive logo/text color. B 2:1 uses `membership-b-2x1` to locally draw its title group, then lets the membership renderer add the alpha-tinted member mark from the local-title trace. |
| consumer electronics A/S combination direction | `08_product_combinations.csv`, `references/agent-workflow.md` | Consumer-electronics-only internal route used after A/S preset matching. A resolves to one A-level combination direction; S resolves to one S-level combination direction, so the final prompt uses one concrete scene or topic direction. |
| visual expression mode | `00_fields.csv`, `references/agent-workflow.md` | Optional high-level routing preference for stable support vs scene expression; influences combination, composition, and background. |
| people participation | `00_fields.csv`, `references/agent-workflow.md` | Optional product presentation switch for whether people, hands, wearing, operation, or user interaction become part of the product combination; when set to yes, people visibly use the user-provided product. |
| composition | `06_composition_camera.csv` | Camera, perspective, motion, and layout energy. |
| product relation | `07_product_relations.csv` | Who is primary or secondary, plus hierarchy rule. |
| product combination | `08_product_combinations.csv` | How products are organized visually, plus arrangement and positive display language. |
| background | `09_background_recipes.csv` | Background recipe with context cue, positive visual language, and continuity rules. |
| fragments | `11_prompt_fragments.csv` | Reusable positive prompt and QA fragments. |
| negative rules | `12_negative_rules.csv` | Centralized prohibitions resolved from `negative_rule_ids`. |
| generation | `references/generation-execution.md` | Decide whether to generate image or output prompt only. |

## Inference Relationship

Do not classify by one field only. Use linked inference:

```text
business_line_id
+ base_visual_tone and visual_priority
+ marketing_type_id inferred from title/subtitle
+ product count/category from image
+ game_visual_asset_type when N-category game character assets are present
+ visual_preset_level when provided or inferred
+ visual_expression_mode from user or automatic inference
+ people_participation from user or automatic inference
+ format_layout
=> product_relation_id
=> product_combination_id
=> composition_id
=> background_recipe_id
=> inherited and modulated visual language
=> positive product and background visual language
=> negative_rule_ids
=> compressed essential constraints
=> final prompt
=> card-style review Markdown traces
=> image generation when requested or implied
```

## Product Relation vs Product Combination

| Field | Answers | Examples |
|-|-|-|
| product_relation | Who is primary, secondary, or grouped? | single hero, primary with support, multi collection, ranked list |
| product_combination | How are products arranged or grouped? | single hero, subject card carrier, product cards, cross-category, scene display |

Both are needed. Relation controls hierarchy; combination controls visual organization.

Do not split arrangement into a separate table in v0.1. Use `hierarchy_rule` from product relations and `arrangement_principle` / `positive_visual_language` from product combinations.

## Game Visual Asset Type

`game_visual_asset_type` is an inferred routing field used only after game-related uploads resolve to `biz_n_category + cat_game`. This route covers game character / role illustration assets, not card coupons or physical game devices.

Boundary rules:

- Game character or role illustration assets belong to `biz_n_category + cat_game`.
- Membership recharge, game point cards, coupon cards, benefit cards, and virtual rights belong to `biz_n_category + cat_card_coupon`.
- Switch, PS5, controllers, consoles, handhelds, and other physical game devices belong to `biz_consumer_electronics + cat_game_device`.
- Mixed game assets are reserved for future multi-category routing; use general routing or ask when the business meaning is unclear.

| Value | Chinese Meaning | Routing Use |
|-|-|-|
| `game_character_visual` | 游戏人物 / 角色立绘 | Treat as poster main visual; route to scene display or single hero with game background. |
| `game_multi_character_visual` | 多张游戏人物 / 多角色立绘 | Treat as a role-group visual; route to primary-support relation, scene display, and scene-immersive composition with game background. |

## Product Category vs Business Category Map

`02_product_categories.csv` defines what the product is and its stable visible traits. It should stay reusable across business lines.

`03_business_category_map.csv` defines the product's business role under a selected business line. It should describe business meaning, risk cues, and usage context, not become a visual style table.

For the same product, sale vs recycle meaning is mainly determined by business line, title/subtitle, marketing type, and background/service atmosphere. Do not rely on `03_business_category_map.csv` alone to decide the full visual style.

## Marketing Type

`04_marketing_types.csv` is the reusable intent table. It maps title/subtitle cues to marketing purpose, information structure, and default candidate IDs.

## Visual Preset Path

`13_visual_preset_paths.csv` is a user-facing shortcut layer for tested B/A/S routes. It should not duplicate product combination, composition, background, negative rule, or QA logic.

Rows with an exact `category_id` apply to that category first. Rows with `category_id=cat_all` are business-line general preset routes used only when no exact category preset exists.

`inherits_preset_id` is optional. When populated, inherit only the referenced visual route; retain the current row's business meaning and safety rules. It prevents membership B from duplicating the recycle B path while keeping membership separate from recycle semantics.

Use it to record:

- route factors: visual expression mode, style modifier, and people participation
- key expected result: preferred background IDs and a short visual expectation

Do not lock product combination or composition unless a future tested preset truly requires it. Product combination and composition should still be inferred from image count, product relation, output format, title semantics, and the selected route factors.

For `biz_consumer_electronics / 消费电子`, A/S preset rows are parent routes only. After matching A or S, resolve exactly one consumer-electronics combination direction from `08_product_combinations.csv`:

- A -> `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式` or `combo_ce_partial_people_use / 消费电子人物局部使用`
- S -> `combo_ce_miniature_theme / 消费电子微缩主题场景` or `combo_ce_surreal_product_scene / 消费电子超现实商品场景`

The selected combination ID and Chinese name must be recorded in review Markdown and must become the primary language of the final prompt.

## Visual Tone vs Visual Carrier

Do not treat background as the source of overall style. Use this hierarchy:

```text
business line = base visual tone
category = semantic context
marketing type = conversion strength and information density
visual expression mode = stable support vs scene expression routing
product relation = hierarchy
product combination = arrangement
composition = energy and camera
background = carrier and continuity
```

This prevents conflicts such as consumer electronics defaulting to heavy neon just because a technology background is selected, or recycle becoming an ordinary sale poster because a benefit-card background is selected.
