# Agent Workflow v0.1

## Decision Order

Use the smallest human input, then expand through linked tables.

```text
product assets + main title + subtitle + optional decorative text + optional visual preset + optional advanced visual expression mode + optional advanced people participation + business line + format
-> read business_line base_visual_tone and visual_priority
-> infer marketing_type_id
-> infer category_id
-> resolve game-related asset boundary; infer game_visual_asset_type only for N-category game character assets
-> resolve visual_preset_level and read 13_visual_preset_paths.csv when matched
-> resolve visual_expression_mode as automatic, stable support, or scene expression
-> resolve initial people_participation as automatic, no people, or people using product
-> infer product count and product relation
-> choose product_combination_id
-> correct people_participation by product relation and product combination when needed
-> choose composition_id
-> choose background_recipe_id
-> if the selected background row defines candidate elements, count limits, or hard spatial/light rules, resolve one concrete background subset now and record it
-> build visual language by inheritance and modulation
-> assemble positive prompt fragments
-> collect negative_rule_ids
-> resolve negative_rule_ids through 12_negative_rules.csv
-> for `会员` B 2:1 only, resolve title-group subtitle through assets/subtitle-typography.json when it is non-empty and not a selected information module
-> compress essential constraints into final prompt
-> keep full traces in card-style review Markdown
```

## Marketing Type Inference

Use title, subtitle, and supplement first. Use business line and product category as tie-breakers.

Examples:

| User Wording | marketing_type_id |
|-|-|
| 秒杀、限时、抢购、低价、直降 | `m_flash_sale` |
| 补贴、券、加价、福利、立省 | `m_subsidy_benefit` |
| 好货、精选、值得买、推荐 | `m_good_goods` |
| 周末、出发、生活、场景、陪伴、种草 | `m_lifestyle_seeding` |
| 专业、性能、参数、器材、选购 | `m_professional_recommendation` |
| 回收、估价、质检、打款、上门、安心 | `m_service_trust` or `m_subsidy_benefit` |
| 新品、上新、首发、新款、换新 | `m_new_arrival` |
| TOP、排行、热销榜 | `m_sales_ranking` |

If multiple cues appear, choose the strongest conversion goal:

```text
ranking > explicit price/subsidy > recycle service > flash sale > new arrival > professional recommendation > good goods > lifestyle
```

## Visual Preset Path

`visual_preset_level` is the default user-facing shortcut for tested category routes. It does not replace the lower-level routing tables; it expands into internal route factors, preferred background IDs, and a short route summary.

Values:

| visual_preset_level | Meaning |
|-|-|
| `自动` | do not force a preset; infer through the normal workflow |
| `B` | tested stable/basic visual route for the matched category |
| `A` | tested content/topic route for the matched category |
| `S` | tested stronger topic route for the matched category |

Routing order:

1. If the user explicitly provides advanced test fields such as `视觉表达模式` or `人物参与`, use those values first.
2. Else, if `visual_preset_level` is `B`, `A`, or `S`, first match `business_line_id + category_id + preset_level` in `13_visual_preset_paths.csv`; if no exact category row exists, match `business_line_id + cat_all + preset_level` as the business-line general preset.
3. Expand the matched row into `visual_expression_mode`, `style_modifier`, `people_participation`, `preferred_background_ids`, and the short route summary in `expected_visual_result`.
   - If `inherits_preset_id` is present, first resolve the referenced row's route factors. The child may override only fields it explicitly supplies; blank child visual fields remain inherited. Keep the requesting business line's own business tone, prompt fragment, and negative rules. `biz_membership + B` therefore takes all visual fields from `vp_recycle_all_b`, while recycle service wording never enters a membership prompt.
4. After the initial `people_participation` value is known, apply forced no-people overrides: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, resolves to `人物参与=否 / 无人物陈列` even if the user explicitly provides `人物参与=是`.
5. If the matched preset is `biz_consumer_electronics / 消费电子` with preset `A` or `S`, resolve exactly one concrete combination direction from `08_product_combinations.csv` before final prompt assembly.
   If the matched preset is `biz_membership + cat_membership_day + S`, resolve `membership_theme` in this order: explicit `会员节点=圣诞|中秋`; otherwise an exact node cue in `主标题`; otherwise an exact node cue in `补充要求`. 圣诞 cues are `圣诞`、`平安夜`、`Christmas`、`Xmas`; 中秋 cues are `中秋`、`Mid-Autumn`。不从 `团圆`、`惊喜`、`礼赠` 等泛情绪词推断节点。没有明确节点词时，先请用户在圣诞和中秋中选择，再选背景。
6. Continue the original workflow: infer product relation, product combination, composition, and final background.
7. If no preset row matches, fall back to automatic inference.

Do not treat a preset row as a new style system or a complete visual prompt. It is a compact route record through the existing workflow; concrete visual language should come from the selected background recipe, product combination, and composition.

When a preset row has `preferred_background_ids`, use those IDs as high-priority background candidates after product relation, product combination, and composition are known. For `biz_consumer_electronics / 消费电子`, a matched B/A/S preset makes `preferred_background_ids` the allowed background set: choose `background_recipe_id` from that row unless the user supplement, explicit advanced test fields, or a safety conflict requires an override. Any override must be recorded in review Markdown with the selected background and the reason.

For the current v0.1 mapping, preset rows can be exact category rows or business-line general rows. Exact category rows have priority over `cat_all` rows. `biz_consumer_electronics` has exact B/A/S rows for phone, computer, tablet, camera, headphones, smart wearable, game device, home appliance, and general consumer-electronics activity; `biz_consumer_electronics + cat_all` stays as the fallback route for unknown or unmapped consumer-electronics categories.

`biz_recycle + cat_all` has B/A/S rows that all map to the same recycle B-level stable-support route. For recycle, do not create category-specific A/S scene or strong-topic behavior in v0.1. When the user provides B, A, or S for 回收, route through `bg_recycle_service_graphic / 回收_背景_弱中语境`, use `稳定承托`, `人物参与=否`, and treat the result as a simple, light-toned, trustworthy recycle poster with product-color inheritance and restrained information hierarchy. For this recycle background, the support surface is optional: use no platform/tabletop when possible, or at most one continuous tabletop/support surface; do not generate two or more separated podiums, round platforms, stone blocks, trays, or support blocks.

`biz_membership + cat_membership_day` has three distinct routes. B stays in the normal prompt pipeline but fully inherits the recycle B visual route: stable support, no people, `bg_recycle_service_graphic`, its no-platform-or-one-continuous-support-surface rule, and the recycle B product geometry. With two or more physical product assets, B resolves `rel_multi_recyclable` and `combo_multi_recyclable` as visual parent rules: two products have reasonable near-equal visual weight without a forced main/support hierarchy and form stagger through front/back, high/low, offset bottom edges, size, angle, light perspective, or slight overlap; three or more products may use one clearer main object. Only the visual geometry and QA constraints are inherited—final membership prompts and reviews must not use recycle-coverage, estimate, inspection, payment, service-trust, or other recycle service wording. A is a title-free membership 2:1 AI base plus code-composition route. The saved MasterGo `source/member-day-background-master.png` is the base reference. `combo_membership_day_visual` selects the lower foreground: no product or one visibly gift-box asset uses the direct gift foreground; other 1-4 product assets use the inside-box slot foreground. Create a separate title-only PNG from `fonts/SourceHanSerifSC-Heavy.otf` by default; only when `补充要求` contains `特殊字` does `member-day-title-style-reference.png` become a reference-image text replacement. The compositor and its fixed layers are defined in `membership-head-composition.md`. S is a separate node-theme route: resolve `membership_theme=圣诞|中秋`, choose the matching S background, use `combo_membership_seasonal_gift` with zero product assets, and otherwise resolve the normal product relation—single hero, primary/support, or multi collection—before selecting its reusable combination. For `membership_theme=圣诞`, use `source/membership-s-christmas-background-master.png` as the title-free image-to-image base: retain its complete “single star crown → continuous tapering particle-and-volume-light tree → gift/product group at the tree base” geometry, then alter only the selected product combination. It must not be reduced to generic Christmas decorations or deferred to Visual QA. S does not use A's background master, title asset, fixed slots, or fixed compositor. After its base passes visual QA, run `membership_s_renderer.py` with the `membership-s-2x1` profile and pass exact `title` and `subtitle` copy; the main title stays single-line and proportionally shrinks to fit the 580px reference text region, while the subtitle wraps/centers horizontally. Keep the full logo/title/subtitle group vertically centered. The node selection never supplies title text. The renderer uses the bundled alpha-mask logo and resolves a shared logo/text color from the background.

For `biz_membership + cat_membership_day + B + 2:1`, the generated poster base must omit only the main title and subtitle; source-product text, icons, and screen content remain. Then run `text_layout_renderer.py --profile membership-b-2x1`. The membership profile owns its title/subtitle specification and the member mark remains a local renderer layer.

Before writing the membership A final prompt for the ordinary-product branch, build `slot_replacement_map` from every active `product_slots` row: `reference_subject → actual_upload_order + visible_product_description`. Write every mapping explicitly into the final prompt in template slot order; a bare slot ID, an unordered product list, or a generic “按上传顺序替换” statement is insufficient. Default mapping follows `template.json.product_slots.slot_assignment`: determine the cut-out silhouette and hierarchy, place the best portrait product in the center main slot, and place flat products in the side slots. Use upload order only as a tiebreak; an explicit user mapping to a named `reference_subject` overrides it and must be recorded in review Markdown. Use only visually safe product descriptions and do not invent brand, model, price, or parameter facts.

Before A composition, independently check the title-free base and title PNG. A first AI base with a non-2:1 canvas goes directly through the renderer's cover-scale crop to the 2250×1125 template; aspect ratio alone never triggers AI regeneration. The crop is horizontally centered and vertically bottom-anchored to preserve the lower foreground. A remaining product-region, slot, crop, or overlap failure retries only the current AI base; a title-copy, selected-title-style, transparency, title-box, or mark/date-reservation failure retries only the title asset. Only the final composed image checks all layers together for collisions. This route does not apply to membership B or S.

`cat_collectible_toy` and `cat_game` under `biz_n_category` have confirmed B/A/S rows:

| preset | Tested route | Expected result |
|-|-|-|
| `B` | `稳定承托` + no strong flat/3D modifier + `人物参与=否` | stable collectible-toy product display |
| `A` | `场景表达` + 手帐纸艺平面 modifier + `人物参与=否` + 撕纸标题区、浅绿网格便签、顶部圆环夹、纸胶带、少量贴纸和虚线涂鸦 | journal-style paper-craft collectible-toy topic layout |
| `S` | `场景表达` + no strong flat/3D modifier + `人物参与=否` + fixed torn-paper edges | collectible-toy topic display with flat-background plus light 3D space |

Game preset rows are only for N-category game character and role illustration assets:

| preset | Tested route | Expected result |
|-|-|-|
| `B` | `稳定承托` + flat game modifier + `人物参与=否` | flat operation background plus game visual subject |
| `A` | `场景表达` + simple game scene modifier + `人物参与=否` | simple game background plus game main visual |
| `S` | `场景表达` + game topic modulation + `人物参与=否` | stronger game content atmosphere or role-group visual, still clean and readable |

Consumer electronics preset rows are parent routes. A/S must be resolved into one concrete consumer-electronics combination direction before final prompt assembly:

| preset | Tested route | Expected result |
|-|-|-|
| `B` | `稳定承托` + exact category + 极简产品发布感 + 主方向：主体清晰展示/功能局部特写/高级几何承托空间（选一并记录）；可融合另外1-2个辅助方向 + 浅色强对比/深色强对比（选一并记录） + 材质边缘高光 + 光影策略（选一并记录） + `人物参与=否` | minimal launch product display |
| `A` | `场景表达` + `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式` or `combo_ce_partial_people_use / 消费电子人物局部使用`（选一并记录） + 光影策略（选一并记录） + `人物参与=否/是随机` | consumer-electronics scene expression |
| `S` | `场景表达` + `combo_ce_miniature_theme / 消费电子微缩主题场景` or `combo_ce_surreal_product_scene / 消费电子超现实商品场景`（选一并记录） + 光影策略（选一并记录） + `人物参与=否` | consumer-electronics topic scene |

Consumer electronics A/S combination direction selection:

- Supplement words like 人物、佩戴、手持、操作、局部人物、不露脸、侧身、手部 route A toward `combo_ce_partial_people_use / 消费电子人物局部使用`.
- Supplement words like 摄影感、生活方式、窗边、通勤、办公、居家、沙滩、夏天 route A toward `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式`.
- Supplement words like 季节、开学、节日、旅行、小世界、小场景、微缩、机场、海滩、街道、草地、桌面城市、具体场景 route S toward `combo_ce_miniature_theme / 消费电子微缩主题场景`.
- Supplement words like 漂浮、悬浮、梦幻、超现实、未来、尺度错位、抽象自然、现实与虚构 route S toward `combo_ce_surreal_product_scene / 消费电子超现实商品场景`.
- If no supplement selects a direction, choose randomly inside the current preset's candidate combination directions and record the selected combination ID and Chinese name in review Markdown.
- The selected combination direction must become the primary scene or arrangement language in the final prompt. Do not leave A/S at the parent route only.

N-category billiards cue preset rows use this route structure:

| preset | Tested route | Expected result |
|-|-|-|
| `B` | `稳定承托` + `combo_billiards_cue_diagonal_texture / 台球杆斜向质感陈列` + 高级商品摄影 B 档 + 调用高级商品光影调制 + `人物参与=否` | advanced product photography cue display |
| `A` | `场景表达` + `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列` + `人物参与=否` + 生活兴趣场景 | interest-scene cue display |
| `S` | `场景表达` + `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列` + `人物参与=否` + surreal concept space carrier | surreal concept scene with cue-focused display |

N-category musical instrument preset direction selection:

- Only when `business_line_id=biz_n_category / N 品类` and `category_id=cat_musical_instrument / 乐器`, use the musical-instrument-specific B/A/S routing below.
- B-level resolves to `vp_n_music_b / 乐器材质空间窗光商品棚拍款`: use low-context musical-instrument scene expression with premium product lighting and one selected B-level background. Default to `bg_music_material_window_light / 乐器_材质空间窗光_弱中语境`. B-level stays on material space, product light, professional-instrument advertising presence, and low-context spatial evidence; it should not route into music-lifestyle corners, private collection traces, or home-like life-interest staging. B-level may keep only the fixed B/A micro-decoration finish layer near title breathing space, title vicinity, or main-visual edge, without expanding into editorial props or a lifestyle-corner carrier. Treat this B-level route as `场景表达` on a restrained material-space carrier rather than `稳定承托`. Treat the selected B-level row in `09_background_recipes.csv` as the only source of visible-element pool, light rules, and forbidden spillover; resolve and record one concrete `背景选用清单`, then carry only that selected subset into the final prompt and QA. Do not restate or expand the full candidate pool elsewhere.
- A-level resolves to `vp_n_music_a / 乐器音乐生活角落与清爽活动场景款`: default to `bg_music_editorial_paper_studio / 乐器_音乐生活方式角落_中语境`; do not require the user to provide trigger words such as 私人收藏、personal belongings、英文小装饰、纸感、印刷感、胶片感、浅色 or 深色 for this default route. Treat the selected row in `09_background_recipes.csv` as the only source of visible-element pool, fixed editorial decorations, quantity caps, optional plant-shadow handling, texture rules, and forbidden spillover. Write the result as a music-lifestyle corner rather than a plain lifestyle photo: private collection traces, low-presence personal belongings, one micro-English header group, one subtle handwritten note, and light texture must become actual final-prompt language. When the supplement or asset clearly introduces another scene, festival, season, space, activity, showcase, window-display, balcony, terrace, garden-music-corner, light-stage, brand-music-space, or similar environmental direction, switch A-level to `bg_music_fresh_event_lifestyle / 乐器_清爽音乐活动生活方式_中语境` and let that selected row own the space language; in this route, use 远景降细节、轻度平面化、杂志广告式调色 as the default scene-finishing logic, and keep 极轻的哑光纸张颗粒与轻印刷感 only as weak material modulation. This music-lifestyle corner route defaults to `无人物陈列`; only when the supplement or asset clearly requires a visible play/use relation may it switch to `人物使用关系`. Across both A directions, when people appear they should serve the use relation while the instrument remains the focus.
- S-level resolves to `vp_n_music_s / 乐器强主题主视觉款`: always use `夜场舞台氛围` and `bg_music_concert_surreal_scene / 乐器_演唱会超现实抽象场景_强语境` as the primary background carrier.
- Musical-instrument `S-level` routing priority:
  - explicit supplement has highest priority for night-stage flavor
  - otherwise infer the specific night-stage mood from title, subtitle, visible asset mood, and reference-image context
- Route musical-instrument `S-level` like this:
  - Supplement words such as 夜场、晚上、黑场、舞台、live、演出、开躁、燃、热爱、人群、灯束、烟雾 strengthen the selected `夜场舞台氛围` direction.
  - Supplement words such as 音乐节、festival、音约 default to and remain on `夜场舞台氛围`.
  - Even when the supplement includes 白天、白日、户外、露天、草地、蓝天、活动装置、路牌、打卡、年轻、明亮, musical-instrument `S-level` should not switch to a bright-display route; keep the scene on a night-stage carrier and absorb those cues only as secondary event-theming details when useful.
  - When no supplement is given, infer the specific `夜场舞台氛围` from dark stage, audience, light beams, smoke, strong event typography, or concert-screen references.
- In musical-instrument `S-level` `夜场舞台氛围`, low-presence audience silhouettes or crowd silhouettes are allowed and usually preferred even when `people_participation` resolves to `否 / 无人物陈列`, as long as they only serve concert scale and stage atmosphere. Treat these silhouettes as background atmosphere rather than `人物参与=是 / 人物使用关系`: keep them distant, low-detail, non-interactive, and never let them become performers using the uploaded instrument or replace the instrument as the main subject.
- Musical-instrument `S-level` defaults to a weak finish layer inherited from the safe part of the A-level activity route: very light matte paper grain, faint print texture, and 1-2 low-presence editorial micro-decoration groups. Keep them attached to corners, outer whitespace, or title breathing areas only; they must not rewrite the scene into a private music corner, and they must not introduce precise year/date/issue/season claims or other new facts.
- Musical-instrument `S-level` title typography defaults to the approved strong-theme stage-poster style validated by the reference sample: a modern display Heiti / title sans feel with upright structure, broad face, thick strokes, clean edges, slight width compression, and optional very light print-grain texture. Treat this as a typography-only reference: keep the title color independent from the sample and resolve color from the current scene contrast, product palette, and readability needs.
- Musical-instrument `S-level` main title should use only two colors in total: most characters stay in one main title color, and only one continuous keyword or phrase may use the accent color. Do not introduce a third emphasis color, and do not scatter accent color across multiple separated words.
- In 4:3, 16:9, or 2:1 musical-instrument `S-level` layouts, keep the title group inside the left reading area with visible left/right breathing space. Do not stretch the title group to fill the full text zone width, and do not enlarge short titles just to occupy more horizontal space.
- People are optional only when they support performance scale or stage atmosphere, but when multiple uploaded product assets or multi-subject merchandise structure are present, forced no-people override still applies before final prompt assembly.
- The selected musical-instrument scene direction, people participation, and lighting language must become actual final-prompt language, not just review labels.

N-category bicycle preset direction selection:

- Only when `business_line_id=biz_n_category / N 品类` and `category_id=cat_bicycle / 骑行`, use the bicycle-specific B/A/S routing below.
- B-level resolves to `骑行高级商品摄影棚拍款`: use strong-contrast advanced product photography, `bg_bicycle_contrast_colorblock_studio / 骑行强对比几何色块棚拍背景`, professional sports-equipment advertising lighting, and a large close bicycle advertising composition. Record one `骑行商品角度` from `cat_bicycle.visual_traits` and make that angle part of the camera/composition language; for side-view or three-quarter-front B-level routes, prioritize enlarged near front wheel, low-angle three-quarter-front view, and bicycle frame extending backward to create perspective pressure.
- B-level uses `高级商品光影调制` as the product-photography lighting skeleton, then expands it through `cat_bicycle.visual_traits`: clear key light direction, bicycle frame rim light, wheel highlights, tire contact shadow, low road or floor reflection, wall-floor intersection shadow, and color-block planes supporting the product.
- For B-level color-block studio routes, record `骑行色板锚点` and `骑行选中色板` in review Markdown. Expand the selected `bg_bicycle_contrast_colorblock_studio / 骑行强对比几何色块棚拍背景` contrast hue relationship into the final prompt together with the selected bicycle angle and lighting language. The selected hue relationship should echo or highlight the obvious non-black/white/gray/silver product color extracted from the uploaded product image; when the product image is mainly black, white, gray, or silver, rotate through the clash hue pool. When supplemental requirements mention 浅色、清爽、明亮、白底、淡色 or 轻盈, keep the same hue relationship but increase the area of light or neutral tones. The three color layers should have clear hierarchy: one large-area spatial base color, one medium-area high-chroma spatial main color, and one small-area neutral light cut-plane or breathing layer; dark versions use the dark base as the largest area, while light versions use the light/neutral breathing color as the largest area. The background geometry should form a studio space through walls, floor, side wall, and diagonal cut planes; the neutral light plane should act as a corner plane, side wall, or title breathing layer, with the diagonal planes following one motion direction.
- A-level resolves to `骑行广告摄影海报化出行场景款`: first choose and record one advertising-photography plus posterized background treatment from 大面积天空色场、晚霞情绪底、城市远景虚化、山体剪影、海岸线与道路切线、围墙局部色块、地平线构图. Then choose outdoor elements only to support that color field, composition line, atmosphere, speed direction, and product/rider relationship. A-level should feel like a designed brand cycling poster made from outdoor advertising photography: simplified background, magazine-ad color grading, light posterized treatment, reduced distant detail, dramatic light, stronger side-backlight, visible ground speed smear, compressed foreground/background depth, stronger speed perspective, and one strong visual structure. Add controlled sports-poster edge textures as poster accents: low-to-medium density halftone dots, torn-paper edges, white distressed paper wear, a small amount of noise grain around the outer edges, one large dry-brush stroke with linear arrow scratches in the lower-right corner, and light worn-ink texture on the title face. These accents must support speed, conflict, and emotion, stay around the outer edges and title area, and must not become clutter or extra copy. When assembling the final prompt, translate generic `自然场景融入` composition language into `广告摄影海报化场景构图`, and include this target sentence for bicycle A-level: `一个有冲突、有速度、有情绪的骑行视觉海报`. Do not make it a plain outdoor photograph or travel-landscape image that fully explains mountains, rivers, roads, trees, and sky at the same time.
- S-level resolves exactly one topic-scene direction and records it in review Markdown: `骑行微缩主题场景` or `骑行超现实商品场景`.
- Supplement words like 小世界、小场景、微缩、城市道路、山路、赛道、绿道、公路、旅行路线、路标、微型骑手、微型树林、微型山坡 route bicycle S toward `骑行微缩主题场景`.
- Supplement words like 巨物化自行车、车轮变太阳、车轮变跑道、车轮变山路、尺度错位、漂浮、悬浮、云海、抽象地形、未来赛道、现实与虚构 route bicycle S toward `骑行超现实商品场景`.
- If no supplement selects a bicycle S direction, choose randomly between `骑行微缩主题场景` and `骑行超现实商品场景`, then record the selected direction in review Markdown.
- B/A/S all choose and record one bicycle product angle from `cat_bicycle.visual_traits`: 完整正侧面、三分之四侧前方、低机位仰拍、轻俯视三分之四、前轮近景带车身延伸、车架局部特写但保留整车识别、骑行中动态侧逆光、远景小车加大环境. For 4:3 B-level, prefer 大车近景广告构图、低机位三分之四侧前方、前轮近景放大、前轮近景带车身延伸, or 轻俯视三分之四. For A-level, prefer 骑行中动态侧逆光, 低机位三分之四侧前方, or 前轮近景带车身延伸; record one speed-perspective choice such as 地面速度拖影、前后空间压缩、道路线向后收束、近轮放大远景压缩, and write it into the final prompt.
- If the uploaded bicycle product image is a flat side-view product cutout, do not treat that source angle as locked unless the user explicitly asks to keep the original angle. Keep the frame structure, color, wheel ratio, brand recognition, and core product identity, but allow advertising-style angle reconstruction through the selected bicycle product angle.
- Bicycle title typography should use the fixed cycling typography cue in `cat_bicycle.visual_traits`: 高级运动广告宽体粗黑体、端正稳定、字面宽大、笔画厚实、几何感强、边缘干净、切角克制、整体清晰利落. Choose the main title color by contrast with the title background plane: use white/light title color on dark background planes, and black/near-black title color on light background planes. Add at most one accent color from `骑行色板锚点` or the high-chroma main color in `骑行选中色板` on one continuous keyword or key phrase; keep the remaining main title characters in the chosen main title color, and reuse the same accent color for subtitle numerals when emphasis is needed. Do not call a typography reference image for this rule.
- The selected bicycle scene direction, product angle, A-level advertising-photography plus posterized background treatment, B-level product-photography lighting language, and cycling title typography must become actual final-prompt language, not just review labels.

## Visual Expression Mode

`visual_expression_mode` is an internal or advanced-test visual routing preference. It is not a quality grade and does not replace `context_strength` in `09_background_recipes.csv`. Ordinary users can use `visual_preset_level` instead.

Values:

| visual_expression_mode | Meaning | Routing Effect |
|-|-|-|
| `自动` | infer from title, subtitle, product, business line, marketing type, and supplement | default; choose stable support unless clear scene/use cues exist |
| `稳定承托` | product clarity and clean information are primary | prefer stable product arrangements, clean information hierarchy, stable composition, and product-support backgrounds |
| `场景表达` | use reason, lifestyle, content, or activity context is primary | prefer scene display, use relation, scene-immersive composition, and scene/context backgrounds |

Automatic mode:

- Prefer `稳定承托` when the brief emphasizes product clarity, price/benefit, professional value, clean style, single product, same-category multi-SKU, or no clear use scene.
- Prefer `场景表达` when the title, subtitle, supplement, visible product role, or category contains clear use cues such as lifestyle, commute, office, study, travel, shooting, sport, outdoor, home, practice, performance, wearing, holding, operating, riding, listening, or game character/world context.

Routing rules:

- Resolve `visual_expression_mode` before selecting product combination.
- For `biz_membership + cat_membership_day + B`, fully inherit the recycle B visual product route before applying general stable-support defaults: use `rel_multi_recyclable` plus `combo_multi_recyclable` for two or more physical product assets, `bg_recycle_service_graphic`, no people, and no support surface or one continuous support surface. This inheritance is visual only; membership prompts and reviews must not use recycle coverage or service wording.
- `稳定承托` biases product combination toward `combo_single_hero`, `combo_same_category_multi_sku`, `combo_product_cards` for true multi-object structures, `combo_subject_card_carrier` when the user asks for a card carrier, and `combo_service_flow` for recycle service. It biases composition toward `comp_stable_product`, `comp_premium_closeup`, `comp_card_grid`, or light product-focused compositions. For 消费电子 B-level routes, express stable support as product clarity plus minimal launch design, refined technology product space,主体清晰展示, functional close-up, advanced geometric support space, light strong-contrast or dark strong-contrast lighting, material edge highlights, shallow micro-scene details, light information modules, and a clear title area; select one main B-level direction from主体清晰展示, functional close-up, or advanced geometric support space, optionally fuse one or two secondary directions only to support product texture, spatial support, or detail expression, then record the main direction, secondary directions, and one lighting strategy in review Markdown. When B-level selects dark strong-contrast lighting, take a heavy color from the product image, screen image, brand color, or product material as the dark tonal base; keep readable brightness layers, material texture, spatial planes, light-beam falloff, and visible background depth in the dark areas; use clear key light or side/back light, product rim light, material reflection, subtle floor reflection, contact shadow, and a few restrained thin-line accents; accent color should adapt to product and brand tone instead of locking to one hue. When B-level selects light strong-contrast or brand/product main-color strong lighting, use a main color extracted from the product, screen image, or brand tone to form large background, geometric stand, or local space color blocks; shape the space with a clear directional key light, bright soft-lit area, light/shadow cuts, physical cast shadows, material highlights, product rim light, and contact shadows instead of cold gray showroom light or decorative lines. When a 消费电子 B/A/S preset is matched, this broad stable-support background bias must not override that preset's `preferred_background_ids`. Otherwise, it biases background toward `bg_clean_gradient_product`, `bg_light_tech_product_space`, `bg_new_arrival_stage`, `bg_product_podium`, `bg_card_module_benefit`, `bg_graphic_operation`, `bg_collectible_flat_collage`, `bg_game_flat_light`, `bg_premium_dark_trust`, or `bg_recycle_service_graphic` according to business line and category.
- `场景表达` biases product combination toward `combo_scene_display`, `combo_cross_category`, `combo_ce_single_scene`, `combo_ce_curated_assortment`, or `rel_primary_support` with scene props/supporting subjects when appropriate. It allows hand, wearer, user, operator, rider, player, or partial person relationships when they explain the product value, support the title semantics, match the user supplement, or are present in user assets. It biases composition toward `comp_scene_immersive` or other scene-aware compositions. For 消费电子 A-level routes, first choose `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式` or `combo_ce_partial_people_use / 消费电子人物局部使用`, then express scene value through that selected combination direction. For 消费电子 S-level routes, first choose `combo_ce_miniature_theme / 消费电子微缩主题场景` or `combo_ce_surreal_product_scene / 消费电子超现实商品场景`, then express topic value through that selected combination direction. When a 消费电子 B/A/S preset is matched, this broad scene-expression background bias must not override that preset's `preferred_background_ids`. Otherwise, it biases background toward `bg_lifestyle_scene_soft`, `bg_light_tech_product_space`, `bg_new_arrival_stage`, `bg_collectible_flat_collage`, `bg_content_topic_flat_3d`, `bg_game_abstract_light`, `bg_outdoor_cycling_scene`, `bg_work_study_desk`, `bg_travel_camera_scene`, or `bg_game_ui_graphic` according to category and business line.
- People, hands, wearing, operation, props, and scene extensions should serve the theme, product value, selected visual expression mode, people participation setting, or provided assets, while keeping the subject readable.
- Keep business-line tone as the parent. N 品类 and 消费电子 can both use either mode; 回收 usually stays stable/service-led unless the user explicitly asks for a scene expression.
- When the business line is `biz_n_category / N 品类` and the category is `cat_bicycle / 骑行`, `cat_billiards_cue / 台球杆`, or `cat_musical_instrument / 乐器`, B-level routes call `frag_premium_product_lighting / 高级商品光影调制` as the product-photography lighting skeleton, then modulate the lighting through that category's `visual_traits`.
- When the business line is `biz_n_category / N 品类` and the category is `cat_billiards_cue / 台球杆`, resolve the product combination first, then read `arrangement_principle`, `positive_visual_language`, and `prompt_fragment` from that selected combination row as the only source of台球杆摆放方式. B-level no-people routes use `combo_billiards_cue_diagonal_texture / 台球杆斜向质感陈列`; A/S no-people routes use `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列`; single-cue people-use routes use `combo_billiards_cue_people_use / 台球杆人物使用陈列`. When the selected combination is `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列`, keep the route locked to this rule: `主视觉必须以杆尾或握把附近的局部放大为第一视觉重心，并清晰看到至少一个高价值细节；多杆错落陈列且每根杆可识别。` Workflow-level cue rules should preserve cue identity, color, texture, rings, grip, and key details, but should not restate a separate default close-up, local-enlargement, or placement rule outside the selected product combination.
- For `cat_billiards_cue / 台球杆` B-level routes, prefer `bg_billiards_premium_texture_display / 台球杆高级材质陈列背景`: choose one main support material from 深色台呢、绒面托盘、皮革台面、深木台面、石材块、浅色纸面, or 高级墙面; add only low-presence billiards context such as blurred billiard balls, table edge, cue rack, glass reflection, or dark club lighting when it helps the material story.
- For `cat_billiards_cue / 台球杆` A-level routes, keep product combination on `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列` only when `people_participation=否 / 无人物陈列`; prefer `bg_billiards_clean_table / 台球杆_生活兴趣场景_中语境`. If `people_participation=是 / 人物参与`, switch the product combination to `combo_billiards_cue_people_use / 台球杆人物使用陈列` rather than `combo_billiards_cue_natural_texture_display`, and let that selected combination own the cue placement and people-use shot logic. This single-cue people-routing note applies only to a single uploaded cue asset; when multiple cue assets or multiple product assets are uploaded, do not apply the single-cue restriction by default.
- Express A-level as one unified life-interest scene: use loft, wood, or light-interior space as the carrier, and integrate low-presence functional cues such as cueing posture, chalk, black-8 path cues, or training-table relations into the same scene. The result should emphasize stability, precision, and control while staying restrained, professional, and product-centered.
- For light-tone A-level routes, it is valid to use off-white walls, light stone planes, plant shadows, books, paper, fabric, or a few quiet objects as low-presence lifestyle carriers, as long as they read as a calm interest space rather than home decor, cafe atmosphere, or generic lifestyle poster.
- Supplement words like 兴趣、爱好、入门、周末、圈层、loft、木质、轻室内、训练、练球、控球、准度、精准、稳定、架杆、巧粉、黑球8, or 收藏空间 all strengthen the same A-level life-interest route. For billiards-cue A/S backgrounds, select exactly 2 visible background elements for each run and keep the final prompt concise.
- For `cat_billiards_cue / 台球杆` S-level routes, keep product combination on `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列` when `people_participation=否 / 无人物陈列`; prefer `bg_billiards_surreal_concept_space / 台球杆超现实概念空间_强语境`; keep people participation at `否 / 无人物陈列` by default. When a single uploaded cue asset explicitly routes to `people_participation=是 / 人物参与`, switch to `combo_billiards_cue_people_use / 台球杆人物使用陈列` on the same concept background, and let that selected combination own the cue placement and people-use shot logic while the concept carrier only modulates the space.
- S-level is not limited to dark surreal space. It may also use bright light-tone surreal or geometric-concept carriers such as sand-white or champagne concept space, planet-like backdrops, floating rock fragments, misty air, pale stone platforms, arches, circular openings, steps, columns, light-toned architectural planes, and light metallic spheres, provided the result still reads as concept advertising rather than ordinary indoor display.
- Billiards-cue title typography should use the fixed cue-typography cue in `cat_billiards_cue.visual_traits`: 高级器材广告高对比中文宋体或衬线字体，字面修长，结构稳定，粗细对比明确，边缘干净，收笔克制，具有收藏级专业器材质感。 Choose the main title color by contrast with the title background space: use 象牙白、暖白或浅金白 on dark backgrounds, and 深墨绿、近黑或深棕色 on light backgrounds. Add at most one accent color from 木纹暖色、金属环高光 or 深绿台呢环境色 on one continuous keyword or key phrase; keep the remaining main title characters in the chosen main title color, and reuse the same accent color for subtitle numerals when emphasis is needed. Do not use promotional heavy Heiti, variety-show block lettering, thick gradients, outline/shadow, or large title panels.
- For `cat_billiards_cue / 台球杆`, title sizing is also not B-only: resolve semantic line breaks and per-line character count first, then set title size by visual weight so the cue body stays first visual subject and the title remains secondary. Keep the detailed assembly rule in `prompt-assembly.md`; treat any `22%-30%` title-group range only as an upper-bound QA check, not as a direct font-size target.

## People Participation

`people_participation` is a product presentation switch. It decides whether people, hands, wearing, operation, or user interaction become part of the product combination. It does not decide the exact participation form by itself.

Values:

| people_participation | Meaning | Routing Effect |
|-|-|-|
| `自动` | infer from title, subtitle, product value, visible assets, visual expression mode, business line, and supplement | default; allow people only when they help explain product value or theme |
| `否` | no people participation | keep product display, props, and background free of people, hands, wearing, operation, user, rider, player, or partial person relationships |
| `是` | people use product | route the product combination toward a visible use relation with the user-provided product, such as wearing, holding, operating, riding, performing, trying, or showing the product in use |

Routing rules:

- Resolve initial `people_participation` after `visual_expression_mode`; after product relation and product combination are known, correct it when the product structure makes people use unsuitable.
- Apply forced no-people overrides before any positive people-use routing: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, resolves `people_participation` to `否 / 无人物陈列` even if the user explicitly provides `人物参与=是`.
- `人物参与=否` biases product combination toward pure product display, subject card carrier, product cards, same-category multi-SKU, service flow, or product-focused scene display without people.
- `人物参与=是` routes the product combination toward people using the user-provided product to clarify use value, scale, lifestyle, activity context, or game character meaning. This routing remains active under both `稳定承托` and `场景表达`.
- When `people_participation=是 / 人物参与`, the person must form a clear and reasonable use relation with the user-provided product; mere co-presence, decorative posing, or casual holding is not enough.
- `人物参与=自动` resolves from product value, visible assets, title semantics, supplement, and visual expression mode. Choose people participation only when the product value benefits from a visible use relation.
- For `cat_billiards_cue / 台球杆`, if the upload is a single cue asset and `people_participation=是 / 人物参与` is selected, do not keep `combo_billiards_cue_diagonal_texture` or `combo_billiards_cue_natural_texture_display`; switch to `combo_billiards_cue_people_use / 台球杆人物使用陈列` so the visible use relation, not the no-people cue-display skeleton, becomes the primary organizing language. When multiple cue assets or multiple product assets are uploaded, forced no-people override applies first and this single-cue people-routing rule does not run.
- For `cat_billiards_cue / 台球杆`, when `people_participation=是 / 人物参与`, require a clear bridge hand and grip hand with reasonable positions, a believable cue-tip direction and real use posture, and product identity that still reads as the same uploaded cue even if the angle changes for the shot.
- For `biz_consumer_electronics / 消费电子`, A-level routes select from the `combo_ce_single_scene / 消费电子单品场景表达` candidates: `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式` or `combo_ce_partial_people_use / 消费电子人物局部使用`, and write the selected combination ID and Chinese name into review Markdown. `combo_ce_partial_people_use / 消费电子人物局部使用` is suitable for one main product. When two or more consumer-electronics products are provided, whether same-category or cross-category, resolve people participation to `否 / 无人物陈列`; express scene value through product grouping, selected scene direction, background, lighting strategy, material detail, and information modules.
- User supplement is optional. If it mentions people, hands, wearing, holding, operation, partial people, no-face people, no people, pure product, small scene carrier, miniature scene, surreal scene, floating product, scale shift, or abstract/future space, use it to narrow the selected consumer-electronics candidate; otherwise keep the preset candidate pool as the default random source.
- When multiple uploaded product assets, multiple visible product subjects, `rel_multi_collection / 多商品集合`, or other multi-subject merchandise structures are present, resolve people participation to `否 / 无人物陈列`. Use topic display, unified space, light, product grouping, and information modules instead of a person using only one item.
- Do not create a people-use exception for cross-category or other multi-subject merchandise assortments. When multiple uploaded product assets, multiple visible product subjects, or `rel_multi_collection / 多商品集合` are present, keep `人物参与=否 / 无人物陈列` and express scene value through product grouping, light, props, and information modules instead.
- `稳定承托` can keep the overall scene, props, and information layer restrained, while the selected people-use relation still needs to be visible and product-centered.
- Game character assets are already main visual subjects; `人物参与` controls additional human/user interaction, not whether the provided character itself may appear.

## Game Visual Asset Linking

When uploaded assets look game-related, resolve business/category boundaries before product relation and product combination. The `biz_n_category + cat_game` route only covers single game character / role illustration and multiple game character / role illustration assets.

Boundary rules:

| Asset | Route |
|-|-|
| 游戏人物 / 角色立绘 / 皮肤号视觉 | `biz_n_category + cat_game` |
| 多张游戏人物 / 多角色立绘 | `biz_n_category + cat_game` |
| 会员充值 / 游戏点卡 / 权益卡 / 虚拟卡面 | `biz_n_category + cat_card_coupon` |
| Switch / PS5 / 手柄 / 游戏主机 / 掌机 / 外设 | `biz_consumer_electronics + cat_game_device` |
| 多张混合游戏素材 | reserved for future multi-category routing; use general routing or ask if business meaning is unclear |

For `biz_n_category + cat_game`, resolve `game_visual_asset_type` to one of the two in-scope values before product relation and product combination.

| game_visual_asset_type | Visual Role | relation_id | combination_id | Background Use |
|-|-|-|-|-|
| `game_character_visual` 游戏人物 / 角色立绘 | poster main visual character | `rel_single_hero` | `combo_scene_display` or `combo_single_hero` | `bg_game_flat_light` for B, `bg_game_abstract_light` for A, `bg_game_ui_graphic` for S |
| `game_multi_character_visual` 多张游戏人物 / 多角色立绘 | coordinated role-group visual with light hierarchy | `rel_primary_support` | `combo_scene_display` | `bg_game_flat_light` for B, `bg_game_abstract_light` for A, `bg_game_ui_graphic` for S |

For `game_character_visual` and `game_multi_character_visual`, collect `neg_game_character_card_misuse` with the other selected negative rules.

Game visual placement and typography:

- In 4:3, 16:9, or 2:1 landscape, keep the title reading weight on the left while the game character or role-group visual sits on the right or right-leaning main visual area. Character effects may extend lightly into the shared space when they do not block title, subtitle, or key face/body features.
- For multiple game characters, describe the result as `角色群像`, `协同角色主视觉`, or `轻主次关系`; avoid treating it like ordinary product cards or collectible-toy merchandising.
- Game title typography should use fantasy high-contrast Chinese display type, slender elegant game-topic lettering, or ornate-but-restrained character-event title type. The title should have clear thick-thin contrast, elegant curves, sharp finishing strokes, and light decorative rhythm while staying refined, front-facing, and flat.

## Product Linking

Use image count and visible structure:

| Condition | relation_id | combination_id |
|-|-|-|
| one clear product | `rel_single_hero` | `combo_single_hero` |
| multiple cue images in `biz_n_category + cat_billiards_cue` | `rel_multi_collection` | `B 档：combo_billiards_cue_diagonal_texture / 台球杆斜向质感陈列；A/S 档：combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列，并继承“主视觉必须以杆尾或握把附近的局部放大为第一视觉重心，多杆错落陈列且每根杆可识别”` |
| one game character or role illustration as campaign subject | `rel_single_hero` | `combo_scene_display` or `combo_single_hero` |
| multiple game characters or role illustrations as campaign subjects | `rel_primary_support` | `combo_scene_display` |
| one main product with small accessories or scene props | `rel_primary_support` | `combo_scene_display` or `combo_single_hero` |
| one clear subject should sit inside a visible card, frame, ticket, or UI panel | `rel_single_hero` or `rel_primary_support` | `combo_subject_card_carrier` |
| multiple products in one category | `rel_multi_collection` | `combo_same_category_multi_sku` or `combo_product_cards` |
| multiple categories | `rel_multi_collection` | `combo_cross_category` or `combo_product_cards` |
| recycle with two or more categories | `rel_multi_recyclable` | `combo_multi_recyclable` |
| membership B with two or more physical products | `rel_multi_recyclable` (visual parent only) | `combo_multi_recyclable` (visual parent only) |
| recycle flow or trust message | `rel_service_consultant` | `combo_service_flow` |
| title includes TOP/ranking | `rel_ranked_list` | `combo_ranked_products` |

For `biz_consumer_electronics / 消费电子`:

- B-level prioritizes `combo_single_hero / 单品主推式陈列` with minimal launch design, refined technology product space,主体清晰展示, functional close-up, advanced geometric support space, light strong-contrast or dark strong-contrast lighting, material edge highlights, light information modules, shallow micro-scene details, and product-centered composition. Select one main B-level direction from主体清晰展示, functional close-up, or advanced geometric support space; optionally fuse one or two secondary directions only to support product texture, spatial support, or detail expression. When the selected lighting strategy is dark strong-contrast, take a heavy color from the product image, screen image, brand color, or product material as the dark tonal base; keep readable brightness layers, material texture, spatial planes, light-beam falloff, and visible background depth in the dark areas; use clear key light or side/back light, product rim light, material reflection, subtle floor reflection, contact shadow, and a few restrained thin-line accents, with accent color adapting to the product and brand tone rather than a fixed hue. When the selected lighting strategy is light strong-contrast or brand/product main-color strong lighting, use a main color extracted from the product, screen image, or brand tone to form large background, geometric stand, or local space color blocks; shape the space with a clear directional key light, bright soft-lit area, light/shadow cuts, physical cast shadows, material highlights, product rim light, and contact shadows instead of cold gray showroom light or decorative lines. Record the main direction, any fused secondary directions, and one lighting strategy in review Markdown.
- A-level prioritizes `combo_ce_single_scene / 消费电子单品场景表达`, then resolves exactly one A combination direction from `08_product_combinations.csv`: `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式` or `combo_ce_partial_people_use / 消费电子人物局部使用`. The selected combination direction must become the primary scene language in the final prompt, not just a candidate phrase.
- A-level with two or more products resolves to `人物参与=否 / 无人物陈列`; use `combo_same_category_multi_sku / 同品类多款`, `combo_cross_category / 跨品类集合`, or `combo_ce_curated_assortment / 消费电子专题货盘陈列` according to the brief. This is part of the broader multi-asset / multi-subject forced no-people override.
- S-level prioritizes `combo_ce_curated_assortment / 消费电子专题货盘陈列`, whether the products are single-product, same-category, or cross-category.
- `combo_ce_curated_assortment / 消费电子专题货盘陈列` resolves exactly one S combination direction from `08_product_combinations.csv`: `combo_ce_miniature_theme / 消费电子微缩主题场景` or `combo_ce_surreal_product_scene / 消费电子超现实商品场景`. The selected combination direction must become the primary arrangement and scene language in the final prompt, not just a candidate phrase.

Consumer-electronics lighting strategy should be concrete and visible, not vague cool technology color. Choose one according to product, title, season, assets, and references: light strong-contrast, dark strong-contrast, natural window light, side/back light, brand/product main-color strong lighting, or neutral material light. Also randomly choose one or two consumer-electronics photography modifiers and include them in the final prompt and review Markdown: 奢华编辑照明、高对比度影棚照明、窄聚光光束、戏剧性阴影衰减、高端杂志广告风格、电影级产品摄影. If consumer electronics uses a shared background such as `bg_lifestyle_scene_soft`, `bg_travel_camera_scene`, `bg_graphic_operation`, or `bg_clean_gradient_product`, do not modify the shared background recipe itself; modulate it through the selected consumer-electronics lighting strategy, material detail, and an advertising design layer. Real-scene routes should include clear light direction, light/shadow cuts, ordered props, light information modules, product edge highlights, contact shadows, or miniature spatial storytelling, instead of a plain photographic scene.

For `cat_collectible_toy`, resolve three visual directions from supplement and visual expression mode. When an A preset is matched, use the journal-style paper-craft route below as the default flat direction:

- Build one continuous paper-craft layout with a torn-paper title area on the left and a pale-green grid memo on the right.
- Place a top ring binder and a small piece of paper tape on the memo, then add sparse stickers and dotted doodle lines as the finish layer.
- Use a warm cream-white and pale-grass-green paper palette, allowing the supplied toy colors to become the accent colors.
- Place one toy or a small toy group on the grid memo as clear white-edge cutouts; for multiple toys, establish light primary/support hierarchy through size and overlap.

All collectible-toy title routes use rounded, friendly modern display typography with a front-facing flat baseline and stable solid color. Do not use outlines, shadows, 3D lettering, metallic effects, or gradient title effects. Collectible-toy routes never select `bg_new_arrival_stage / 新品发布_商品高光_中语境`, including when the marketing type is `m_new_arrival / 新品上新`; use `bg_product_podium / 通用_商品展台_价值陈列_弱中语境` for stable display, or `bg_collectible_flat_collage / 潮玩_平面拼贴专题_中语境` and `bg_content_topic_flat_3d / 潮玩_平面立体融合_中语境` according to the resolved topic direction.

| cue | preferred combination | preferred background |
|-|-|-|
| supplement says 平面风 / 平面拼贴 / 卡片 / 收藏卡 | `combo_subject_card_carrier` or `combo_product_cards` | `bg_collectible_flat_collage` |
| no flat/3D supplement and visual expression mode is `场景表达` | `combo_scene_display` or `combo_same_category_multi_sku` | `bg_content_topic_flat_3d` |
| supplement says 立体风 / 立体展示 / 展台 / 橱窗 | `combo_scene_display` or `combo_same_category_multi_sku` | `bg_product_podium` or `bg_lifestyle_scene_soft` |

Collectible-toy element discipline:

- 平面风: choose 1-2 flat visual element families, such as torn paper plus stickers, color blocks plus small cards, or grid memo plus paper tape. Keep the paper-craft language unified; use dotted doodle lines as the only drawing-like finish layer.
- 场景表达 without flat/3D supplement: use flat topic background plus light 3D display. Choose 1-2 flat element families and 1 main display support, with at most 1 auxiliary support.
- 立体风: use one clean cute 3D display space, such as a gift-window, collection shelf, soft podium, or small toy display area. Keep props and supports in one visual language.
- In all three directions, product hierarchy comes first: one product or small group can lead, supporting toys stay companion-like, and decoration only builds topic feeling.

Do not require detailed product names when visual display is enough.

## Product Card Grid Trigger

Use `combo_product_cards` mainly when there are multiple visual objects or an explicitly parallel information structure.

Strong triggers:

- multiple uploaded product images
- multiple visible product subjects
- multiple SKUs, categories, accessory sets, service object groups, flow nodes, ranked lists, or comparison grids

Game character groups use role hierarchy first: one main character with supporting characters in scene display.

Weak triggers:

- multiple subtitle benefit points
- multiple selling points
- multiple parameters

Weak triggers create light information modules around the main product while keeping the selected single-hero, scene-display, or subject-card-carrier combination.

## Background and Benefit Routing

For `m_flash_sale`, `m_subsidy_benefit`, and `m_sales_ranking`, select the background from business line, category, product relation, product combination, composition, and scene semantics first. Then add `frag_benefit_modules_light` from `11_prompt_fragments.csv` as an information layer when the user provided price, discount, subsidy, guarantee, service, or ranking copy. Benefit modules do not act as the background recipe.

When no matched `visual_preset_level` exists, infer the route from:

1. `04_marketing_types.csv`
2. `03_business_category_map.csv`
3. `07_product_relations.csv`
4. `08_product_combinations.csv`
5. `06_composition_camera.csv`
6. `09_background_recipes.csv`
7. `11_prompt_fragments.csv`
8. `12_negative_rules.csv`

When reading product and background rows, do not use only `prompt_fragment`. Also read:

- `01_business_lines.csv`: `base_visual_tone`, `visual_priority`
- `03_business_category_map.csv`: business-specific meaning and default context as business-role cues, not as the full visual style
- `07_product_relations.csv`: `hierarchy_rule`
- `08_product_combinations.csv`: `arrangement_principle`, `positive_visual_language`
- `09_background_recipes.csv`: `positive_visual_language`, `continuity_rules`
- `11_prompt_fragments.csv`: reusable positive prompt fragments and QA fragments
- `12_negative_rules.csv`: negative rules referenced by `negative_rule_ids`

Resolve every `negative_rule_ids` field after selecting rows. Deduplicate IDs, then compress essential constraints into the final prompt. Keep the full selected IDs and merged `negative_prompt_fragment` values in the card-style review Markdown defined in `generation-execution.md`.

## Visual Inheritance

Use this order when composing the visual language:

```text
业务线基础调性
-> 品类语义
-> 营销强度
-> 视觉方案档位
-> 视觉表达模式
-> 人物参与
-> 商品关系
-> 商品组合
-> 构图能量
-> 背景承载
```

The business line is the parent tone. Category, marketing type, product combination, composition, and background are modulation layers. If a downstream layer conflicts with the business-line tone, keep the business-line tone and soften the downstream expression unless the user explicitly asks for that stronger style.

For example, 消费电子 can use light-tech cues, but default to clean professional product presentation instead of dark neon, heavy stage, or complex sci-fi space. 回收 can use benefit modules, but must still read as recycle service rather than ordinary product sale. N 品类 can use lifestyle or editorial cues, but should still preserve category logic and product clarity.

Sale vs recycle meaning for the same product should be resolved mainly from business line, title/subtitle, marketing type, and service/background atmosphere. Do not use product category alone to decide sale or recycle visual language.

## Asking Questions

Ask only when needed. Prefer one concise question.

Ask when:

- business line is unclear and changes the poster meaning
- the title/subtitle contains risky factual claims without source
- exact output format is missing
- the user asks for a ranking, price, service promise, model, or bundle that is not provided

Do not ask when:

- product category can be visually inferred with enough confidence
- product relation and combination can be selected from image count and marketing type
- background or composition can be linked from existing tables
