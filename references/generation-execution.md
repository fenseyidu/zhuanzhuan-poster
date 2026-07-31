# Generation Execution v0.1

## Purpose

This is a poster image generation skill. Prompt assembly is only the control layer before generation. Default execution favors AI image generation.

Use this file when the user asks to:

- 生图
- 出图
- 做海报
- 生成头图
- 生成运营图
- 根据商品图生成海报

## Output Mode

Default to `generate_image` unless the user explicitly asks for prompt-only.

| User Request | output_mode |
|-|-|
| 做一张海报 | `generate_image` |
| 帮我生图 | `generate_image` |
| 生成头图 | `generate_image` |
| 先给我 Prompt | `prompt_only` |
| 只要提示词 | `prompt_only` |
| 先别生图 | `prompt_only` |

## Rendering Priority

For ordinary poster requests such as 生图、出图、做海报、生成头图, default to the available AI image generation capability.

Use HTML/CSS, JS, canvas, SVG, PPT, screenshot export, local composition, or editable web-poster workflows only when the user explicitly asks for that output method.

If the user does not specify an output method, do not choose JS/CSS or local rendering as the primary path.

## Prompt Roles

Use these prompt roles exactly:

| Name | Purpose | Submitted to image model |
|-|-|-|
| 最终 Prompt | Concise, natural-language, reusable generation prompt. | yes |
| 生图执行 Prompt | Long expanded review record with full reasoning, constraints, and trace. | no |
| 参数追踪 / 选用参数 | Stable IDs, Chinese names, called Chinese fragments, and assembly decisions. | no |
| 合并禁止项 / 禁止项追踪 | Selected `negative_rule_ids` and merged negative rules. | no |

The image generation tool must receive only `最终 Prompt`. Do not submit `生图执行 Prompt`, `选用参数`, or full merged negative rules to the image model.

## Execution Steps

1. Parse the minimum input contract.
2. Infer marketing type and linked IDs.
3. Assemble `最终 Prompt`.
4. If risky factual claims are missing a source, ask before generation.
5. Run Pre-output QA from `qa-flow.md`; fix once if it fails.
6. Default to the available AI image generation capability with `最终 Prompt` only.
7. Return the generated image.
8. Run Visual QA. If it fails and image generation is available, use one targeted correction prompt and regenerate once.
9. Create an output archive under `~/Documents/转转海报输出/` and save the generated image plus `review.md`.
10. Run lightweight Technical QA from `qa-flow.md`; fix file/archive issues once if possible.
11. Include the normalized task card, `最终 Prompt`, archive path, and QA notes in the user response.

## Output Archive

Every image generation run must create a separate archive folder under the user's Documents directory:

```text
~/Documents/转转海报输出/{YYYY-MM-DD}_{main_title}_{format}/
```

Do not create output folders in or beside:

```text
<skill-folder>/
<skill-parent>/
```

Archive contents:

```text
generated.png
review.md
```

If the image generation tool returns a different filename or path, copy or save the image into the archive folder when possible. If copying is not possible, record the original generated image path in `review.md`.

Use filesystem-safe folder names: keep Chinese title text when possible, replace slashes, colons, and whitespace runs with safe separators, and keep the output format suffix such as `1x1`, `4x3`, or `16x9`.

## Review Markdown

Write `review.md` as a card-style Markdown review file. Use `##` section headings and wrap dense field groups in fenced `text` code blocks so Markdown preview renders them as gray readable cards. Do not use Markdown tables for the review body.

Use this structure:

````markdown
# 头图 Skill 测试结果：{main_title} {format}

## 用户输入

```text
商品素材：
- {asset_path_or_image_id_1}
- {asset_path_or_image_id_2}

标签：{label_text_or_无}
主标题：{main_title}
副标题：{subtitle_or_无}
副标题本地排版：{subtitle_typography_policy_or_无}
标题风格参考：{会员 A/S 且补充要求包含特殊字时用内置毛笔参考}
主标题字形：{resolved_main_title_typeface}
装饰字：{decorative_text_or_无}
视觉方案档位：{visual_preset_level_or_自动}（可选：自动 / B / A / S）
高级测试字段：{visual_expression_mode_and_people_participation_if_explicit_or_无}
业务线：{business_line_name}
输出规格：{format}
补充要求：{supplement_or_无}
```

## 归一化任务卡

```text
业务线：{business_line_name}
业务线调性：{business_base_visual_tone}
品类：{category_name_or_inferred}
营销类型：{marketing_type_name}
视觉方案档位：{visual_preset_level_name_or_自动}
命中预设路径：{visual_preset_id_or_无} / {visual_preset_name_or_无}
视觉表达模式：{visual_expression_mode_name}
人物参与：{people_participation_name}
输出规格：{format_name}
商品关系：{product_relation_name}
商品组合：{product_combination_name}
构图：{composition_name}
背景：{background_recipe_name}
背景选用清单：{background_subset_summary_or_无}
视觉调制：{visual_modulation_summary}
乐器标题字形：{musical_instrument_title_typography_or_无}
台球杆摆放方式：{billiards_cue_arrangement_or_无}
台球杆标题字形：{billiards_title_typography_or_无}
骑行色板锚点：{bicycle_palette_anchor_or_无}
骑行选中色板：{bicycle_selected_palette_or_无}
骑行商品角度：{bicycle_product_angle_or_无}
骑行标题字形：{bicycle_title_typography_or_无}
标签：{label_text_or_无}
主标题：{main_title}
副标题：{subtitle_or_无}
副标题本地排版：{subtitle_typography_policy_or_无}
主标题字形：{resolved_main_title_typeface}
副标题本地排版：{subtitle_typography_policy_or_无}
装饰字：{decorative_text_or_无}
```

## 选用参数

```text
业务线：{business_line_id} / {business_line_name}
业务线基础调性：{business_base_visual_tone}
业务线视觉优先级：{business_visual_priority}
主标题字形：{resolved_main_title_typeface}
品类：{product_category_id} / {product_category_name_or_inferred}
营销类型：{marketing_type_id} / {marketing_type_name}
视觉方案档位：{visual_preset_id_or_auto} / {visual_preset_level_name_or_自动}
预设路径摘要：{expected_visual_result_or_无}
视觉表达模式：{visual_expression_mode_id_or_auto} / {visual_expression_mode_name}
人物参与：{people_participation_id_or_auto} / {people_participation_name}
输出规格：{format_layout_id} / {format_name}
商品关系：{product_relation_id} / {product_relation_name}
商品组合：{product_combination_id} / {product_combination_name}
构图镜头：{composition_camera_id} / {composition_name}
消费电子A/S组合方向：{ce_combination_direction_id_or_无} / {ce_combination_direction_name_or_无}
消费电子选中方向：{ce_active_expression_direction_or_无}
消费电子光影策略：{ce_lighting_strategy_or_无}
消费电子摄影调性：{ce_photography_modifiers_or_无}
预设背景候选：{preferred_background_ids_with_names_or_无}
背景方案：{background_recipe_id} / {background_recipe_name}
背景选用清单：{background_subset_summary_or_无}
乐器标题字形：{musical_instrument_title_typography_or_无}
台球杆摆放方式：{billiards_cue_arrangement_or_无}
台球杆标题字形：{billiards_title_typography_or_无}
骑行色板锚点：{bicycle_palette_anchor_or_无}
骑行选中色板：{bicycle_selected_palette_or_无}
骑行商品角度：{bicycle_product_angle_or_无}
骑行标题字形：{bicycle_title_typography_or_无}
路径校验：{通过_or_未通过_or_用户覆盖}；覆盖原因：{override_reason_or_无}
禁止项：{negative_rule_ids_with_rule_names}

调用中文：
- 业务线调性：{business_base_visual_tone}
- 业务线优先级：{business_visual_priority}
- 视觉方案档位：{visual_preset_called_summary_or_无}
- 视觉表达模式：{visual_expression_mode_summary}
- 人物参与：{people_participation_summary}
- 商品关系规则：{relation_hierarchy_rule}
- 商品组合陈列：{combination_arrangement_principle}
- 商品组合视觉语言：{combination_positive_visual_language}
- 构图表达：{composition_prompt_fragment}
- 乐器标题字形：{musical_instrument_title_typography_or_无}
- 台球杆标题字形：{billiards_title_typography_or_无}
- 消费电子摄影调性：{ce_photography_modifiers_called_or_无}
- 背景基础表达：{background_prompt_fragment}
- 背景视觉语言：{background_positive_visual_language}
- 背景连续性：{background_continuity_rules}
- 副标题本地排版：{subtitle_typography_trace_or_无}
```

## 最终 Prompt

```text
参与生图：是
用途：实际提交给图像模型的精简可复用提示词
提交内容：仅下方 Prompt 正文
```

```text
{final_prompt_submitted_to_image_model}
```

## 生图执行 Prompt（完整记录）

```text
参与生图：否
用途：仅作为复盘、排查和人工交接记录，不提交给图像模型
```

```text
{long_execution_prompt_for_review_only}
```

## 合并禁止项

```text
{deduplicated_negative_rule_ids_and_merged_negative_rules}
```

## 测试信息

```text
生成日期：{yyyy-mm-dd}
输出目录：{archive_folder}
生成图片：{generated_image_path}
模型输入：仅提交「最终 Prompt」
```

## 生图 QA 备注

```text
QA 结论：{通过_or_需定向重生_or_需人工后期}
背景主色 QA：{消费电子填写_通过_or_FAIL_or_不适用}
保留项：{what_to_keep}
问题分层：{failed_layers_or_无}
修正项：{failed_items_or_无}
定向修正 Prompt：{targeted_retry_prompt_or_无}
Technical QA：{file_path_ratio_archive_status}
```
````

`最终 Prompt` is the exact prompt submitted to the image model. Mark it as `参与生图：是` in `review.md`. `生图执行 Prompt` can be a longer expanded prompt for testing and review, but it is only a record. Mark it as `参与生图：否`; it must not be used as the image model input.

In `选用参数`, every selected stable ID must be written as `ID / 中文名`; never show an ID alone. Also include the main Chinese text fragments actually called from the CSV rows, especially business-line base visual tone, business-line visual priority, relation hierarchy, combination arrangement, product visual language, composition, background visual language, and background continuity. This makes the review file readable without reopening the CSV library.

## Product Assets

When image generation supports reference images, pass the uploaded product images as product references. For product-source wording, use `frag_product_visual_source` from `11_prompt_fragments.csv`.

When the image generation capability cannot use product references, state the limitation before or after generation:

```text
当前生成可能无法严格保留商品图细节，适合做视觉方向稿；关键商品保真需要继续用支持参考图的生图流程或后期合成。
```

## Post-Generation QA

After generation, inspect the image with `references/visual-qa.md`. Do not only say whether it looks good.

Use this structure in `review.md` and in user-facing QA replies:

```text
QA 结论：通过 / 需定向重生 / 需人工后期
背景主色 QA：消费电子填写 通过 / FAIL / 不适用
保留项：{what already works and should be kept}
问题分层：文字层 / 业务线字体与调性层 / 商品层 / 背景层 / 信息模块层 / 构图层 / 视觉表达模式层 / 人物参与与场景常识层 / 事实与业务语义层
修正项：{only the failed items}
定向修正 Prompt：{short correction prompt if regeneration is useful}
```

Use the PASS / FAIL checklist in `visual-qa.md` as the source of truth for visual judgment. If text is inaccurate, say so. Low-priority editorial microcopy, corner labels, decorative English words, light numbering, or publication-style tiny text should not trigger QA by themselves when the selected route explicitly allows them, but exact year/date/season/issue claims should still fail unless the user explicitly provides them. AI image generation may not render exact Chinese titles reliably; title-group subtitles are rendered locally only in registered `2:1` local-composition routes.

For `biz_consumer_electronics / 消费电子`, always write `背景主色 QA` in `review.md`. If the product has a clear screen main color, product accent color, brand color, or specified main color, but the largest background area still reads as black, white, gray, or cold neutral, mark `背景主色 QA：FAIL`, set the failed layer to `背景层`, and use `Background Main Color Correction / 背景主色定向修正` for targeted retry. If no clear product color source exists, write `背景主色 QA：不适用`.

QA decision:

- `通过`: only minor subjective preference issues remain; the image matches the prompt, business meaning, product visibility, text hierarchy, and fact constraints.
- `需定向重生`: one or more correctable layers fail, such as text effects, title spacing, product cropping, background discontinuity, wrong product relation, or visual clutter.
- `需人工后期`: image is directionally good but exact Chinese text, logo, product details, or small factual text cannot be reliably fixed through generation alone.

When QA fails and the task is image generation, write a local repair prompt instead of rewriting the full original prompt. The submitted targeted prompt has exactly three parts:

1. the concrete failure;
2. one direct correction action;
3. `其余内容不变。`

Use one or two short sentences only. Put passed-layer details, product-fidelity checks, negative rules, and any preservation rationale in `保留项` and QA notes—not in the prompt submitted to the image model. Do not restate the creative brief, name the failed layer redundantly, enumerate layout attributes, or issue several correction actions. The templates below are diagnosis aids; before submitting, compress them to this three-part form.

## Targeted Edit Input Contract

Default to a single-target local edit: submit the current generated image as the only image input, and state `以当前图为唯一编辑目标。` at the start of the correction prompt. Do not submit a mother-layout image, prior reference image, source product image, or style reference as an untyped additional input: an interface without explicit image roles can treat that image as a replacement source and overwrite already-correct products, text, or composition.

Add a second image only when the editing capability explicitly supports and labels its role as `composition reference`, `product reference`, or equivalent. In that case, the current generated image must be labeled `edit target`; the correction still changes only the failed item. If a product-identity repair needs the original product image but the capability cannot assign it a product-reference role, do not attempt a reference-image retry; mark it `需人工后期` or use a tool that supports role-specific references.

Example: `以当前图为唯一编辑目标。仅将手机和笔记本下移，使其恢复贴底裁切与可见高度，不替换或重排当前商品内容。其余内容不变。`

For measurable position, scale, crop, or slot-geometry repair, do not submit the diagnosis clause. Keep it in QA notes and submit one direct geometry action with a relative canvas target or reference-slot relation. Treat a combined scale-and-translate operation as one action:

```text
以当前图为唯一编辑目标。仅将{商品组}整体{缩小并下移}，使{主视觉}仅位于画面{下方 N% 的区域}，不替换、重排或回退当前商品内容。其余内容不变。
```

For `会员` A/S 2:1 ordinary-product slot foreground, do not use the loose scope `商品组整体`: it can accidentally scale coins and ribbons or redraw the front gift-box wall. When the repair is to reduce and lower the four products and the rear box body, use this exact prompt:

```text
以当前图为唯一编辑目标。仅将礼盒内的四件商品及其后方礼盒主体整体等比缩小并下移，使四件商品最高点落在画面高度约 70% 以下；金币、丝带、现有礼盒前侧边缘不参与编辑，四件商品的相对位置、遮挡关系和倾斜方向保持不变，前侧不得新增、扩展或露出礼盒壁。其余内容不变。
```

For `biz_consumer_electronics / 消费电子`, targeted regeneration must be especially narrow. Use this local-patch shape:

```text
{具体失败点}。{只写这一个失败点的直接动作}。其余内容不变。
```

If an AI image generation tool is available and the user asked to generate an image, use the targeted correction prompt to regenerate one version. For `会员` image generation, the membership retry policy overrides this default: automatically allow up to two targeted regenerations, QA after each, then stop and state the blocker if the second still fails; do not ask whether to continue. If regeneration is not available, output the targeted correction prompt for the user.

When the failed layer is `商品层` and the generated product does not match the uploaded product image, use the fixed short correction prompt below instead of rewriting the original creative brief or expanding the failure details into a long patch prompt. In multi-product tasks, check every object in QA, but submit only the specific product failure being corrected.

### Fixed Product Fidelity Correction

Use this exact prompt when product-fidelity QA fails after comparing the generated product with the uploaded product image:

```text
以当前图为唯一编辑目标。仅将{商品}修正为对应上传素材的外观、结构、颜色和关键识别特征。其余内容不变。
```

Targeted correction templates below are diagnosis references only. Before submitting any one of them to the image model, reduce it to `具体问题。唯一修改动作。其余内容不变。`.

Targeted correction templates:

### Text Layer Correction

Use when title/subtitle spacing, line break, perspective, heavy text effects, obvious gradient title fill, duplicate copy, or title carrier fails.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正文字层：{具体文字失败点}。修正方式：{只写需要调整的文字动作，例如修正文案、折行、字距行距、去掉厚重描边/投影/渐变/标题卡，或回到对应业务线标题气质}。不要重新设计其他已通过部分。
```

For title line-break failures, keep the correction narrow:

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正主标题：横版 4:3 / 16:9 中主标题超过 4 个汉字时按语义拆成两行；会员 A 的 2:1 主标题超过 908px（1125px 参考宽度）时保持单行并等比缩小字号；会员 S 的 2:1 主标题在其 580px 参考文字区内保持单行并等比缩小字号；会员 B 的 2:1 主标题超过 590px 时按语义拆成两行。需要折行时，每行保留完整词组、标点、品牌名、品类名、数字权益或固定短语。不要重新设计商品、背景、构图、色彩、光影、副标题、标签或装饰元素。
```

### Text Readability Correction

Use when the main title or subtitle is not readable at first glance because text color lacks enough brightness or hue contrast against the current background.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正文字可读性：{具体文字可读性失败点}。修正方式：{只调整文字颜色、阅读面或局部轻量承托，让主标题/副标题第一眼可读，文案保持不变}。不要重新设计其他已通过部分。
```

### Business Tone Correction

Use when the image fails the selected business-line typography or visual tone.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正业务线调性层：{具体调性失败点}。修正方式：{只写业务线或品类调性需要回到的方向，例如消费电子标题调回现代广告标题宋体或高对比中文 Serif 气质，或其他业务线对应调性}。不要重新设计其他已通过部分，不新增未提供事实。
```

### Consumer Electronics Lighting Contrast Correction

Use when `biz_consumer_electronics / 消费电子` B/A/S lighting is flat, evenly washed, weakly shadowed, or lacks a clear strong-contrast bright-dark structure.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正消费电子光影层：{具体光影失败点}。修正方式：把画面光影调整为强对比结构，建立明确主光方向、清晰明暗切面、产品边缘高光、材质反射和接触阴影。不要重新设计其他已通过部分。
```

### Product Layer Correction

Use when product identity, completeness, cropping, or occlusion fails.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。若商品的版式属性已通过，严格保留画布尺寸、整体构图、对应商品的位置、大小、角度、前后层次与裁切边界不变。仅修正商品层：{按商品对象列出具体商品失败点}。修正方式：{只修复对应对象的外观、结构、颜色、比例、关键识别特征、屏幕/取景画面、完整露出、裁切或遮挡中的失败项；商品身份保持稳定}。不要重新设计其他已通过部分。
```

When the product-layer failure is specifically a mismatch against the uploaded product image, do not expand into the generic template above. Use the fixed short correction prompt instead:

```text
请基于上一版重新生成。除商品身份修正外，其余画面保持上一版不变。严格保留画布尺寸、整体构图、已通过商品的位置、大小、角度、前后层次、裁切边界、标题、副标题、装饰字、背景和光影不变。仅修正商品层：将每一个商品严格参照对应上传商品图重新渲染，分别修正外观、结构、颜色、比例和关键识别特征；不要只修其中一个商品，不要改动已通过商品的版式属性。
```

### Background Layer Correction

Use when background is disconnected, cluttered, too template-like, or not supporting the product/title.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正背景层：{具体背景失败点}。修正方式：{只修复背景断裂、杂乱、模板化、光源/透视/阴影/色彩不统一等失败点}。不要重新设计其他已通过部分。
```

### Membership S Christmas Light-integration Correction

Use only when `biz_membership + cat_membership_day + S + 圣诞` has supplied products that look pasted in front of the light tree, are oversized, or use incompatible lighting. This is a combined product/background failure; do not use the generic product-identity or background template first.

```text
以当前图为唯一编辑目标。仅将右侧商品组等比缩小并收进光树下部内侧的香槟金体积光中，使商品上方、前侧和边缘共享树光，底部与金色颗粒地面连成连续反射和柔和接触阴影；商品身份及彼此相对关系保持不变。其余内容不变。
```

### Background Main Color Correction

Use when a consumer-electronics image has a clear product accent color, screen main color, brand color, or specified main color, but the largest background color area still reads as black, white, gray, or cold neutral.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正背景主色策略：{商品跳色/屏幕主色/品牌色/指定主色}没有成为背景最大面积主色。修正方式：把{指定色或提取色}升级为背景主色场或最大面积空间色，黑白灰只做辅助；不要只加灯带、边缘光或小面积点缀。不要重新设计其他已通过部分。
```

### Information Module Correction

Use when benefit, selling-point, membership, recharge, exchange, service, or subtitle modules are too heavy, too button-like, too icon-driven, or overpower the title/product.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正信息模块层：{具体信息模块失败点}。修正方式：{只把信息模块改为轻量文字信息层/细分隔线/中点分隔/低存在感信息行，删除图标卡、按钮式模块或厚重卡片感}。不要重新设计其他已通过部分，只使用用户提供事实。
```

### Composition Layer Correction

Use when ratio, reading flow, subject hierarchy, safe margin, or overlap fails.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正构图层：{具体构图失败点}。修正方式：{只调整比例、阅读流、主体层级、安全边距、主体位置或遮挡关系中的失败项}。不要重新设计其他已通过部分。
```

### People And Scene Plausibility Correction

Use when people, hands, props, or scene objects are visually implausible, distract from the subject, or do not serve the theme/product value.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正人物场景常识层：{具体人物/手部/道具/使用关系失败点}。修正方式：{只修复人物姿态、手部结构、使用关系或道具关系；人物参与为是时人物清晰使用用户商品}。不要重新设计其他已通过部分。
```

### Fact And Business Semantics Correction

Use when unprovided readable factual information, wrong business line, wrong product relation, or wrong game/recycle meaning appears.

```text
请基于上一版重新生成。除本次修正项外，其余画面保持上一版不变。仅修正事实和业务语义层：{具体事实或业务语义失败点}。修正方式：{只删除或改正未提供事实、错误业务线含义、错误商品关系或错误组合方式；主标题/副标题/装饰字使用用户提供内容}。不要重新设计其他已通过部分。
```
