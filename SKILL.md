---
name: zhuanzhuan-poster-prompt
description: Generate Zhuanzhuan AI operation poster images or assemble generation-ready prompts across N-category, consumer electronics, and recycle business lines. Use when the user provides product images or product IDs plus a main title, subtitle, business line, and format, and asks Codex to generate a poster/head image, infer marketing type, choose product combination, composition, background, negative rules, or assemble the final image-generation prompt.
---

# Zhuanzhuan Poster Prompt

## Core Goal

Turn a small human brief into a structured, business-safe AI poster image. The prompt assembly is an intermediate step; when the user asks to make, generate, or output a poster image, do not stop at the prompt.

Default v0.1 input is intentionally short:

```text
商品素材：拖入图片 / 本地图片路径 / 商品库 ID
标签：可选，仅用户明确提供时使用
主标题：
副标题：没有就写“无”
标题字形：会员 A 默认思源宋体 SC Heavy；会员 S 的文字样式以对应 MasterGo renderer 为准；会员 B 使用现代标题黑体；仅当会员 A 的补充要求包含“特殊字”时，主标题使用内置毛笔参考图字形
装饰字：可选，没有可不写
视觉方案档位：自动 / B / A / S（可选）
会员节点：仅会员 S 使用，可选填圣诞 / 中秋；未填写时按主标题、再按补充要求中的明确节点词识别，仍不明确才询问
业务线：N 品类 / 消费电子 / 回收 / 会员
输出规格：1:1 / 4:3 / 16:9 / 2:1
补充要求：可选
```

Advanced test briefs may still include `视觉表达模式：自动 / 稳定承托 / 场景表达` and `人物参与：自动 / 否 / 是` to validate underlying routes before mapping them into a visual preset. When explicitly provided, these advanced test fields override the visual preset route, except when a forced no-people rule applies: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, must resolve `人物参与=否 / 无人物陈列`.

## Main-title Typography Rule

Apply this rule after all category typography cues.

- For `会员` A, render the entire main title in `assets/membership-head-template/fonts/SourceHanSerifSC-Heavy.otf` (`思源宋体 SC Heavy`).
- Only when a `会员` A `补充要求` explicitly contains the exact trigger `特殊字`, render the entire main title in the title style of `assets/membership-head-template/member-day-title-style-reference.png`.
- For `会员` S, use the selected 节点背景和商品组合；在底图通过视觉检查后，使用 `membership_s_renderer.py` 按 MasterGo 146:0998 排版调用方传入的主标题和副标题，并添加完整本地会员标识。两段文字共用 580px 参考文字区；主标题始终单行，超宽时等比缩小字号适配，副标题超宽时折行并水平居中。主标题仅在包含 X/x/× 且两侧都有文字时按“左文案 × 右文案”布局，左右标题同样保持单行并按较宽一侧缩小共同字号；否则原样渲染且不添加 ×。整组随副标题行数变化但始终垂直居中。节点仅决定背景路线，绝不预填或改写标题文案，也绝不沿用 A 的标题资产或固定层。
- For `会员` B, inherit the recycle B visual route and use a front-facing, flat, solid-color modern display Heiti with firm, heavy, stable strokes.
- Never apply the trigger to only part of the main title. Subtitle, label text, and decorative text keep their own typography rules.
- For `会员` A `2:1`, `template.json.title_layer.layout` is the default-title source of truth: at a 1125px-wide reference canvas, use 110px title size and 908px maximum visible width. Keep the title on one line; if it exceeds that width, proportionally reduce the title size to fit and never decide from product-area pressure or subjective readability. When `补充要求` contains `特殊字`, instead use `template.json.title_layer.special_title_layout`: crop to visible alpha, scale to exactly 268px visible height on the 2250px output canvas, ignore width limits, and preserve proportions. For `会员` B `2:1`, use `assets/text-layouts/membership/b-2x1.json`: 80px title size and 590px maximum width at the same reference width; only this route wraps an over-width title at a semantic boundary.

## 2:1 Subtitle Typography Rule

Apply this rule only to `会员` B `2:1` outputs when the user supplies a non-empty subtitle that remains in the title group. Other routes render the subtitle directly in the AI image unless their own composition contract says otherwise.

- `assets/subtitle-typography.json` is the single source of truth: its bundled Alibaba PuHuiTi Regular font is 40px at a 1125px-wide reference canvas, and it also defines the title gap.
- Scale the subtitle font size and title gap by `actual_canvas_width / 1125`; do not use a canvas-height percentage or maintain separate business-line subtitle sizes.
- `会员` B `2:1` generates a poster base without the main title and subtitle, then uses `assets/text_layout_renderer.py --profile membership-b-2x1`; `membership_head_renderer.py --mode membership-b` adds the member mark above the local title. `会员` A `2:1` keeps its separate transparent-title-asset plus fixed-layer compositor route. `会员` S uses `membership_s_renderer.py` with the registered `membership-s-2x1` profile.
- `会员` B `2:1` treats the member mark, main title, and non-empty subtitle as one vertically centered group. At the 2250px-wide final canvas, the visible member-mark-to-title gap and visible title-to-subtitle gap are both 62px (31px at the 1125px reference width). Keep these adjacent visible gaps when the main title wraps; recalculate the whole group height and center it rather than anchoring any one text line. The local renderer wraps an over-width Chinese title at provided whitespace or punctuation first, then falls back to character boundaries when no semantic boundary is available.
- For all other routes, submit the exact subtitle to the image model as part of the title group.
- For `2:1` local-composition routes, record the policy path, final font size, visible box, color, and title gap in `review.md`.

Infer marketing type from the main title, subtitle, product images, business line, optional visual preset, optional advanced test fields, and optional supplement. Use the business line as the parent visual tone, then link marketing type to product relation, product combination, composition, background recipe, positive prompt fragments, and centralized negative rule IDs.

Default output behavior:

- If the user asks to `生图`, `出图`, `做海报`, `生成头图`, or otherwise create the poster, assemble the final prompt and default to the available AI image generation capability with that prompt only.
- For `会员` A 2:1 member-day heads, use the saved MasterGo title-free background master as the AI-base reference. Resolve the lower foreground through `combo_membership_day_visual`: with no product asset, directly use gift boxes, ribbons, and coins; with one visibly gift-box asset, replace the default gift boxes; with other 1-4 product assets, use `template.json.product_slots` inside-box slots. The exact AI-base wording comes only from `references/prompt-assembly.md`. Create the exact main title as a separate transparent title-only PNG: use `title_asset_renderer.py` with the bundled `SourceHanSerifSC-Heavy.otf` by default; only when `补充要求` contains `特殊字`, use `member-day-title-style-reference.png` as a reference-image text replacement and invoke `membership_head_renderer.py --special-title`. The compositor crops the PNG to its visible alpha, fits a default title proportionally inside `template.json.title_layer.visible_height` and `max_visible_width`, and centers it; a `特殊字` title instead uses the fixed 268px visible height without a width limit. Never stretch the full source canvas or force the title to fill a fixed width. The current approved default A reference values are 110px / 908px at 1125px canvas width. It then adds the member-day mark, date, rule badge, and bottom wave.
- For `会员` S 2:1, look up `membership-s-2x1.json.image_to_image_references` by the selected node. When a node has a registered reference, use it as the AI-base edit target and preserve its reading field and theme focus. With zero product assets, apply `combo_membership_seasonal_gift`; with 1–4 product assets, apply the selected S product combination. If the selected node has no registered reference, stop and request that node's image-to-image reference. The current 圣诞 reference is `source/membership-s-christmas-background-master.png`; it is not interchangeable with A's master. For the 圣诞 product branch, the product group must be a compact focus enclosed by the lower inner volume of the light tree: it shares the tree's soft champagne-gold top/front light and selective rim light, then joins the golden particle ground through a continuous warm reflection and soft contact shadow. Do not let it become an oversized independent studio cutout in front of the light tree. The image model does not draw the logo, main title, or subtitle; use `membership_s_renderer.py` afterwards, which keeps the main title on one line by shrinking it to fit the registered text region.
- For `会员` A 2:1, check the AI base and title asset independently before final composition. If the first AI base is not exactly 2:1, pass it directly to the renderer: it cover-scales and crops to the 2250×1125 template (horizontal center, vertical bottom anchor to preserve the lower foreground). Do not trigger AI regeneration for an aspect-ratio mismatch alone; only retry a base for a remaining foreground, slot, or collision failure after composition. An A title failure only retries the title-only image. Unless the user explicitly requests another color, A's title, member-day mark, and date all use the bundled MasterGo reference color `#7E4504`; do not auto-switch their colors by local contrast. The date/subtitle layer follows the global subtitle typography policy. The final composition must still check title, products, and fixed layers together for collisions. For `会员` S 2:1, validate the AI base before text composition: for 圣诞 with supplied products, require a compact group inside the lower inner light-tree volume, shared warm top/front/rim lighting, and one continuous gold reflection plus soft contact shadow at its base. Treat a product group that is too large, sits in front of the beam, has cutout-like hard edges, or uses a separate studio light as an AI-base failure. Then call `membership_s_renderer.py` with exact `--title` and `--subtitle`; both use the same 580px reference text region, the main title remains single-line by proportionally shrinking its font when needed, and the subtitle may wrap. Keep the logo/title/subtitle group vertically centered. Its shared logo/text color is background-adaptive. `会员` B does not use either route. For `会员` B 2:1, generate the same poster base as recycle B: omit only the main title and subtitle, while retaining all visible source-product text and screen content. Apply the route-owned 60% left text-reading / 40% right main-visual composition rule from `references/prompt-assembly.md`. Run `text_layout_renderer.py --profile membership-b-2x1 --trace-output <title-layout.json>`, then call `membership_head_renderer.py --mode membership-b --title-layout <title-layout.json>` to add `member-b-brand.png` above and left-aligned to the local title.
- `会员` B keeps its modern display-Heiti title treatment and local subtitle policy.
- Use HTML/CSS, JS, canvas, local composition, or editable web-poster workflows only when the user explicitly asks for that output method.
- If the user explicitly asks for `Prompt`, `提示词`, `只要文案`, or `先别生图`, output the prompt only.
- If unclear, default to image generation because this skill's final purpose is poster image generation.

## Reference Loading

Load only the files needed for the task:

- Read `references/input-contract.md` when the brief is missing fields, includes uploaded product images, or may need fact confirmation.
- Read `references/agent-workflow.md` when assembling a poster prompt end to end.
- Read `references/field-taxonomy.md` when changing or checking CSV fields and stable IDs.
- Read `references/prompt-assembly.md` when writing the final prompt and review output format.
- Read `references/generation-execution.md` when the user wants a generated image, not just the prompt.
- Read `references/qa-flow.md` before prompt-only output or image generation to run Pre-output QA, and after image generation to schedule Visual QA and Technical QA.
- Read `references/visual-qa.md` after image generation to judge the generated poster by visual layer and decide whether targeted regeneration is required.
- Read `references/business-rules.md` when the task involves business-line boundaries, recycle semantics, prices, model names, rankings, or service promises.
- Read `references/membership-head-composition.md` when the task is a 会员 A 2:1 head image or changes its compositing contract. For 会员 S, read `references/prompt-assembly.md`, the selected background/combination rows, and `assets/membership-head-template/profiles/membership-s-2x1.json`.

Structured data lives in `assets/Prompt参数库_v0.1/data/`. Use CSV rows as the parameter source before inventing new categories. For consumer-electronics A/S preset routes, read the matched row in `13_visual_preset_paths.csv`, then resolve the concrete combination direction from `08_product_combinations.csv`.

Read `assets/subtitle-typography.json` for the `会员` B 2:1 local title-group route; it is the sole source for subtitle font, reference size, and title gap.

Read `assets/text-layouts/registry.json` before any local title/subtitle composition to select the route-owned pipeline; do not infer a renderer from a business line or reuse another route's layout profile.

## Workflow

1. Parse the user's brief into the v0.1 input contract.
2. If product images are attached, treat visible product appearance as the product source. Do not require brand, model, price, or parameters unless the user asks to show them. For 会员 A/S 2:1 heads, stop and ask the user to reduce the selection when more than four product assets are supplied. For A, a single visibly gift-box asset replaces the default direct gift foreground; other product assets use `assets/membership-head-template/template.json` 的 `product_slots.slot_assignment` to map assets to slots by silhouette shape and product hierarchy, then perform local image-to-image replacement. For S, zero product assets use `combo_membership_seasonal_gift` with the selected node reference as its image-to-image base; with 1-4 assets, resolve the common product relation before selecting a reusable product combination and use the same node reference for image-to-image. A selected S node with no registered reference must request one. S never uses A slots or the member-day master.
3. Infer missing business line, product category, game visual asset type, visual preset, visual expression mode, people participation, and marketing type when confidence is high. Ask one concise question only when a missing choice changes business meaning or risk.
4. Normalize inferred values to stable IDs from the CSV parameter library.
5. Read `base_visual_tone` and `visual_priority` from the selected business line. If a visual preset level is provided and matched in `13_visual_preset_paths.csv`, expand it into internal route factors, preferred background IDs, and expected result before resolving visual expression mode and people participation. After the initial expansion, apply forced no-people overrides before selecting product combination and writing the final prompt: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, must resolve `人物参与=否 / 无人物陈列` even if the user explicitly provides `人物参与=是`. For matched consumer-electronics presets, select the background recipe from that row's `preferred_background_ids` unless explicit user supplement, advanced test fields, or a safety conflict requires an override; record the override reason. For consumer-electronics A/S routes, resolve and record one concrete combination direction from `08_product_combinations.csv`; for consumer-electronics B/A/S routes, also choose and record the active expression direction and lighting strategy before writing the final prompt. Then select linked product relation, product combination, format layout, composition camera, and background recipe.
   For `biz_n_category + cat_collectible_toy`, matched `A` routes use a journal-style paper-craft collage: a torn-paper title area, a pale-green grid memo, a top ring binder, a small piece of paper tape, sparse stickers, and dotted doodle lines. Matched `S` routes must visibly include torn-paper edges alongside the light 3D display. Treat these as fixed selected elements, not optional candidates.
6. Build visual language by inheritance and modulation: business-line tone first, then category meaning, marketing strength, visual expression mode, people participation, product hierarchy, product arrangement, composition energy, and background carrier.
7. Read corresponding `prompt_fragment`, relation `hierarchy_rule`, combination `arrangement_principle`, positive visual language, background continuity rules, and `negative_rule_ids`.
8. Assemble the final prompt as a concise natural-language generation prompt. This is the only prompt submitted to the image generation model. When a user-provided product asset contains a visible screen, text, or brand mark, include this hard constraint in the final prompt: `不生成额外海报文案、会员标识或水印；用户商品上原有的屏幕画面、可见文字与品牌标记均视为商品身份，必须完整保留，不得替换为抽象图案、空白或无关界面。`
9. Resolve `negative_rule_ids` through `12_negative_rules.csv`, deduplicate them, and compress only the essential constraints into the final prompt.
10. Run Pre-output QA from `references/qa-flow.md`. If it fails, fix the prompt once before output or generation.
11. Decide output mode: image generation by default, prompt-only only when explicitly requested.
12. For image generation, default to the available AI image generation capability using only the final prompt and product assets when supported.
13. For every `会员` A 2:1 run, first check the title-free AI base against the selected lower-foreground branch; check slots only for ordinary-product runs. Then check the title-only PNG for exact copy, usable transparency, selected title style (default 思源宋体 SC Heavy; `特殊字` only uses the brush reference), fit inside `title_layer.box`, and no mark/date collision. Only then invoke the compositor with `--title-asset`; perform one final collision check on the completed image. For `会员` S, validate the selected node background, zero-product gift branch or resolved product relation, left reading area, right theme focus, and shared theme light after image-to-image. For 圣诞 with supplied products, explicitly judge the compact scale, light-tree containment, shared warm light, gold ground reflection, and soft contact shadow before text composition; a pasted, oversized, or separately lit product group requires the dedicated light-integration retry. Then run `membership_s_renderer.py` and check the logo/title/subtitle layout and adaptive color contrast. For `会员` B 2:1, use the inherited recycle B visual product route and a poster base that omits only the main title and subtitle. Run `text_layout_renderer.py --profile membership-b-2x1 --trace-output <title-layout.json>`, then invoke `membership_head_renderer.py --mode membership-b --title-layout <title-layout.json>`; verify that the member mark is above and left-aligned to the local title without collisions. For other image-generation tasks, run Visual QA from `references/qa-flow.md` and `references/visual-qa.md`, then use the targeted correction templates in `references/generation-execution.md`. Before submitting any targeted retry, use the current generated image as the sole untyped image input, scope the prompt to the single failed problem and one direct correction action, and end with `其余内容不变`; do not submit long preservation lists or a rewritten creative brief. If it fails and image generation is available, use one targeted correction prompt and regenerate once.
14. Create an output archive under `~/Documents/转转海报输出/`, and save the generated image plus a review Markdown file. Never create output folders in or beside the skill installation directory.
15. Run lightweight Technical QA from `references/qa-flow.md` for file existence, archive location, openability, and inspectable aspect ratio. Do not use a script by default.
16. In the card-style review Markdown file, include the final prompt, selected parameters with Chinese names and called Chinese fragments, merged negative rules, optional long execution prompt for review only, source asset paths, generated image path, and image QA notes.

## Membership B Logo Placement Override

For `会员` B 2:1, do not place any `预留标识区`、`会员标识区`、`占位块`、`左上留白` or similar instruction in the AI generation prompt. These phrases cause the model to draw an empty visual block. The renderer—not the AI—owns logo placement: measure the generated title's visual boundary and color, then place the 60px logo above the title with its left edge aligned to the title's measured left edge.

## Human vs Agent Responsibilities

Humans provide the minimum facts:

- product images, paths, or product IDs
- optional label text, only when they want a top label above the main title; for 回收 2:1 layouts it should keep a light capsule outline style and use the same text size as the subtitle
- main title
- subtitle, or `无`
- optional `特殊字` trigger in a `会员` A 补充要求; it switches the entire main title to the bundled MasterGo brush-title reference
- `会员节点`：仅会员 S 使用，填写圣诞或中秋
- optional decorative text, only when they want an atmosphere word or handwritten decorative word
- optional visual preset level: `自动`, `B`, `A`, or `S`
- optional advanced test visual expression mode: `自动`, `稳定承托`, or `场景表达`
- optional advanced test people participation: `自动`, `否`, or `是`
- business line: `N 品类`, `消费电子`, `回收`, or `会员`
- output format
- any real price, subsidy, ranking, model name, activity time, or service promise that must appear

The agent infers and links:

- marketing type
- product category when visible or obvious
- game visual asset type for game-related uploads
- visual preset path when a matching business line + category + B/A/S preset exists
- visual expression mode when absent, inferred as stable support or scene expression from title, product use relation, supplement, and business line
- people participation when absent, inferred as automatic permission, no people, or people allowed from title, product use value, visual expression mode, supplement, and visible assets
- product relation
- product combination
- product arrangement and hierarchy language
- composition camera
- background recipe
- background visual language and continuity
- marketing expression strength
- negative rule IDs and merged negative rules
- image generation execution when the user wants the poster image
- external test-case archive when image generation runs

## Prompt and Archive Contract

Use these names consistently:

- `最终 Prompt`: the concise, reusable natural-language prompt submitted to the image generation model.
- `生图执行 Prompt`: an optional long review prompt written only into the review Markdown file; never submit it to the image generation model.
- `参数追踪`: selected stable IDs, Chinese names, called Chinese fragments, and assembly decisions, for review only.
- `合并禁止项`: selected `negative_rule_ids` and merged negative rules, for review only.

Every image generation run must create a separate output archive under the user's Documents directory:

```text
~/Documents/转转海报输出/{YYYY-MM-DD}_{main_title}_{format}/
```

Save the generated image and `review.md` there. Do not create output folders in or beside `zhuanzhuan-poster-prompt/`, regardless of where the skill is installed.

## Guardrails

- Do not invent prices, discounts, subsidies, rankings, model names, dates, or service promises.
- Do not change visible product identity, structure, color, brand marks, or key appearance unless the user explicitly allows it.
- Do not make recycle posters look like ordinary product sale posters.
- Do not let background, decoration, or cards obscure the product or title area.
- If exact text rendering is critical, state that the prompt should preserve the exact title and subtitle and that final text may need design QA or post-editing.
- QA stays lightweight: do not create standalone QA reports unless the user asks. PASS continues to the next step; FAIL defaults to one targeted retry; if the retry still fails, state the blocker. For `会员` image generation, override this failure handling: when the output does not meet the applicable visual standard, automatically perform up to two targeted regenerations, running QA after each. Each retry uses the current failed generation as the sole edit target, changes only the currently failed item, and preserves previously passed content. If the second targeted regeneration still fails, stop, state the specific blocker, and do not ask whether to continue.
- 对会员 A 2:1 的商品与礼盒几何修正不得笼统写“商品组整体”，以免金币、丝带或前侧盒壁被误改；使用：`以当前图为唯一编辑目标。仅将礼盒内的四件商品及其后方礼盒主体整体等比缩小并下移，使四件商品最高点落在画面高度约 70% 以下；金币、丝带、现有礼盒前侧边缘不参与编辑，四件商品的相对位置、遮挡关系和倾斜方向保持不变，前侧不得新增、扩展或露出礼盒壁。其余内容不变。` 不要在提交提示词中罗列无关的保留项，也不要先写“商品组当前过高过大”等问题描述；保留项和失败原因只记录在 QA 备注中。
- 对 `会员` A 2:1，标题和下方前景不再由同一次 AI 生图承担。标题专用 PNG 与商品底图分别通过 QA 后，才可进行固定层合成；标题 PNG 必须按可见 alpha 内容裁切后等比缩放并居中，禁止按整张输入画布强制拉伸至标题框，避免笔画压扁或拉宽。标题问题只重生标题图，前景问题只重生当前商品底图。普通商品槽位分支进行几何定向重生时，须明确保留当前商品组的组合结构不变（槽位归属、左右关系、前后遮挡、主次层级、倾斜方向和与金币/礼盒的层次关系）；只允许整组缩放和位移。最终若标题、商品或固定层发生碰撞，归为“合成碰撞失败”。
- 对 `会员` S 圣诞 2:1 的商品光场融合失败，使用当前失败底图作为唯一编辑目标，定向修正商品组的尺度和光场关系；不要套用 A 的礼盒槽位、标题 PNG 或固定层规则。修正后必须再次检查商品是否被光树下部体积光包裹，并与金色地面反射和接触阴影连续相连。
- After image generation, check whether the result appears to match the business line, product visibility, title area, format, visual expression mode, people participation, and visual cleanliness. If the image generation tool cannot preserve exact text or product identity, report that limitation and recommend post-editing or another iteration.
