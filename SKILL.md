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
标题风格参考：会员 A/S 2:1 可选，默认使用内置 MasterGo 毛笔标题参考 PNG
装饰字：可选，没有可不写
视觉方案档位：自动 / B / A / S（可选）
业务线：N 品类 / 消费电子 / 回收 / 会员
输出规格：1:1 / 4:3 / 16:9 / 2:1
补充要求：可选
```

Advanced test briefs may still include `视觉表达模式：自动 / 稳定承托 / 场景表达` and `人物参与：自动 / 否 / 是` to validate underlying routes before mapping them into a visual preset. When explicitly provided, these advanced test fields override the visual preset route, except when a forced no-people rule applies: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, must resolve `人物参与=否 / 无人物陈列`.

Infer marketing type from the main title, subtitle, product images, business line, optional visual preset, optional advanced test fields, and optional supplement. Use the business line as the parent visual tone, then link marketing type to product relation, product combination, composition, background recipe, positive prompt fragments, and centralized negative rule IDs.

Default output behavior:

- If the user asks to `生图`, `出图`, `做海报`, `生成头图`, or otherwise create the poster, assemble the final prompt and default to the available AI image generation capability with that prompt only.
- For `会员` A/S 2:1 member-day heads, use the saved MasterGo title-free background master as the AI-base reference. Generate only the warm-gold background, lower product group, coins, small toy, perspective, lighting, and shadows; the title area must stay clean. Generate the exact main title in a separate title-only image task by treating `member-day-title-style-reference.png` as a reference-image text replacement, not an open-ended style-generation prompt: preserve the reference's brush treatment and replace only its visible title copy with the requested main title. Do not append style descriptors such as `厚重`、`流动`、`有力量`、`行书` that can alter the reference strokes. Require a transparent title PNG before composition. The compositor crops the PNG to its visible alpha, fixes its visible height to `template.json.title_layer.visible_height`, derives the width proportionally from the title's own alpha bounds, and centers it; never stretch the full source canvas or force the title to fill a fixed width. The current approved default is `visible_height=250` at `title_layer.box.y=360`. It then adds the member-day mark, date, rule badge, and bottom wave.
- For `会员` A/S 2:1 AI-base generation, append this restriction: `AI 底图中不要生成主标题、会员日标识、日期、副标题、规则按钮、规则文字、底部波浪；海报场景中不要新增人物、手部、礼盒、卡片、价格、折扣、排名、服务承诺、第三方会员卡；但上传商品自身的屏幕、取景器或显示窗中原有的人像、场景或界面属于商品外观，必须保留。`
- For `会员` A/S 2:1, check the AI base and title asset independently before final composition. A base failure only retries the lower product/coin image; a title failure only retries the title-only image. The final composition must still check title, products, and fixed layers together for collisions. `会员` B does not use this route.
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
- Read `references/membership-head-composition.md` when the task is a 会员 A/S 2:1 head image or changes its compositing contract.

Structured data lives in `assets/Prompt参数库_v0.1/data/`. Use CSV rows as the parameter source before inventing new categories. For consumer-electronics A/S preset routes, read the matched row in `13_visual_preset_paths.csv`, then resolve the concrete combination direction from `08_product_combinations.csv`.

## Workflow

1. Parse the user's brief into the v0.1 input contract.
2. If product images are attached, treat visible product appearance as the product source. Do not require brand, model, price, or parameters unless the user asks to show them. For 会员 A/S 2:1 heads, stop and ask the user to reduce the selection when more than four product assets are supplied; otherwise use `assets/membership-head-template/template.json` 的 `product_slots.slot_assignment` to map assets to slots by silhouette shape and product hierarchy, then perform local image-to-image replacement. An explicit user slot mapping takes precedence; upload order is only a tiebreak when shape and hierarchy cannot distinguish assets. The member-day master remains the edit target and the original product-group composition stays locked.
3. Infer missing business line, product category, game visual asset type, visual preset, visual expression mode, people participation, and marketing type when confidence is high. Ask one concise question only when a missing choice changes business meaning or risk.
4. Normalize inferred values to stable IDs from the CSV parameter library.
5. Read `base_visual_tone` and `visual_priority` from the selected business line. If a visual preset level is provided and matched in `13_visual_preset_paths.csv`, expand it into internal route factors, preferred background IDs, and expected result before resolving visual expression mode and people participation. After the initial expansion, apply forced no-people overrides before selecting product combination and writing the final prompt: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, must resolve `人物参与=否 / 无人物陈列` even if the user explicitly provides `人物参与=是`. For matched consumer-electronics presets, select the background recipe from that row's `preferred_background_ids` unless explicit user supplement, advanced test fields, or a safety conflict requires an override; record the override reason. For consumer-electronics A/S routes, resolve and record one concrete combination direction from `08_product_combinations.csv`; for consumer-electronics B/A/S routes, also choose and record the active expression direction and lighting strategy before writing the final prompt. Then select linked product relation, product combination, format layout, composition camera, and background recipe.
   For `biz_n_category + cat_collectible_toy`, matched `A` routes use a journal-style paper-craft collage: a torn-paper title area, a pale-green grid memo, a top ring binder, a small piece of paper tape, sparse stickers, and dotted doodle lines. Matched `S` routes must visibly include torn-paper edges alongside the light 3D display. Treat these as fixed selected elements, not optional candidates.
6. Build visual language by inheritance and modulation: business-line tone first, then category meaning, marketing strength, visual expression mode, people participation, product hierarchy, product arrangement, composition energy, and background carrier.
7. Read corresponding `prompt_fragment`, relation `hierarchy_rule`, combination `arrangement_principle`, positive visual language, background continuity rules, and `negative_rule_ids`.
8. Assemble the final prompt as a concise natural-language generation prompt. This is the only prompt submitted to the image generation model.
9. Resolve `negative_rule_ids` through `12_negative_rules.csv`, deduplicate them, and compress only the essential constraints into the final prompt.
10. Run Pre-output QA from `references/qa-flow.md`. If it fails, fix the prompt once before output or generation.
11. Decide output mode: image generation by default, prompt-only only when explicitly requested.
12. For image generation, default to the available AI image generation capability using only the final prompt and product assets when supported.
13. For every `会员` A/S 2:1 run, first check the title-free AI base against the lower product/coin region and slots. Then check the title-only PNG for exact copy, usable transparency, brush-style approval, fit inside `title_layer.box`, and no mark/date collision. Only then invoke the compositor with `--title-asset`; perform one final collision check on the completed image. For other image-generation tasks, run Visual QA from `references/qa-flow.md` and `references/visual-qa.md`, then use the targeted correction templates in `references/generation-execution.md`. Before submitting any targeted retry, use the current generated image as the sole untyped image input, scope the prompt to the single failed problem and one direct correction action, and end with `其余内容不变`; do not submit long preservation lists or a rewritten creative brief. If it fails and image generation is available, use one targeted correction prompt and regenerate once.
14. Create an external test-case folder under the skill folder's parent directory, named `zhuanzhuan-poster-prompt-test-cases/`, and save the generated image plus a review Markdown file.
15. Run lightweight Technical QA from `references/qa-flow.md` for file existence, archive location, openability, and inspectable aspect ratio. Do not use a script by default.
16. In the card-style review Markdown file, include the final prompt, selected parameters with Chinese names and called Chinese fragments, merged negative rules, optional long execution prompt for review only, source asset paths, generated image path, and image QA notes.

## Human vs Agent Responsibilities

Humans provide the minimum facts:

- product images, paths, or product IDs
- optional label text, only when they want a top label above the main title; for 回收 2:1 layouts it should keep a light capsule outline style and use the same text size as the subtitle
- main title
- subtitle, or `无`
- optional title-style reference PNG for 会员 A/S 2:1; otherwise use the bundled MasterGo title reference
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

Every image generation run must create a separate folder outside the skill folder:

```text
<skill-parent>/zhuanzhuan-poster-prompt-test-cases/{YYYY-MM-DD}_{main_title}_{format}/
```

Save the generated image and `review.md` there. Keep test archives outside `zhuanzhuan-poster-prompt/` so test outputs do not pollute the skill context.

## Guardrails

- Do not invent prices, discounts, subsidies, rankings, model names, dates, or service promises.
- Do not change visible product identity, structure, color, brand marks, or key appearance unless the user explicitly allows it.
- Do not make recycle posters look like ordinary product sale posters.
- Do not let background, decoration, or cards obscure the product or title area.
- If exact text rendering is critical, state that the prompt should preserve the exact title and subtitle and that final text may need design QA or post-editing.
- QA stays lightweight: do not create standalone QA reports unless the user asks. PASS continues to the next step; FAIL defaults to one targeted retry; if the retry still fails, state the blocker.
- 定向重生默认采用“单目标局部编辑”：当前生成图是唯一编辑目标。只有当编辑能力能显式标记 `edit target`、`composition reference`、`product reference` 等角色时，才可附加参考图；不能标记角色时，禁止把母版、上一轮参考图或原商品图作为未标注的额外输入，以免模型回退、替换或重排已通过内容。提示词默认只写三件事：`编辑范围。唯一修改动作。其余内容不变。` 定位、缩放、裁切或固定槽位关系漂移时，失败诊断只写入 QA 备注，不提交给模型；将一条带可测量目标的几何变换视为唯一修改动作。例如：`以当前图为唯一编辑目标。仅将商品组整体缩小并下移，使主视觉仅位于画面下方 28% 的区域（从画面高度 72% 至底边），不替换、重排或回退当前商品内容。其余内容不变。` 不要在提交提示词中罗列无关的保留项，也不要先写“商品组当前过高过大”等问题描述；保留项和失败原因只记录在 QA 备注中。商品身份必须依赖外部素材才能修正时，若工具不能显式传递商品参考角色，应停止该定向重生并报告需要支持角色化参考的编辑工具或人工后期。
- 对 `会员` A/S 2:1，标题和下方商品组不再由同一次 AI 生图承担。标题专用 PNG 与商品底图分别通过 QA 后，才可进行固定层合成；标题 PNG 必须按可见 alpha 内容裁切后等比缩放并居中，禁止按整张输入画布强制拉伸至标题框，避免笔画压扁或拉宽。标题问题只重生标题图，商品区问题只重生当前商品底图。最终若标题、商品或固定层发生碰撞，归为“合成碰撞失败”。
- After image generation, check whether the result appears to match the business line, product visibility, title area, format, visual expression mode, people participation, and visual cleanliness. If the image generation tool cannot preserve exact text or product identity, report that limitation and recommend post-editing or another iteration.
