# Visual QA v0.1

## Purpose

Use this file as the single visual review checklist after a poster image is generated. Judge the image against the normalized task card, selected parameters, user product assets, and selected negative rules.

For typography, `会员` A/S main titles use `SourceHanSerifSC-Heavy.otf` by default; an A/S `补充要求` containing `特殊字` uses the bundled brush-title reference style. `会员` B main titles use a modern display-Heiti treatment: front-facing, flat, solid-color, firm and stable. Subtitle, label text, and decorative text follow their respective typography rules.

Do not judge only by subjective taste. Classify concrete PASS / FAIL items by layer, then use the matching targeted correction template from `generation-execution.md`.

## Contents

1. QA Inputs
2. Decision Policy
3. Layer Checklist
4. Targeted Retry Mapping

## 1. QA Inputs

Before visual QA, read or reconstruct:

- user input: product assets, main title, subtitle, decorative text, business line, format, visual expression mode, people participation, supplement
- normalized task card: business line, category, marketing type, visual expression mode, people participation, product relation, product combination, composition, background
- selected background subset when the chosen background row defines one
- selected Chinese fragments: business tone, product relation rule, product arrangement, composition, background visual language, continuity rule
- merged `negative_rule_ids` from `12_negative_rules.csv`
- generated image

When uploaded product images exist, compare the generated product directly against the uploaded product image instead of judging product correctness only from memory or general category impression.

If two or more uploaded product assets, or two or more distinct product subjects, are present, run product QA object by object instead of only at whole-image level. For each object, check both groups separately:

- identity attributes: color, structure, texture/material pattern, logo/marking, part relationship, and proportion
- layout attributes: size, position, angle, front/back hierarchy, crop boundary, and occlusion state

If any required object drifts in either group, mark `商品层` as FAIL even when the overall image still looks category-correct.

For every `biz_membership + cat_membership_day` A/S 2:1 head, read `template.json.layout_coupling` before foreground QA. `会员` B is excluded. First verify that the AI base has no readable title/fixed layers and that the foreground remains inside `foreground_region`. With zero supplied product assets, verify the direct foreground uses only the default gift boxes, ribbons, and coins, without an outer gift-box container. With one visibly gift-box asset, verify the same direct composition and the uploaded gift box's visible appearance, structure, color, material, and key identifying features. With other 1-4 product assets, reconstruct `slot_replacement_map` from `template.json.product_slots`; verify no product subject is above `foreground_visible_top_max_y`, the gift-box opening and low side corners meet the initial 75%-width target, and every supplied product occupies its named `reference_subject` slot with its required size, position, angle, layer order, and visible focus. Verify automatic slot assignment unless the user explicitly overrode it: the strongest portrait product should occupy the center main slot, flat products should occupy the side slots, and upload order must not be used except to break a shape/hierarchy tie. For every supplied device with a visible screen, viewfinder, or display window, compare its original screen content object by object; a black screen, pure-color screen, empty screen, or altered person, scene, or interface is a `商品层` FAIL. The group must read as a staggered, layered lower foreground rather than a complete front-facing lineup. Bottom-edge emergence/crop is optional: decide it from the product's size, recognizability, and the lower visual hierarchy; smaller products may be fully visible. When it is used, foreground coins must naturally occlude the lower transition, rather than leaving a hard crop; do not require every product to expose an equal half. If the final prompt does not explicitly enumerate every active `reference_subject → uploaded product` mapping, mark pre-output QA as FAIL and rebuild the prompt before generation. Then verify the title-only PNG: exact user copy, usable alpha, visible height exactly matches `title_layer.visible_height`, width is proportionally derived from alpha bounds, and the centered title has no collision with future brand/date reservations. By default it must be rendered from `SourceHanSerifSC-Heavy.otf`; only with `补充要求=特殊字` compare it with the brush reference for stroke thickness, thick-thin contrast, tapering, spacing, and brush rhythm. A wrong title style is a `文字层` FAIL and retries only the title asset. These failures are independent and retry only their own asset. After composition, inspect title, foreground, mark, date, rule control, and wave together; any collision is `合成碰撞失败`.

If the generated image cannot be inspected, mark Visual QA as not reached and run Technical QA instead.

## 2. Decision Policy

Use these conclusions exactly:

- `通过`: core task is satisfied; only minor subjective preference remains.
- `需定向重生`: one or more correctable visual layers fail; write the failed layer and one targeted correction prompt.
- `需人工后期`: direction is usable, but exact Chinese text, small logo, tiny product detail, or factual micro-text is unlikely to be fixed reliably through one more generation.

Any FAIL in a required layer should trigger `需定向重生` when image generation is available. Default retry count is one.

The targeted correction prompt is a local repair instruction, not a new full generation prompt. Default to the current generated image as the sole retry input. Add a reference image only when the editing capability explicitly distinguishes its role from the edit target; otherwise, keep mother-layout and product-source images in QA only. Submit `以当前图为唯一编辑目标。编辑范围。唯一修改动作。其余内容不变。` For measurable position, scale, crop, or slot-geometry repair, omit the diagnostic clause from the submitted prompt: record it in QA notes and submit one direct action in the form `以当前图为唯一编辑目标。仅将……，使……，不替换、重排或回退当前商品内容。其余内容不变。`; a combined scale-and-translate instruction counts as one geometry action. It may use one or two short sentences, but must not enumerate passed composition, product attributes, lighting, typography, background, negative rules, or preservation logic. Record those details in the QA notes instead.

When only one layer fails, repair only that layer. When multiple layers fail, choose the most blocking layer first. Do not turn a targeted correction prompt into the original full prompt or a new creative brief. For all business lines, including `biz_consumer_electronics / 消费电子`, the submitted retry must behave like a local patch: normally state the concrete failure, one direct action, then `其余内容不变。`; use the geometry-repair exception above when a relative canvas position, proportional size, crop boundary, or reference-slot relation is the actionable target.

## 3. Layer Checklist

### 3.1 Text Layer

PASS:

- Main title and subtitle use user-provided text and are readable at first glance; text color has enough brightness or hue contrast against the current background.
- Main title appears once.
- Subtitle appears once, or list-style subtitle is split into light modules without repeating the full sentence.
- Typography is front-facing and flat, with stable baseline and no perspective tilt, skew, or spatial rotation.
- Main title and subtitle have a clear visual hierarchy and breathable spacing.
- Every non-empty `会员` B `2:1` title-group subtitle uses the bundled Alibaba PuHuiTi Regular font through `assets/subtitle-typography.json`; its final font size and title gap equal the policy values scaled by final canvas width. In every other route, verify that the AI-rendered subtitle matches the user-provided copy and remains readable.
- Main title uses stable flat color or restrained tonal handling.
- 1:1 square posters keep the main title as a complete single-line title unless the user explicitly asks for line breaks.
- 4:3 and 16:9 landscape posters split main titles longer than 4 Chinese characters into semantic two-line title groups, while preserving complete words, brand names, category names, numeric benefits, and fixed phrases.
- 2:1 landscape posters keep the main title single-line when its measured visible width does not exceed the active route maximum; otherwise they split at a semantic boundary. For 会员 A/S the reference policy is 110px / 908px at 1125px width; for 会员 B it is 80px / 590px.
- For 回收 2:1 layouts, top labels appear only when the user explicitly provides label text; when present, the label stays above the main title and does not become a third slogan.
- For `会员` B 2:1 layouts, the renderer-added member mark uses the inherited local-title color, is alpha-clean, is left-aligned with the local main-title box, and occupies the renderer-composed area above rather than becoming an AI-generated third slogan.
- For `会员` B 2:1 layouts, use 1125×562 as the typography reference: main-title font size is 80px and maximum visible width is 590px. The subtitle follows the global subtitle typography policy, shares the main-title left edge by default, and is not reduced to tiny type. The entire product group stays inside the right-side visual zone (`x=57%–94%`, `y=32%–84%`), remains compact and staggered, and does not encroach on the title-reading area or fill the whole right half.
- For `会员` B 2:1, fully apply the recycle B visual product QA: no people; `bg_recycle_service_graphic`; no support surface or one continuous support surface; and, with two or more physical product assets, the `combo_multi_recyclable` geometry. With exactly two products, keep reasonable near-equal visual weight without a forced main/support hierarchy; form stagger through front/back, high/low, offset bottom edges, size, angle, light perspective, or slight overlap; avoid aligned lower edges, equal-height side-by-side placement, card matrices, multiple separated podiums, and ordinary sale-product pairing. Judge this only as visual geometry—the membership poster must not introduce recycle coverage or service wording.
- For musical-instrument `S-level` routes, the main title may use exactly two flat colors, with only one continuous keyword or phrase taking the accent color; in 4:3, 16:9, or 2:1 landscape, the title group keeps visible left/right breathing space and does not horizontally fill the whole text zone.
- Decorative text, when provided, stays low-priority and does not become a third slogan.
- Low-priority editorial microcopy, corner labels, decorative English words, light numbering, or publication-style tiny text may appear without triggering QA when the selected route explicitly allows them, as long as they stay clearly secondary and do not replace the main title, subtitle, or user-provided decorative text. Exact year/date/season/issue claims should not appear unless the user explicitly provides them.

FAIL:

- Main title or subtitle is inaccurate, duplicated, rewritten, or not readable at first glance because text color lacks enough brightness or hue contrast against the current background.
- Low-priority editorial microcopy introduces unprovided year, date, season, issue, journal title, or other precise factual wording, even if the text is small.
- Main title and subtitle are crowded, with no clear visual air layer.
- In the `会员` B `2:1` local-composition route, a title-group subtitle is AI-generated, uses another font, has a font size or title gap that differs from the scaled policy, or is duplicated beside the local subtitle layer. In every other route, a title-group subtitle is missing, inaccurate, duplicated, or unreadable.
- Main title has heavy outline, heavy shadow, 3D, metallic, embossed, obvious top-bottom gradient fill, multi-color gradient fill, heavy commerce-template title effect, over-pressing font weight, heavy glow, or thick title-plate effect.
- Main title is placed inside a large bordered card, heavy title box, page-header band, big UI panel, or button-like container when not requested.
- Main title becomes visually clean but loses the selected business-line or category title personality, such as collectible-toy titles becoming hard-edged promotional Heiti or consumer-electronics titles losing modern display Songti / high-contrast Chinese Serif character.
- 1:1 square poster forces a two-line title group without user request.
- 4:3 or 16:9 landscape poster keeps a main title longer than 4 Chinese characters as a single long line, or any landscape poster breaks long titles in a way that damages complete words, punctuation, brand names, category names, numeric benefits, or fixed phrases.
- 2:1 landscape poster wraps before the active route's measured maximum width is exceeded, or keeps a title on one line after that maximum is exceeded.
- 回收 2:1 layout invents a top label when the user did not provide one, or makes a provided label more prominent than the main title.
- `会员` B 2:1 member mark is AI-generated, has a different color from the recorded main-title color, has a visible opaque background, is misaligned with the main-title group, or collides with title, subtitle, product, or high-detail background content.
- In a musical-instrument `S-level` route, the title uses more than two colors, scatters accent color across multiple separated words, or stretches so wide that the title group loses clear left/right breathing space in the landscape text area.

### 3.2 Business-Line Typography And Tone Layer

PASS:

- N 品类: visual style supports interest consumption, content aesthetics, category value, professional gear, lifestyle, or niche product operation.
- 潮玩: visual style has collectible-toy topic feeling, cute but controlled character, clear product hierarchy, and a title style with rounded, friendly, modern topic-lettering feel.
- 游戏: game character or role-group visual is treated as the main visual subject, with flat game-operation background for B, simple game background for A, or stronger game content atmosphere for S; the title style feels like fantasy high-contrast Chinese display type, slender elegant game-topic lettering, or ornate-but-restrained character-event title type.
- 消费电子: visual style is clean, professional, product-clear, light-tech or refined, with visible material quality, deliberate color, coherent lighting, and brand-advertising feel; the main title has a modern display Songti / high-contrast Chinese Serif feel when a title style is visible.
- 消费电子 B/A/S: lighting reads as strong contrast, with a clear bright-dark structure, coherent main light direction, visible product edge highlights, material reflection, and contact shadows.
- 消费电子 B 档: product display reads as minimal launch design with refined geometric support, material lighting, controlled highlights, and a clear product hero.
- 消费电子 A 档: scene display reads as `combo_ce_photo_lifestyle / 消费电子高级摄影生活方式` or `combo_ce_partial_people_use / 消费电子人物局部使用`, with product-centered focus.
- 消费电子 S 档: topic scene reads as `combo_ce_miniature_theme / 消费电子微缩主题场景` or `combo_ce_surreal_product_scene / 消费电子超现实商品场景`, with complete recognizable products.
- 回收: visual style reads as 简单、省心、值得信任, stable, light-toned, and restrained; the product or recyclable object is clear, the background inherits a small amount of product color, and the main title has a firm modern display-Heiti feel.

FAIL:

- N 品类 becomes a generic discount template with no category or content value.
- 潮玩 uses heavy promotional Heiti, red-yellow sale-template lettering, noisy discount-poster style, equal-weight product stuffing, unplanned random product scattering, or cute props that overpower the provided products.
- 游戏 uses generic ecommerce block type, heavy promotional Heiti, rough battle-damaged block type, mecha/geometric hard type, cheap gradient title, thick outline/shadow, noisy esports UI lettering, or treats the character visual as ordinary product cards instead of a game main visual.
- 消费电子 main title uses thick promotional Heiti, variety-show block lettering, cheap ecommerce template lettering, or heavy gradient block type instead of a modern display Songti / high-contrast Chinese Serif feel.
- 消费电子 becomes dirty neon tech, heavy sci-fi stage, over-complex glow, or cluttered high-contrast technology template without user request.
- 消费电子 B/A/S lighting is flat, evenly washed, weakly shadowed, or lacks a clear strong-contrast bright-dark structure.
- 回收 is rendered as ordinary sale, product hero selling, or price-first commerce poster without recycle service meaning.

### 3.3 Product Layer

PASS:

- User-provided product or main visual subject is visible, complete, and not replaced.
- Core appearance, category, color, structure, proportion, and key identifying features align with the user asset.
- When uploaded product images exist, the generated product remains recognizably the same product after direct comparison with the uploaded product image.
- For `cat_billiards_cue / 台球杆`, changed viewpoint is acceptable when the cue is still recognizably the same uploaded product: grip, ring details, black/gold color relationship, material pattern, and overall structure remain stable.
- For products with a device screen, viewfinder, display window, or inner-screen image in the user asset, the screen content remains part of product identity: main image content, subject silhouette, color relationship, and light-dark structure stay recognizable.
- When people use the product, changed viewpoint or pose is acceptable if product identity remains stable.
- Text, cards, decoration, people, hands, and background do not block key product features.
- For two or more uploaded products or distinct product subjects, each object remains independently recognizable after direct comparison with its corresponding source asset, and each object's passed layout attributes remain stable: size, position, angle, front/back hierarchy, crop boundary, and occlusion state do not drift without a task-driven reason.
- For `combo_multi_recyclable / 多品类回收组合`, multiple recyclable categories form a product-led staggered group by default. With exactly 2 products, both products have reasonable visual weight without a forced main/support hierarchy, and they show clear stagger through front/back, high/low, visibly offset bottom edges, size, angle, light perspective, or slight overlap. With 3 or more products, one main object may be larger and clearer while supporting objects have readable front/back, high/low, size, angle, or light-perspective variation. All objects still read as one recycle coverage group.
- For `biz_membership + cat_membership_day + B`, apply the preceding `combo_multi_recyclable` geometry as a visual parent rule. All products must read as one membership activity product group, not recycle coverage, and no recycle service wording may appear.
- For `game_multi_character_visual`, user-provided game characters or role illustrations remain separate role subjects in a role-group visual; light primary/support hierarchy is allowed, but each source character remains independently recognizable.
- For multiple collectible toys, one or a small group may be visually primary while supporting toys are arranged as companions with clear spacing, scale, height, or foreground/background rhythm.

FAIL:

- Product is cropped, blocked, replaced, or key identifying structure is missing.
- Product category, color, structure, proportion, or identifying features no longer match the user asset.
- After direct comparison with the uploaded product image, the generated product shows obvious mismatch in one strong identifying feature, or multiple ordinary identifying features drift together.
- For `cat_billiards_cue / 台球杆`, the cue is turned into another model/look when the shot angle changes: grip, ring, color blocking, pattern, or structural identity no longer reads as the same uploaded cue.
- The user asset has a clear screen, viewfinder, display window, or inner-screen image, but the generated result turns it into a black screen, empty screen, pure-color screen, unrelated pattern, or removes the main person, scene, color relationship, or light-dark structure from the original screen content.
- Generated image invents a different main product.
- Supporting props or decorative objects overpower the user-provided product.
- In a multi-product task, one object is repaired while another provided object drifts in size, position, angle, front/back hierarchy, crop boundary, or key identifying features; this still fails `商品层` even if the edited object improves.
- For `combo_multi_recyclable / 多品类回收组合`, products are forced into an equal-weight rigid card grid, isolated on separate platforms, scattered randomly, arranged with aligned lower edges or equal-height side-by-side placement when there are exactly 2 products, or arranged like ordinary sale merchandise rather than recycle coverage.
- For `biz_membership + cat_membership_day + B`, the inherited recycle B visual geometry is absent, or the image introduces recycle coverage/service wording, multiple separated podiums, a card matrix, aligned lower edges, equal-height side-by-side placement, or an ordinary sale-product pairing.
- Multiple user-provided game characters or role illustrations are fused into one new character, collapsed into a single body/look, dropped entirely, or reduced to generic background decoration instead of a coordinated role-group visual.
- Multiple collectible toys are averaged into the same weight, stuffed into cards without hierarchy, scattered randomly, or arranged so decorations become more important than the toys.

### 3.4 Information Module Layer

PASS:

- Benefit, selling-point, membership, recharge, exchange, and service information stays auxiliary.
- Default modules use short text, subtle separators, centered dots, low-presence information lines, and restrained spacing; consumer electronics does not use icon cards, benefit cards, selling-point cards, button-like modules, or obvious UI containers.
- Card/coupon or service-flow routes may use restrained card structures only when that route explicitly requires card semantics.
- Module text may include low-priority editorial microcopy or decorative labels when they remain clearly auxiliary and do not replace the main copy hierarchy.

FAIL:

- Information modules look like heavy solid buttons, large filled pills, heavy-shadow UI controls, bulky color blocks, or large solid icons.
- Modules overpower the main title or product.
- Subtitle is both repeated as a full sentence and split into modules.

### 3.5 Background Layer

PASS:

- Background, title, product, people, and information modules share one space logic or one design system.
- Realistic scenes, flat graphics, collage, cards, light-tech spaces, and product displays have shared color, light, perspective, shadow, edge transition, or graphic order.
- Background supports product recognition and title reading.
- When the selected background row defines candidate elements, count caps, or optional carriers, the visible background uses only the selected subset or a smaller compliant subset; auxiliary props stay restrained and do not turn the whole candidate pool into a checklist dump.
- For `bg_recycle_service_graphic / 回收_背景_弱中语境`, the result uses no visible platform, or at most one continuous tabletop/support surface; the product can also sit directly in a clean light space with soft contact shadow.
- For consumer electronics, when the product has a clear accent color, screen main color, brand color, or task-card-specified main color, the largest background color area comes from that color family as the main wall color, main gradient field, main halo area, or dominant space color.
- For consumer electronics with a clear product color source, black, white, and gray stay auxiliary for material highlights, shadows, stands, structural cuts, whitespace transitions, or information support, and do not become the largest background main color.
- Flat collage is acceptable when the collage system is unified and intentional.
- For collectible-toy topic scenes, pure flat card style, flat-background plus light 3D display, and clean cute 3D space can all pass when they match the normalized task card or supplement.
- Collectible-toy flat style uses a small number of flat element families; flat-background plus light 3D display uses a small number of flat elements plus one main support; clean cute 3D space keeps one coherent display language.

FAIL:

- Background regions form disconnected systems: hard seams, pasted-together areas, abrupt material changes, conflicting light, conflicting perspective, or conflicting depth.
- Title area looks like an independent white header, page header, or separate pasted band detached from product/person scene.
- Flat graphics, collage, card layers, realistic scenes, and product layers lack shared transition or common graphic order.
- Background is cluttered, too template-like, or steals attention from product and title.
- When the selected background row defines candidate elements, count caps, or optional carriers, the image dumps the full candidate pool, exceeds the selected/allowed count, or adds visible out-of-row props as background design.
- For `bg_recycle_service_graphic / 回收_背景_弱中语境`, the image shows two or more separated podiums, round platforms, stone blocks, trays, support blocks, or disconnected tabletops.
- For consumer electronics, the product has a clear accent color, screen main color, brand color, or task-card-specified main color, but the largest background color area still reads as black, white, gray, or cold neutral.
- For consumer electronics, the product color only appears as edge light, light strip, thin line, local glow, or small decoration, and does not become the dominant background color.
- For consumer electronics, the background main color is detached from the product color source, so the image still reads as a white-background, gray-background, black-background, or cold neutral poster.
- Collectible-toy flat style and 3D display style are mixed without shared color, shadow, edge treatment, or graphic rhythm.
- Collectible-toy output piles up too many flat elements, card types, stickers, torn paper, frames, podiums, gift boxes, props, or support objects so the image feels fragmented or the products lose hierarchy.

### 3.6 Composition Layer

PASS:

- Image follows the requested `1:1`, `4:3`, `16:9`, or `2:1` format when inspectable.
- Reading flow matches the selected format and composition.
- Main subject hierarchy is clear.
- Safe margins are respected.
- Text, product, people, and modules can overlap lightly when they still belong to the same image system and do not block each other.

FAIL:

- Wrong aspect ratio.
- Main subject is too small, too cropped, too edge-stuck, or visually unbalanced.
- Reading flow conflicts with the selected format.
- Overlap blocks title, subtitle, product identity, face, hands, or key module content.

### 3.7 Visual Expression Mode Layer

PASS:

- `稳定承托`: product is clear, scene is restrained, information is clean, and background does not distract.
- `场景表达`: scene, props, background extensions, people, or use context serve the theme and product value.
- `自动`: output follows the resolved visual direction in the normalized task card.
- For collectible toys, supplement cues 平面风 / 平面拼贴 route toward flat card or sticker-frame display; supplement cues 立体风 / 立体展示 route toward clean cute 3D space; if no such supplement exists and visual expression mode is `场景表达`, flat background plus light 3D topic display is preferred.
- For collectible toys, each resolved direction follows a limited-element approach: 平面风 keeps a unified flat language, 场景表达 combines a restrained flat topic background with light 3D display, and 立体风 keeps one clean cute 3D display space.
- For N-category collectible toys, A-level output visibly forms one journal-style paper-craft layout with a torn-paper title area, pale-green grid memo, top ring binder, paper tape, sparse stickers, and dotted doodle lines; S-level output visibly contains torn-paper edges integrated into the flat-background-plus-light-3D display. Their absence is a Visual Expression Mode Layer FAIL.
- For N-category game character visuals, B routes to a simple light-colored flat background plus game character main visual, using only a small amount of dotted texture, diagonal line texture, light UI linework, abstract symbols, or theme color blocks to create game identity; A routes to abstract light-shadow game atmosphere plus game main visual, and S routes to stronger game content atmosphere while keeping title readability.
- For 4:3, 16:9, and 2:1 N-category game character visuals, character or role-group weight sits on the right or right-leaning main visual area while the title remains readable on the left.

FAIL:

- `稳定承托` becomes noisy, over-scene, over-decorated, or weakens product recognition.
- `场景表达` has scene elements that do not serve theme, product value, selected category, or user supplement.
- Output ignores the resolved visual expression mode.
- Collectible-toy output ignores explicit supplement direction such as 平面风, 平面拼贴, 立体风, or 立体展示.
- Collectible-toy output treats A/B/C as an element checklist and generates all candidate elements in one image instead of selecting a coherent subset.
- N-category game B becomes a dark or complex immersive scene, battlefield, vehicle/smoke scene, deep perspective space, strong worldbuilding background, or visibly keeps/expands the complex background from the uploaded character image.
- N-category game A/S places the main character or role-group into the title reading area so the title and subject compete.
- N-category game character output mixes unrelated game-world types, such as fantasy characters with unrelated realistic shooter vehicles or unrelated characters, when they are not provided by the user.

### 3.8 People Participation And Scene Plausibility Layer

PASS:

- `人物参与=否`: no people, hands, wearing, operation, rider, player, or partial person relationship appears.
- `人物参与=是`: person visibly uses the user-provided product through wearing, holding, operating, riding, performing, trying, or in-use display.
- For `rel_multi_collection / 多商品集合` with `combo_cross_category / 跨品类集合` resolved to `人物参与=否 / 无人物陈列`, all provided product categories remain complete, recognizable, and product-led.
- People, hands, props, and scene objects follow basic visual and common-sense relationships.
- Creative scene extension is acceptable when it serves the theme and product value.

FAIL:

- `人物参与=否` but people, hands, wearing, operation, user, rider, player, or partial person relationship appears.
- `人物参与=是` but people are only atmosphere, distant figures, spectators, unrelated decorative people, or use another product instead of the user-provided product.
- `rel_multi_collection / 多商品集合` with `combo_cross_category / 跨品类集合` is resolved to `人物参与=否 / 无人物陈列`, but the image adds a person using one item and turns the other provided products into weak props, background decoration, missing items, or unrelated substitutes.
- People, hands, props, or scene objects distract from the subject, block key product features, or conflict with basic visual/common-sense relationships.

### 3.9 Fact And Business Semantics Layer

PASS:

- Business line meaning is correct.
- Product relation and combination match input asset count, visible asset type, and task card.
- N-category game character / game multi-character visuals, N-category card coupons, consumer-electronics game devices, physical products, and recycle meanings are routed to their correct business/category.

FAIL:

- Recycle is rendered as ordinary sale.
- Game character or character group is wrongly routed as product card when the task card requires main visual scene.
- Single product, multi-product, card coupon, or people-use relation conflicts with the normalized task card.

## 4. Targeted Retry Mapping

Use this mapping after a FAIL:

- Text Layer -> `Text Layer Correction` in `generation-execution.md`
- Business-Line Typography And Tone Layer -> `Business Tone Correction` in `generation-execution.md`
- Product Layer -> `Product Layer Correction` in `generation-execution.md`
- Information Module Layer -> `Information Module Correction` in `generation-execution.md`
- Background Layer -> `Background Layer Correction` in `generation-execution.md`
- Consumer-electronics background main-color failure -> `Background Main Color Correction` in `generation-execution.md`
- Composition Layer -> `Composition Layer Correction` in `generation-execution.md`
- Visual Expression Mode Layer -> `Composition Layer Correction` or `Background Layer Correction`, depending on the visible failure
- People Participation And Scene Plausibility Layer -> `People And Scene Plausibility Correction` in `generation-execution.md`
- Fact And Business Semantics Layer -> `Fact And Business Semantics Correction` in `generation-execution.md`

If multiple layers fail, choose the most blocking layer first. Prefer one targeted regeneration over a full prompt rewrite.
