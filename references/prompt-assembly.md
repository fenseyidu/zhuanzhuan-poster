# Prompt Assembly v0.1

## Output Sections

When the user asks for prompt-only, output:

```text
归一化任务卡
最终 Prompt
禁止项
自检清单
```

In prompt-only mode, the `归一化任务卡` must still show user-facing input fields, including optional fields as `无` when empty:

```text
商品素材：{asset_path_or_image_id}
标签：{label_text_or_无}
主标题：{main_title}
副标题：{subtitle_or_无}
装饰字：{decorative_text_or_无}
视觉方案档位：{visual_preset_level_or_自动}（可选：自动 / B / A / S）
业务线：{business_line_name}
输出规格：{format}
补充要求：{supplement_or_无}
```

If the user is running route tests and explicitly provides advanced fields, include them after the default fields:

```text
高级测试字段：
视觉表达模式：{visual_expression_mode_or_自动}
人物参与：{people_participation_or_自动}
```

When the user asks for image generation, use `最终 Prompt` to generate the poster image, then output:

```text
生成图片
归一化任务卡
最终 Prompt
归档路径
生图 QA 备注
```

## Final Prompt Order

Assemble `最终 Prompt` as a concise natural-language paragraph similar to the review example format. It is the only prompt submitted to the image generation model.

The final prompt should read like a reusable generation prompt, not like a parameter table translated into prose. Avoid raw phrases such as `商品关系采用...`, `商品组合方式采用...`, `背景采用...` unless they naturally fit the sentence.

## Main-title Typography

Apply this rule after resolving category-specific typography. For `会员` A/S, write the entire main title as `思源宋体 SC Heavy（SourceHanSerifSC-Heavy.otf）`, with a front-facing, flat, solid-color layout. An A/S `补充要求` containing the exact phrase `特殊字` uses `member-day-title-style-reference.png` as the reference for the entire main-title glyph style. For `会员` B, write the entire main title as a modern display-Heiti treatment: front-facing, flat, solid-color, firm heavy strokes, and a stable center of gravity. Record the resolved title mode in review Markdown.

## 2:1 Subtitle Typography

For a non-empty title-group subtitle in the `会员` B `2:1` route, do not submit the subtitle text to the image model. Reserve its resolved subtitle area as clean background, then render the exact user copy after generation with the route-owned renderer and `assets/subtitle-typography.json`. The policy fixes Alibaba PuHuiTi Regular at 40px on a 1125px-wide reference canvas and scales by final canvas width. Place it below the measured or fixed main-title box, use the title's left edge by default, and record the final font size, color, visible box, and title gap in review Markdown. For every other route, submit the subtitle to the image model as part of the title group. When a route intentionally resolves the subtitle into separate information modules, do not also render a title-group subtitle.

## Visual Inheritance And Modulation

Build visual language through inheritance first, then modulation. Do not let a downstream row overwrite the business-line tone unless the user explicitly requests it.

```text
business line base_visual_tone
-> category meaning and visible product traits
-> marketing type intensity and information structure
-> visual preset path when provided and matched
-> visual expression mode as stable support or scene expression
-> people participation as automatic, no people, or people using product
-> product relation hierarchy
-> product combination arrangement
-> composition energy
-> background carrier and continuity
-> user supplement, when safe
```

Layer responsibilities:

- Business line sets the base tone: N 品类 is content-led and category-specific; 消费电子 is clean, professional, product-clear, light-tech, material-rich, and brand-advertising oriented, with both light spacious palettes and deep high-contrast palettes available; 回收 is trustworthy, service-led, safe, and stable.
- Category adds visible product traits and business-role cues, such as cycling gear value, musical practice, camera shooting value, office efficiency, game participation, or high-value recycle trust. Do not use category alone to decide sale vs recycle expression.
- Marketing type adjusts conversion strength, information density, and benefit carriers; it should not redefine the whole visual style by itself.
- Visual preset path maps user-facing B/A/S to a tested category route when available. It expands into internal route factors, preferred background IDs, and a short route summary, then the normal product relation, combination, composition, and background workflow continues.
- Visual expression mode routes the task toward stable product support or scene expression before selecting product combination. It can be provided by advanced test input, expanded from a visual preset, or inferred in automatic mode.
- People participation is a product presentation switch after visual expression mode and must be corrected after product relation/product combination are known. It controls whether people, hands, wearing, operation, or user interaction become part of the product combination; when set to yes, the person uses the user-provided product while product combination and composition decide the exact form. Any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, forces no people even when the user explicitly asks for people.
- Product relation and product combination decide product hierarchy and arrangement, not the overall aesthetic.
- Background recipe is the visual carrier. It must support the inherited tone, product, and title area rather than becoming an unrelated style scene.

Translate broad style words into stable visual variables. For example, translate `小红书感`, `杂志感`, or `高级感` into concrete visual language such as lifestyle scene, soft natural light, editorial spacing, grid order, restrained color, deep high-contrast lighting, screen glow, material reflection, shallow depth of field, geometric support, and low decoration density.

Include these ingredients in a compact flow:

1. poster visual concept
2. business scope and output ratio
3. inherited business-line tone and category semantic cues
4. visual preset path, if provided or matched
5. visual expression mode
6. people participation
7. product source and product identity preservation
8. product relation hierarchy
9. product combination arrangement principle
10. positive product-display visual language
11. composition camera
12. background recipe
13. background positive visual language and continuity rules
14. main title, subtitle, optional decorative text, and text hierarchy
15. category-specific product angle or title typography cue, when selected
16. marketing expression and information density
17. one compact essential quality sentence derived from selected rules, written as positive requirements

## Visual Preset Handling

Use `视觉方案档位` as the default user-facing route when provided. Do not expose raw preset IDs in the final prompt.

If a matching row exists in `13_visual_preset_paths.csv`, record the row in review Markdown and use its route factors before selecting product relation, product combination, composition, and final background. Match exact `business_line_id + category_id + preset_level` first; when no exact row exists, use `business_line_id + cat_all + preset_level` as the business-line general preset.

Use phrasing naturally, for example:

```text
视觉方案采用潮玩 A 档手帐纸艺专题路线：以撕纸标题区、浅绿网格便签、顶部圆环夹、纸胶带、少量贴纸和虚线涂鸦构成一张连续的温暖纸艺拼贴，商品以清晰白边切图进入便签区并按上传素材数量组织主次。
```

For `biz_n_category + cat_collectible_toy`, write these fixed preset details into the final prompt: A uses a torn-paper title area, pale-green grid memo, top ring binder, paper tape, sparse stickers, and dotted doodle lines as one continuous journal-style paper-craft layout; S must contain visible torn-paper edges integrated with the flat-background-plus-light-3D display.

## Membership B Prompt

When `business_line_id=biz_membership`, `category_id=cat_membership_day`, and preset level is `B`, use the normal final-prompt pipeline with the inherited stable-support visual route and the membership business tone. Do not use the A/S MasterGo base, title-only asset, fixed-layer compositor, or product-slot template.

For `format_id=fmt_landscape_2_1`, require a poster base without the main title and subtitle. This applies only to the title group: all visible text, icons, and screen content that belong to the uploaded products must remain unchanged. Do not mention a membership-mark area, reservation, placeholder, or extra upper-left whitespace in the final Prompt. After generation, run `text_layout_renderer.py --profile membership-b-2x1 --trace-output <title-layout.json>`, then let `membership_head_renderer.py --mode membership-b --title-layout <title-layout.json>` add `member-b-brand.png` above the local title. Do not ask the image model to draw, imitate, recolor, or regenerate the membership mark.

For `biz_membership` B in `fmt_landscape_2_1`, add these requirements to the final Prompt: `以 1125×562 的 2:1 画布为基准，海报底图不生成主标题和副标题；商品本体及其屏幕、机身、包装上的原有文字、图标和界面内容必须保留。左侧 60% 保持连续、干净的背景与完整文字阅读动线；主视觉商品群整体集中在右侧 40%（x=60%–100%）内，纵向错落陈列并保留画布边缘安全距离，不侵入左侧文字区域，不铺满主视觉区。`

For `biz_membership + cat_membership_day + B`, fully inherit the recycle B visual product route. With two or more physical product assets, use the visual geometry of `combo_multi_recyclable`: two products keep reasonable near-equal visual weight without a forced main/support hierarchy and are staggered through front/back, high/low, offset bottom edges, size, angle, light perspective, or slight overlap; three or more products may use one clearer main object. All products share one continuous light space, one light direction, and either no support surface or one continuous support surface; do not use a card matrix, multiple separated podiums, aligned bottom edges, equal-height side-by-side placement, or an ordinary sale-product pairing. Describe this in the final Prompt as a `会员活动多商品主视觉`, never as recycle coverage or recycle service; do not add recycle estimates, inspection, payment, service trust, or other recycle wording.

```bash
python3 assets/text_layout_renderer.py \
  --profile membership-b-2x1 \
  --base-image <generated-b-2-1-poster.png> \
  --title <main-title> \
  --subtitle <subtitle> \
  --output <title-group.png> \
  --trace-output <title-layout.json>

python3 assets/membership-head-template/membership_head_renderer.py \
  --mode membership-b \
  --base-image <title-group.png> \
  --title-layout <title-layout.json> \
  --output <final-poster.png>
```

## Membership A/S 2:1 Image-to-Image Prompt

When `business_line_id=biz_membership`, `category_id=cat_membership_day`, `format_id=fmt_landscape_2_1`, and preset level is `A` or `S`, run two distinct image tasks. The saved title-free MasterGo background master is the AI-base edit target. Create a separate transparent title-only asset: render with `SourceHanSerifSC-Heavy.otf` by default; only when `补充要求` contains `特殊字`, use the saved brush-title PNG as the typography reference. Do not use a title-and-product image as the base and do not erase a generated title afterwards.

Build the AI-base prompt from one shared block and exactly one lower-foreground block. Do not combine the direct gift foreground with the inside-box slot foreground.

```text
以输入的无标题会员日暖金母版为唯一编辑目标。保留原画布比例、连续暖金背景、下方前景贴底位置、金币、透视、光影与阴影；画面上方约 68% 呈现连续、干净、舒展的暖金文字阅读背景；商品主体、低矮打开的礼盒、金币与丝带以紧凑的贴底层叠组合呈现在下方约 32% 区域。AI 底图中不要生成主标题、会员日标识、日期、副标题、规则按钮、规则文字、底部波浪；海报场景中不要新增人物、手部、卡片、价格、折扣、排名、服务承诺、第三方会员卡。
```

Use one of these lower-foreground blocks:

| Supplied product assets | Lower-foreground block |
|-|-|
| 0 | `下方主视觉为 2-3 个礼盒、少量丝带和金币的直接贴底层叠组合，不使用外层礼盒容器、盒口、盒角或盒壁。以 1 个主礼盒和 1-2 个辅助礼盒形成居中、连续的前后层叠群组，礼盒尺寸和高度有变化、自然相互遮挡，不均匀铺满两侧边缘；金币与丝带仅作低量点缀，保持当前画面的整体色彩系统、透视、光影与阴影。` |
| 1, visibly a gift box | `下方主视觉沿用 2-3 个礼盒、少量丝带和金币的居中贴底层叠组合，不使用外层礼盒容器、盒口、盒角或盒壁；以上传礼盒素材替换主礼盒，并保留其外观、结构、颜色、材质和关键识别特征。` |
| 1-4, other products | `下方主视觉采用从礼盒内部向上展开的近景视角：镜头位于盒口上方，朝盒内轻微俯视。礼盒以低矮的打开式礼盒承托商品，盒壁仅在画面下缘露出。礼盒从画布底边自然延续，商品组在底边的盒内空间向上错落露出。画面呈现商品背后的盒口内沿、左右低位的局部盒角、盒内金币与丝带；前侧盒壁和盒底顺着画布下方延展，形成贴底的近景空间。礼盒的颜色、材质和光影跟随当前画面的整体色彩系统。首次 AI 底图生成时，礼盒开口及左右盒角整体约占画面宽度 75%，居中陈列，两侧保留呼吸空间，不贴画面边缘。下方固定槽位按以下“母版原对象 → 上传商品”逐项局部替换：{slot_replacement_map}；每件商品严格继承对应槽位的大小、位置、倾斜方向、三分之四视角、前后层级、可见重点和光影关系；{foreground_description}。` |
| more than 4 | Stop and ask the user to keep at most four products. |

When `补充要求` contains `特殊字`, the separate title-only task treats `member-day-title-style-reference.png` as a reference-image text-replacement target, rather than a typography mood reference. For the bundled reference, submit this prompt exactly, replacing only `{main_title}`:

```text
使用图1作为参考图，将图中的“狂欢开启 惊喜到周末”改为“{main_title}”。
标题必须完整、清晰、正视、横向单行，无其他文字、无标识、无日期、无商品、无装饰。
将标题置于完全纯色 #00FF00 绿色背景中央，背景只能是单一无纹理无阴影的绿色，便于后续抠图；标题本身不得使用绿色。
```

Without `特殊字`, render the exact main title from `assets/membership-head-template/fonts/SourceHanSerifSC-Heavy.otf` to a transparent PNG before composition. For a user-supplied title reference with `特殊字`, replace the first quoted string with the visible title copy in that reference. Do not add style descriptors such as `厚重`、`流动`、`有力量`、`行书`、`毛笔节奏`, because they make the model reinterpret and alter the reference strokes. Convert the brush-reference result to a transparent title PNG before composition. It is not submitted as another untyped image alongside an AI-base retry.

For the ordinary-product branch, build `{slot_replacement_map}` from `template.json.product_slots` in slot order, after applying `slot_assignment`. Each supplied asset must be written as `{reference_subject} 槽位替换为第 {actual_upload_order} 张{visible_product_description}`. When an asset has a visible screen, viewfinder, or display window, `visible_product_description` must also state that its original screen content is retained; this includes an original person, scene, or interface. The automatic mapping classifies the cut-out product silhouette and hierarchy: portrait products preferentially enter the center main slot, flat products preferentially enter the two side slots, and upload order resolves only otherwise identical candidates. `reference_subject` comes only from the matching template row; `visible_product_description` uses only safely visible category, color, and appearance traits from that uploaded image, without inventing a brand, model, price, or parameter. Never substitute a generic phrase such as `槽位 1 为商品 1`. If the user explicitly maps an uploaded asset to a named reference subject, use that mapping instead of automatic assignment and record the override in review Markdown.

`foreground_description` reads `template.json.product_slots`; use it only for the ordinary-product branch:

| Supplied product assets | AI-base lower foreground |
|-|-|
| 1 | asset 1 occupies its template slot; retain the small toy and coins |
| 2 | assets 1-2 occupy their template slots; retain the small toy and coins |
| 3 | assets 1-3 occupy their template slots; retain the small toy and coins |
| 4 | assets 1-4 occupy all template slots; retain coins |
| more than 4 | stop before generation and ask the user to keep at most four products |

With other supplied assets, use the template's `partial_upload_behavior`; the resulting foreground keeps the reference image's original product composition as a set of local substitutions. The member-day mark, date subtitle, rule button, rule text, and bottom wave are fixed compositor layers.

## Membership A/S 2:1 Independent QA And Targeted Edit

Check the title-free base first: no title/fixed layers, and the foreground remains in `foreground_region`. With no supplied product assets, the foreground uses the default gift boxes, ribbons, and coins. With a single gift-box asset, the foreground keeps that default composition and the gift boxes preserve the uploaded asset's visible appearance. With other supplied assets, every supplied product stays in its named slot and the staggered foreground holds. A failure uses a product/base-only targeted edit.

Check the title PNG second: exact title copy, usable transparency, selected title style (default 思源宋体 SC Heavy; `特殊字` only uses the brush reference), title-box fit, and no brand/date collision. A failure regenerates only the title asset; never ask the product-base model to rewrite it.

Only after both pass, invoke the compositor. If any title/product/fixed-layer collision appears in the completed image, mark `合成碰撞失败`.

If advanced test fields are explicitly provided, they override the matched preset route unless a forced no-people rule applies. Record this in review Markdown:

```text
高级测试字段覆盖视觉方案档位：是
```

## Category-Specific References

When `business_line_id=biz_n_category / N 品类`, `visual_preset_level=B`, and `category_id` is `cat_bicycle / 骑行`, `cat_billiards_cue / 台球杆`, or `cat_musical_instrument / 乐器`, assemble the final prompt with a product-photography structure:

```text
主方向 + 高级商品光影调制 + 摄影调性 + 品类材质/阴影展开 + 商品角度或器材展示方式
```

Use `frag_premium_product_lighting / 高级商品光影调制` as the shared B-level photography skeleton, then translate it through the current category's `visual_traits`:

- 骑行: 高级几何色块商品棚拍、大车近景广告构图、低机位三分之四侧前方、前轮近景放大、车身向后延伸、高彩撞色空间、车架轮廓光、轮组高光、轮胎接触阴影、路面低反射、墙地交界阴影、色块切面。
- 台球杆: 专业器材高级商品棚拍、器材广告摄影、明确主光方向、材质高光、杆体接触阴影、暗部层次、克制标题尺度；具体台球杆摆放、镜头远近和人物使用关系只读取所选商品组合。
- 乐器: 乐器低语境高级商品棚拍；默认使用材质空间窗光棚拍，包含木质墙面或木地板、暖色墙面或深色声学墙、侧窗光、斜向光斑、大块明暗切面、暗部层次、木纹或金属高光、琴体边缘轮廓光、真实接触阴影、专业器材质感；B 档保持低语境商品承托，不切换到音乐生活方式角落、私人收藏痕迹或完整生活兴趣场景。B 档标题继续使用压实型音乐海报展示黑体，但允许带少量宋意/衬线式刀锋收笔，不改成完整宋体、普通电商粗黑体、柔和文艺黑体或圆润标题字。允许仅作为版式完成层的极低存在感英文微装饰与装饰字，但它们必须停留在标题呼吸区、标题附近或主视觉边缘，不能长成生活方式角落陈列或明显编辑型场景。此时选中的 `09_background_recipes.csv` 背景行是元素池、数量上限、主光规则和禁用扩写的唯一来源：先解析出本次 `背景选用清单`，再把选中的具体元素和统一光影写入 `最终 Prompt`；不要在本文件重复维护候选元素池，也不要在 `最终 Prompt` 中罗列整条候选池。B 档不写练习、演奏、生活方式剧情、人物使用、普通圆台、纯渐变背景、舞台灯阵或厚重促销卡片。

When `business_line_id=biz_n_category / N 品类` and `category_id=cat_musical_instrument / 乐器`, for both `visual_preset_level=B` and `visual_preset_level=A`, resolve and write this item into the final prompt:

- `乐器 B/A 标题字形`: use the same title temperament as `乐器 S 标题字形`, while keeping the B/A route logic unchanged. Use the validated strong-theme musical-poster title temperament: 端正稳定、字面宽大、笔画厚实、重心稳定、局部切角克制、转角带轻微刀锋感、内白略收紧、轻微收窄、以黑体骨架为主，并带少量宋意/衬线式收笔气质，带可见但克制的细印刷颗粒或微磨砂质感。整体应更像被压实的音乐海报标题，而不是圆润、轻飘、细长或柔和文艺感黑体；它可以有一点宋意，但不能走成真正的宋体、细宋或收藏感衬线路线。该纹理在 100% 查看时应可辨，但不能削弱笔画边缘清晰度、文字对比和可读性。文字保持正视、平面、清楚，不使用描边、投影、金属、厚重渐变或大标题框。标题颜色必须按当前画面背景明暗、乐器主色和可读性单独确定。主标题整体只使用两种颜色，其中大部分文字使用主色，只允许一个连续词组使用跳色，不引入第三种强调色。
- `乐器 B/A 微装饰完成层`: for both B and A, write a fixed micro-decoration finish layer directly into `最终 Prompt`. If `decorative_text` is provided, it must appear once as a handwritten low-priority overlay near the main title, title breathing area, or main-visual edge. In addition, B-level must keep exactly 1 group of ultra-low-presence English micro-decoration, and A-level must keep 1-2 groups. Limit the content to tiny English words, short tags, short dashes, dots, or `//`, and keep them attached to title breathing space, title vicinity, main-visual edge, or outer whitespace. They must stay clearly secondary, must not become a third slogan, and must not introduce date, issue, platform-bar, service-promise, or extra selling-point information.

```text
主标题采用固定的乐器 B/A 共用展示标题字形，直接继承已验证的强主题音乐海报字形气质：端正稳定、字面宽大、笔画厚实、重心稳定、局部切角克制、转角带轻微刀锋感、内白略收紧、轻微收窄，以黑体骨架为主，并带少量宋意/衬线式收笔气质，带可见但克制的细印刷颗粒或微磨砂质感；整体更像被压实的音乐海报标题，而不是圆润、轻飘、细长或柔和文艺感黑体；可以有一点宋意，但不能走成真正的宋体、细宋或收藏感衬线路线；该纹理在 100% 查看时应可辨，但不能削弱笔画边缘清晰度、文字对比和可读性；文字保持正视、平面、清楚，不使用描边、投影、金属、厚重渐变或大标题框；标题颜色按当前画面背景明暗、乐器主色和可读性单独决策；主标题整体只使用两种颜色，其中大部分文字使用主色，只允许一个连续词组使用跳色，不引入第三种强调色；副标题数字需要强调时沿用同一个跳色。
```

```text
乐器 B/A 固定加入微装饰完成层：若用户提供装饰字，则将装饰字作为手写感、低优先级的自由叠加元素处理，可轻叠在主标题附近、标题呼吸区或主视觉边缘；除装饰字外，B 档固定保留 1 组、A 档固定保留 1-2 组极低存在感的英文微装饰，可使用 tiny English words、short tags、短横线、点列或 //，位置只落在标题附近、主视觉边缘、边角或外缘留白；这些微装饰只服务版式完成度和音乐专题气质，不形成第三条营销文案，不遮挡主标题、副标题或商品关键特征，不引入日期、期号、平台栏、服务承诺或额外卖点。
```

When `business_line_id=biz_n_category / N 品类`, `visual_preset_level=A`, and `category_id=cat_musical_instrument / 乐器`, resolve and write these items into the final prompt:

- `乐器 A 场景方向`: choose one unified A-level route from `音乐生活方式角落` or `清爽音乐活动生活方式场景`, and write the selected direction explicitly into the final prompt instead of leaving it as an implicit mood.
- `乐器 A 清爽活动完成层`: when the selected background is `bg_music_fresh_event_lifestyle / 乐器_清爽音乐活动生活方式_中语境`, write the final prompt around a complete, believable photographic space before adding activity atmosphere. The instrument should read clearly in the midground; the foreground may use low-presence blur, airy depth, or natural occlusion; the background may use soft environmental blur, gentle bokeh, or weak spatial layers to carry the mood. Activity, seasonal, festival, and editorial-decoration details should attach to this photographic space as secondary atmosphere. Also write this route's default finishing logic directly into `最终 Prompt`: 远景降细节、轻度平面化、杂志广告式调色，画面带有极轻的哑光纸张颗粒和轻印刷感；微装饰遵循 `乐器 B/A 微装饰完成层`，并优先分布在边角、外缘留白和次要空隙处。
- `乐器 A 音乐生活角落总纲句`: when the selected background is `bg_music_editorial_paper_studio / 乐器_音乐生活方式角落_中语境`, start the visual description with this target sentence or an equivalent natural-language opening: `创建一张具有音乐生活方式感的产品海报`. The result should read as a private music corner and editorial spread, not a plain lifestyle photograph or commercial studio setup.
- `乐器 A 音乐生活角落固定结构`: when `bg_music_editorial_paper_studio` is selected, write the fixed structure directly into `最终 Prompt`: one low-presence micro-English header group, one subtle handwritten English note, light texture, and a few personal belongings traces. Optional paper-module decorations, black-vinyl or cover clues, and weak plant shadow or edge small plant may appear only as secondary support. Do not add numbering-like tags, issue/date markers, platform bars, Chinese service copy, or extra benefit lines.
- `乐器 A 音乐生活角落文案边界`: editorial microcopy may use only very short generic English tags or non-factual music-themed words, and must stay decorative and low-priority. Do not introduce `vol.`, `issue`, numbering-like fragments, journal-title structures, year/date claims, service promises, platform wording, or any other unprovided readable information.
- `乐器 A 标题边界`: even in the editorial-corner route, keep the title on the shared B/A strong-theme display-black route with slight Songti / serif edge. Do not let the title drift into a soft magazine serif, thin editorial sans, rounded black, gentle lifestyle-heading look, or a fully serif literary title just because the scene is quieter.
- `乐器 A 光影与质感`: for the editorial-corner route, write afternoon natural sunlight from the window side, gentle but clear light-shadow planes, paper-print texture, cloth fiber, old-paper grain, and very light analog/print noise into the final prompt. The image may be light-toned or dark-toned according to the supplement, but must keep a warm, quiet, lived-in editorial atmosphere.
- `乐器 A 人物边界`: the editorial-corner route defaults to `无人物陈列`; only when the supplement or asset clearly requires use relation may it switch to `人物使用关系`. When A-level includes a person, prioritize a natural performance/use relation first; the face does not need to be deliberately weakened, but it should not become the first visual focus, and the instrument must remain the main subject.

When `business_line_id=biz_n_category / N 品类`, `visual_preset_level=S`, and `category_id=cat_musical_instrument / 乐器`, resolve and write these items into the final prompt:

- `乐器 S 弱完成层`: when the selected background is `bg_music_concert_surreal_scene / 乐器_演唱会超现实抽象场景_强语境`, write a stable weak finish layer directly into `最终 Prompt`: very light matte paper grain, faint print texture, and 1-2 low-presence editorial micro-decoration groups. Treat paper grain and print texture as a subtle global finish layer across the whole image, but keep their strength below the stage/event space, instrument body, and main text.
- `乐器 S 标题字形`: use the validated strong-theme musical-poster title temperament: 端正稳定、字面宽大、笔画厚实、边缘干净、轻微收窄、带极轻印刷颗粒或磨砂质感的现代展示黑体/标题黑体。文字保持正视、平面、清楚，不使用宋体/衬线收藏感路线，也不使用描边、投影、金属、厚重渐变或大标题框。这个参考只作用于字形气质，不继承参考图颜色；标题颜色必须按当前画面背景明暗、乐器主色和可读性单独确定。主标题整体只使用两种颜色，其中大部分文字使用主色，只允许一个连续词组使用跳色，不引入第三种强调色。
- `乐器 S 标题权重与留白`: in 4:3, 16:9, or 2:1 landscape, keep the title group inside the left reading area with visible breathing space on both left and right sides. Resolve semantic line breaks first, then control title width by visual weight: the title should read clearly but should not stretch horizontally to fill the whole text zone, and short titles should not be enlarged just to occupy more width.
- `乐器 S 微装饰位置`: keep the editorial micro-decoration groups attached to corners, outer edges, and title breathing areas only. They may support layout rhythm, but they must not become top banners, central callouts, extra cards, or a new visual carrier that competes with the instrument, title, subtitle, or stage space.
- `乐器 S 微装饰文案边界`: when readable microcopy is used, limit it to tiny English words, very short English fragments distilled from the user-provided main title, subtitle, decorative text, or generic non-factual music tags, plus short dashes, dots, `//`, or light numbering-like structures. Do not introduce year, date, issue, season, journal title, event schedule, or any other unprovided factual wording.
- `乐器 S 主空间边界`: this weak finish layer is a modulation only. It must not rewrite the S-level route into `bg_music_editorial_paper_studio / 乐器_音乐生活方式角落_中语境`, `bg_music_3d_operation_scene / 乐器_3D运营主题陈列_中强语境`, private-collection traces, handwritten-note-led layout, or window-light lifestyle staging. The primary reading should remain strong night-stage atmosphere.
- `乐器 S 夜场人物剪影边界`: when the selected direction is `夜场舞台氛围`, the final prompt may and usually should include low-presence audience silhouettes or crowd silhouettes to establish concert/event scale, even when `people_participation` resolves to `否 / 无人物陈列`. Treat these silhouettes as stage-atmosphere background elements rather than people-use relation: keep them distant, low-detail, and non-interactive, and do not let them become foreground performers, hands, or explicit use-relation subjects around the uploaded instrument.

For these B-level routes, write the selected product-photography language directly into `最终 Prompt` as the main visual description.

## Background Subset Resolution

When the selected `background_recipe_id` contains candidate elements, props, count caps, optional carriers, or other background-level choices, resolve one concrete `背景选用清单` before writing `最终 Prompt`.

- The selected row in `09_background_recipes.csv` is the only source of truth for background element pools, count limits, hard light/spatial rules, and forbidden spillover.
- `最终 Prompt` may mention only the selected visible subset and the selected row's hard rules. Do not restate the full candidate pool, do not write “从 A/B/C 中选择一些” style wording, and do not expand with out-of-row props.
- Record `背景选用清单` in review Markdown together with the selected background ID and Chinese name.
- When the selected background is `bg_recycle_service_graphic / 回收_背景_弱中语境`, resolve and record the support surface as `无台面` or `1 个连续台面/统一承托面`. The final prompt must not leave this open-ended as multiple platforms, and must not allow two or more separated podiums, round platforms, stone blocks, trays, or support blocks.
- When the selected combination is `combo_multi_recyclable / 多品类回收组合`, write the product arrangement as a staggered recycle product group by default. For exactly 2 products or categories, do not write a forced main/support hierarchy; keep both products at reasonable size and require stagger through front/back, high/low, offset bottom edges, size, angle, light perspective, or slight overlap. Explicitly avoid aligned lower edges, equal-height side-by-side placement, and ordinary product-pair posing. For 3 or more products or categories, one main recyclable object may be larger, while supporting objects are arranged with front/back, high/low, size, angle, and light-perspective variation. Each product remains complete and recognizable. Do not describe it as a generic card matrix unless the user explicitly asks for cards, entrance grids, iconized categories, or flow nodes.
- For `biz_membership + cat_membership_day + B`, apply the preceding `combo_multi_recyclable` geometry and support-surface rule as a visual parent rule, but describe the result only as a membership activity product group. Do not copy recycle coverage or service semantics into the final Prompt.

When `business_line_id=biz_n_category / N 品类` and `category_id=cat_billiards_cue / 台球杆`, B/A/S all resolve and write this item into the final prompt:

- `台球杆摆放方式`: resolve and write the cue placement only from the selected product combination row. When `people_participation=否 / 无人物陈列`, B-level follows `combo_billiards_cue_diagonal_texture / 台球杆斜向质感陈列` and A/S follow `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列`; when `people_participation=是 / 人物参与` for a single uploaded cue asset, switch to `combo_billiards_cue_people_use / 台球杆人物使用陈列` and let the visible use relation become the primary camera/composition language. If the selected combination is `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列`, the final prompt must explicitly write: `主视觉必须以杆尾或握把附近的局部放大为第一视觉重心，并清晰看到至少一个高价值细节；多杆错落陈列且每根杆可识别。` The uploaded product image is the source for cue identity, color, texture, material pattern, rings, grip, and key details, but it must not lock the final poster into the uploaded product-photo arrangement; the cue may change angle for a believable shot line, but it must still read as the same uploaded product.
- `台球桌几何约束`: when the selected scene, background, or composition introduces billiard-table relations, the final prompt must include this exact constraint: `如出现台球桌、桌边、桌角、袋口或局部台面关系，保持真实台球桌几何：桌边笔直，袋口比例正常，桌面为合理四边形结构，不要出现边框弯折、桌角拉伸或错误透视。`
- `台球杆 A/S Prompt 写法`: keep the final prompt concise and positive. Write the selected scene direction, the 2 selected visible background elements, product display, title handling, and essential quality requirements. Keep negative-rule details in `合并禁止项` and QA notes, not in the submitted final prompt.

When `business_line_id=biz_n_category / N 品类`, `visual_preset_level=B`, and `category_id=cat_billiards_cue / 台球杆`, resolve and write this item into the final prompt:
- `台球杆 B 专用背景`: use `bg_billiards_premium_texture_display / 台球杆高级材质陈列背景` first. Choose one main support material from 深色台呢、绒面托盘、皮革台面、深木台面、石材块、浅色纸面 or 高级墙面, then add only low-presence billiards context such as blurred billiard balls, table edge, cue rack, glass reflection, or dark club lighting when useful. Write the selected material, color mood, and light direction into the final prompt.

When `business_line_id=biz_n_category / N 品类`, `visual_preset_level=A`, and `category_id=cat_billiards_cue / 台球杆`, resolve and write these items into the final prompt:

- `台球杆 A 商品组合`: keep `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列` as the main arrangement language only when `people_participation=否 / 无人物陈列`. If `people_participation=是 / 人物参与`, do not use `combo_billiards_cue_natural_texture_display`; switch to `combo_billiards_cue_people_use / 台球杆人物使用陈列` and let the selected combination own the people-use composition and spatial logic. This single-cue people-routing rule applies only to a single uploaded cue asset; when multiple cue assets or multiple product assets are uploaded, do not apply the single-cue restriction by default.
- `台球杆 A 场景方向`: write one unified life-interest scene into the final prompt: use a restrained loft corner, wood space, or light interior to present the cue as an interest identity. Select exactly 2 visible background elements from real billiard balls, chalk, cue rest, local training-table relation, plant shadow, books or paper, and quiet light-colored objects. 默认不使用白球/母球；keep the scene professional and low-presence.
- `台球杆 A 专用背景`: prefer `bg_billiards_clean_table / 台球杆_生活兴趣场景_中语境`. The final prompt should make this single A-level route explicit and keep it distinct from B-level low-context material-display photography.

When `business_line_id=biz_n_category / N 品类`, `visual_preset_level=S`, and `category_id=cat_billiards_cue / 台球杆`, resolve and write these items into the final prompt:

- `台球杆 S 商品组合`: keep `combo_billiards_cue_natural_texture_display / 台球杆自然质感陈列` as the main arrangement language when `people_participation=否 / 无人物陈列`. If `people_participation=是 / 人物参与` for a single uploaded cue asset, switch to `combo_billiards_cue_people_use / 台球杆人物使用陈列`; surreal concept space may modulate the carrier, but the selected combination remains the only source of cue placement and people-use shot logic.
- `台球杆 S 专用背景`: prefer `bg_billiards_surreal_concept_space / 台球杆超现实概念空间_强语境`. Default to `超现实桌台重构` as the primary concept direction; only use floating material space, geometric structure cuts, or light-sculpted concept space when the user explicitly asks or the task clearly needs them. Then select exactly 2 visible background elements from pale stone platform, floating rock fragments, floating material fragments, misty air, steps, columns, light-toned architectural planes, and black 8-ball. If any ball appears, render it as black 8-ball, and decide its position and visibility from the shot line, composition, and scene needs.
- `台球杆标题字形`: use a fixed cue-title style: 高级器材广告高对比中文宋体或衬线字体，字面修长，结构稳定，粗细对比明确，边缘干净，收笔克制，具有收藏级专业器材质感. Choose the main title color by contrast with the title background space: use 象牙白、暖白或浅金白 on dark backgrounds, and 深墨绿、近黑或深棕色 on light backgrounds. The title may add one restrained accent color only; the accent color should come from 木纹暖色、金属环高光 or 深绿台呢环境色. Apply the accent to one continuous keyword or key phrase, keep the remaining main title characters in the chosen main title color, and reuse the same accent color for subtitle numerals when emphasis is needed. Write this directly into the final prompt instead of calling a typography reference image.
- `台球杆标题权重与字号`: this rule also applies across B/A/S unless the user explicitly overrides it. Do not size the title by fixed image-area ratio alone. Resolve semantic line breaks and per-line character count first, then set the title by visual weight: the cue body remains the first visual subject, the title reads clearly but stays secondary, and short titles must not be enlarged just to fill the text zone. In 4:3, keep the title group in the vertical middle of the left reading area, leave clear breathing space above it, and let decorative text follow the title group without sticking to the top-left corner. Treat `22%-30% of image height, below one third` only as an upper-bound QA check for the whole title group instead of a direct font-size target.

```text
主标题采用固定的台球杆高级器材广告字形，高对比中文宋体或衬线字体，字面修长，结构稳定，粗细对比明确，边缘干净，收笔克制，具有收藏级专业器材质感；标题主色根据标题所在背景空间的明暗选择，深色背景用象牙白、暖白或浅金白，浅色背景用深墨绿、近黑或深棕色；跳色最多一个，来自木纹暖色、金属环高光或深绿台呢环境色，并集中用于一个连续关键词或关键短语；其他主标题字保持选定的标题主色，副标题数字需要强调时沿用同一个跳色；不使用廉价促销粗黑体、综艺感黑体、厚重渐变字、描边、投影或大标题框。
```

When `business_line_id=biz_n_category / N 品类` and `category_id=cat_bicycle / 骑行`, resolve and write these items into the final prompt:

- `骑行色板锚点`: for B-level, extract the obvious product color from the uploaded product image and record it. If the product image is mainly black, white, gray, or silver, record `黑白灰银为主`.
- `骑行选中色板`: for B-level, select one contrast hue relationship from the clash hue pool in `bg_bicycle_contrast_colorblock_studio / 骑行强对比几何色块棚拍背景`, record the hue relationship and brightness modulation, and write them into the final prompt without fixed HEX values. The selected hue relationship should echo or highlight `骑行色板锚点`; when the product image is mainly black, white, gray, or silver, rotate through the clash hue pool. When supplemental requirements mention 浅色、清爽、明亮、白底、淡色 or 轻盈, keep the same hue relationship but increase the area of light or neutral tones.
- `骑行 B 专用背景`: for B-level, use `bg_bicycle_contrast_colorblock_studio / 骑行强对比几何色块棚拍背景`. Write the selected hue relationship into the final prompt as a three-layer color system: spatial base color, high-chroma spatial main color, and neutral light cut-plane/breathing layer, with all space colors modulated from the selected hue relationship. Give the three colors clear hierarchy: one large-area spatial base color, one medium-area high-chroma spatial main color, and one small-area neutral light cut-plane/breathing layer. For a dark version, make the dark spatial base color the largest area; for a light version, make the neutral light/breathing color the largest area. The final prompt must state where the high-chroma wall + floor + diagonal geometric-plane space sits behind or under the bicycle, and how the neutral light layer appears as a matte diagonal cut plane, side wall, local wall-floor transition, soft floor reflection, or title-area breathing space. Geometric color blocks should enter the space as walls, floor, side wall, and diagonal cut planes; the neutral light layer should act as a corner plane, side wall, or title breathing layer.
- `骑行 A 速度情绪海报`: for A-level, write the result as `一个有冲突、有速度、有情绪的骑行视觉海报`. The final prompt must include stronger cycling speed: visible ground speed smear, stronger side-backlight, compressed foreground/background depth, and stronger speed perspective. Keep the visual language clean and integrated into the same light, color, and motion system, and do not let extra decoration obscure the bicycle, rider, title, subtitle, or key product structure.
- `骑行 A 纸感纹理`: for A-level, weak paper texture is part of the default finish layer. Write it as very light matte paper grain and faint print texture inside sky blank space, top information band, and title breathing space. Keep the bicycle body, key frame details, wheel/drive/brake recognition, and title readability clear and complete.
- `骑行 A 编辑装饰位置`: for A-level, editorial-style decoration is a fixed component rather than an optional garnish. The final prompt should explicitly require a top horizontal blank band with 2-3 low-presence information clusters. Keep the clusters inside safe margins and clearly secondary to the product and title.
- `骑行 A 角落微文案`: for A-level, editorial-style corner microcopy should be written as required low-priority structure, not an optional possibility. Prefer very small English words, short English tags, // separators, dots, short dashes, compact tag groups, or short numbering-like structures derived from the existing input. Keep decorative text lower priority than the main title, subtitle, and product, but still explicitly present in the final prompt. When readable text is included, use only English words or short English fragments distilled from the user-provided main title, subtitle, decorative text, or other explicitly provided short phrases; do not introduce business-line wording, year, season, issue, journal title, or other extra factual wording.
- `骑行商品角度`: choose one angle from `cat_bicycle.visual_traits` and express it as camera/composition language. For B-level side-view or three-quarter-front routes, prioritize a large close advertising composition: enlarged near front wheel, low-angle three-quarter-front view, and bicycle frame extending backward to create perspective pressure. If the uploaded bicycle image is flat side-view and the user did not ask to preserve that angle, the final prompt may say to keep product identity while reconstructing the bicycle into the selected advertising angle.
- `骑行标题字形`: use a fixed clean cycling title style: 高级运动广告宽体粗黑体、端正稳定、字面宽大、笔画厚实、几何感强、边缘干净、切角克制、整体清晰利落. Choose the main title color by contrast with the title background plane: use white/light title color on dark background planes, and black/near-black title color on light background planes. The title may add one accent color only; the accent color should come from `骑行色板锚点` or the high-chroma main color in `骑行选中色板`. Apply the accent to one continuous keyword or key phrase, keep the remaining main title characters in the chosen main title color, and reuse the same accent color for subtitle numerals when emphasis is needed. Write this directly into the final prompt instead of calling a typography reference image.

```text
主标题采用固定的高级骑行运动广告字形，宽体粗黑体、端正稳定、字面宽大、笔画厚实、几何感强、边缘干净、切角克制，整体清晰利落；标题主色根据标题所在背景切面的明暗选择，深色背景用白色/浅色标题，浅色背景用黑色/近黑色标题；跳色最多一个，来自商品色锚点或背景高彩主色，并集中用于一个连续关键词或关键短语；其他主标题字保持选定的标题主色，副标题数字需要强调时沿用同一个跳色。
```

## Visual Expression Mode Handling

Use `视觉表达模式` as an internal or advanced-test routing phrase in the final prompt only when it helps clarify the product arrangement and background choice. Do not expose raw IDs.

If `visual_expression_mode=稳定承托`, use phrasing like:

```text
视觉表达采用稳定承托，商品完整清晰作为主角，场景、道具和信息层保持克制，背景干净服务商品识别和信息阅读；若人物参与为是，人物与商品的使用关系仍保持清晰可见。
```

If `visual_expression_mode=场景表达`, use phrasing like:

```text
视觉表达采用场景表达，商品或主体进入使用语境、内容语境或活动语境，场景、道具和背景延展服务主题价值；人物、手部、佩戴或操作关系按人物参与设置和商品组合判断。
```

If `visual_expression_mode=自动`, infer one of the two directions and record the reason in the review Markdown. In the final prompt, write the inferred visual expression direction naturally rather than saying `自动`.

## People Participation Handling

Use `人物参与` as a routing phrase in the final prompt only when it helps clarify product arrangement or scene relation. Do not expose raw IDs.

Before writing the final prompt, apply forced no-people overrides: any matched `B` preset route, or any multi-asset / multi-subject merchandise structure, must be written as `人物参与=否 / 无人物陈列` even if the user explicitly provides `人物参与=是`.

If `people_participation=否`, use phrasing like:

```text
人物参与设为无人物陈列，画面不加入人物、手部、佩戴、操作或使用者关系，商品通过陈列、道具、空间和信息模块表达价值。
```

If `people_participation=是`, use phrasing like:

```text
人物参与设为商品使用关系，人物与用户提供的商品形成清晰可见的使用关系，优先表现为佩戴、手持、操作、骑行、演奏、试用或使用中展示，人物动作、身体位置和视线共同服务商品使用价值。
```

If `people_participation=自动`, infer whether people are useful and record the reason in the review Markdown. In the final prompt, write the resolved direction naturally rather than saying `自动`.

## Text Handling

Treat main title and subtitle as required poster text unless the user says they are only for intent inference.

Use phrasing like:

```text
主标题文字为「...」，副标题文字为「...」，主标题和副标题采用正视平面排版，文字基线稳定、横平竖直、正对画面阅读；主标题字面颜色稳定、平面干净，字重有识别度但不过度压迫；主副标题层级明确，副标题与主标题保持舒展间距和呼吸感。
```

For 4:3, 16:9, and 2:1 landscape posters, use a left-text/right-visual reading tendency without hard percentage zones:

```text
画面按左文右视觉的阅读动线组织；文字、商品或人物主视觉共享同一背景空间，允许轻度层次叠加，整体光源、透视、色彩和阴影保持连贯。
```

For 1:1 square posters, keep the title behavior from `fmt_square_1_1`:

```text
采用上方阅读重心、下方主视觉重心的构图；标题、商品、人物和背景属于同一个连续画面系统，通过留白、景深、光影、色彩过渡或图形秩序形成阅读层级；主标题默认完整单行呈现，通过字号、字距、标题宽度和位置适配保证可读；用户明确要求折行时再按用户要求处理。
```

When `format_id=fmt_landscape_4_3` or `format_id=fmt_landscape_16_9` and the main title is longer than 4 Chinese characters, add this title handling rule to the final prompt and write the concrete two-line split:

```text
主标题超过 4 个汉字时，默认按语义拆成两行标题组，每行保留完整词组，不拆断品牌名、品类名、数字权益或固定短语；在最终 Prompt 中明确写出两行标题，例如：主标题按两行展示：「第一行」和「第二行」。
```

When `format_id=fmt_landscape_2_1`, apply the route-owned maximum title width. For `会员` A/S use 908px at a 1125px-wide reference canvas: keep one line and proportionally reduce the title size only if it exceeds that width. For `会员` B use 590px at the same reference width: if the one-line visible width exceeds that maximum, add this title handling rule and write the concrete semantic split:

```text
会员 B 2:1 横版先测量主标题的单行可见宽度；仅当它超过 590px 时，才按语义拆成两行标题组。每行保留完整词组、标点和固定短语；在最终 Prompt 中明确写出两行标题，例如：主标题按两行展示：「第一行」和「第二行」。会员 A/S 2:1 超过 908px 时保持单行并按比例缩小字号。
```

When `business_line_id=biz_recycle`, `format_id=fmt_landscape_2_1`, and the user explicitly provides `label_text`, render it as an optional top label above the main title. Do not infer or auto-generate a label when the field is absent.

```text
标签文字为「...」，只因用户明确提供而出现；作为主标题上方的轻量胶囊线框标签，保留浅色或半透明胶囊底、细描边、圆角胶囊外框和舒展左右内边距；标签文字大小与副标题相同，可用更轻字重或低对比灰/棕/产品色保持辅助层级；与主标题左边线稳定对齐，和主标题之间保留清晰呼吸距离；标签不参与主标题折行判断，不替代主标题或副标题，不承载未提供的价格、补贴、服务承诺、活动日期等事实信息；不要做成无边框普通文字，不要缩成难读的小字，也不要做成实心强色块、大促销角标、爆炸贴、按钮、重阴影、发光或厚描边。
```

For list-style subtitles that are split into cards, do not use the full subtitle sentence in the final prompt. Use phrasing like:

```text
主标题文字为「...」，将副标题中的权益点拆成卡片展示：「...」「...」「...」。
```

If exact text rendering is mission-critical, add:

```text
标题和副标题或拆分后的卡片文案必须按用户提供文字呈现；生成后需要进行文字准确性检查，必要时进入设计后期修正。
```

If `decorative_text` is provided, add it as a handwritten overlay design element:

```text
装饰字为「...」，作为手写风格自由叠加元素处理，可叠加在主标题左上角附近，或轻叠在商品、人物或主视觉边缘，形成松弛的设计笔触；装饰字不作为第三条营销文案，不遮挡主标题、副标题、人物脸部或商品关键特征。
```

If `decorative_text` is empty, do not mention or generate decorative text.

## Copy Carrier And Deduplication

Use one carrier for each user-provided copy item.

- Main title appears once.
- If subtitle is a normal sentence, render it once as the subtitle.
- User-provided decorative text appears only when the user provides it, and it is not a third slogan or fact claim. Low-priority decorative microcopy can appear as atmosphere when it stays separate from business copy and factual claims.
- If subtitle is a list of benefits, selling points, service points, or short modules, choose one carrier:
  - If the selected layout has benefit cards, selling-point cards, service cards, or modular information cards, split the list subtitle into those cards and do not render the full subtitle sentence again.
  - If the selected layout has no suitable card/module carrier, render the subtitle once as a single subtitle line.
- Do not show the same subtitle content both as a full subtitle line and again inside cards.
- Common list separators include `｜`, `|`, `/`, `、`, commas, semicolons, line breaks, or multiple short phrases with parallel structure.

## Benefit Information Layer

When the marketing type is `m_flash_sale`, `m_subsidy_benefit`, or `m_sales_ranking`, use `frag_benefit_modules_light` as an information layer when the user provided price, discount, subsidy, membership, recharge, exchange, service, guarantee, or ranking copy.

Benefit modules do not choose the background. Select the background from business line, category, product relation, product combination, composition, and scene semantics first; then add the benefit modules as lightweight information near the title or product.

Use phrasing like:

```text
将用户提供的价格、折扣、补贴、会员、充值、兑换、保障或卖点整理为轻量文字信息层；优先使用纯文字短句、细分隔线、中点分隔或低存在感信息行，作为标题或商品旁的辅助信息层，不作为整张背景主风格；卡券类会员、充值、兑换等虚拟权益卡面由卡券品类和专门背景承接，不在通用权益模块中默认生成权益卡、卖点卡或图标。
```

## Final Prompt Shape

```text
生成一张{business_line_name} {format}运营海报，主题是{main_title_or_marketing_theme}，{format_reading_flow_sentence}。{visual_expression_mode_sentence}{people_participation_sentence_if_useful}{product_display_natural_sentence}。整体{marketing_expression_and_visual_tone}。背景{background_natural_sentence}，商品完整清晰，标题和承载文案清晰可读。主标题为「{main_title}」，{subtitle_or_card_copy_sentence}{decorative_text_sentence_if_any}。{compressed_negative_constraints}
```

Example shape:

```text
生成一张转转 N 品类 4:3 横版运营海报，主题是潮玩新人专属权益，按左文右视觉的阅读动线组织画面，文字和商品卡阵列共享同一背景空间。整体可爱、干净、有新人福利感，但不出现具体价格、折扣、券额或活动日期。背景采用柔和暖色渐变、圆角卡片、轻展台、星星点缀和统一光影，商品完整露出，主副标题清晰可读。主标题为「潮玩新人专属」，副标题为「趣玩生活入坑可以更省」，副标题与主标题保持舒展间距。仅使用用户提供业务文案，不新增价格、折扣、品牌、IP 名、二维码或事实型文字；商品完整清晰，不裁切不遮挡。
```

If subtitle is `无`, say:

```text
只保留主标题，不强行添加副标题。
```

## Self-Check

Before finalizing, run this Pre-output self-check for prompt assembly. Post-generation visual judgment belongs to `qa-flow.md` and `visual-qa.md`.

- business line is not mixed with another business line
- marketing type matches title/subtitle intent
- visual preset level is matched to the correct business line and category when provided
- explicit advanced test fields correctly override visual preset route factors, except that matched `B` preset routes and multi-asset / multi-subject merchandise structures still force `人物参与=否 / 无人物陈列`
- visual expression mode matches user preference or automatic inference, and influences combination before background
- people participation matches user preference or automatic inference, and influences product combination before composition and background
- product identity is preserved
- relation and combination match image count and marketing goal
- product arrangement has hierarchy, grouping, rhythm, and enough breathing room
- background supports product and title, not the other way around
- background, title, product, people, and information modules belong to one space logic or one design system; realistic scenes, flat graphics, collage, cards, and light-tech spaces need shared color, light, perspective, shadow, edge transition, or graphic order
- for 1:1 square posters, the upper reading focus and lower visual focus form one continuous image system through whitespace, depth of field, light, color transition, or graphic order
- benefit, selling-point, and service information stays light: short text, subtle separators, centered dots, or low-presence information lines; consumer electronics should not use icon cards, benefit cards, selling-point cards, button-like modules, or obvious UI containers
- for 1:1 square posters, the main title is kept as a complete single-line title unless the user explicitly asks for line breaks
- for 4:3 and 16:9 landscape posters, if the main title is longer than 4 Chinese characters, it is handled as a semantic two-line title group
- for 2:1 landscape posters, follow the active route’s title-overflow policy rather than product-space pressure: 会员 A/S keeps one line and shrinks after 908px at 1125px reference width; 会员 B wraps semantically after 590px
- user-provided copy uses one carrier only; no repeated subtitle/list copy across title area and cards
- format matches the requested ratio and reading flow
- no unprovided readable factual information such as price, ranking, model, date, or service promise appears

## Negative Rule Merge

Collect `negative_rule_ids` from the selected business line, category map, marketing type, format, relation, combination, composition, background recipe, and common prompt fragments.

Then read `12_negative_rules.csv`, deduplicate by `negative_rule_id`, and merge only the `negative_prompt_fragment` values into the final `禁止项` block. Keep positive visual description in the main prompt body.

For `最终 Prompt`, do not paste the full merged negative rules. Compress the most important constraints into one short sentence, usually covering:

- user-provided business copy only; low-priority decorative microcopy is acceptable when it is not a fact, CTA, brand, benefit, or selling point
- no duplicate copy across subtitle, cards, badges, or modules
- no text outline, shadow, 3D, metallic, obvious gradient title fill, heavy commerce-template title effect, over-pressing font weight, heavy glow, or heavy title-plate effects
- no perspective text, tilted text, skewed text, spatially rotated text, or large title-panel carrier
- no disconnected background systems, hard collage seams, conflicting light/perspective, heavy solid benefit buttons, heavy filled cards, or bulky UI-like benefit modules
- no unprovided readable factual information such as price, discount, brand, IP, ranking, date, or service promise
- product complete, clear, not cropped, not occluded
- no QR code, watermark, extra UI, or unrelated business/factual readable text

Keep the full selected `negative_rule_ids` and full merged negative rules in the review Markdown under `合并禁止项`. For image-generation reviews, write `review.md` in the card-style format defined in `generation-execution.md`.

In the review Markdown `选用参数` section, include both stable IDs and Chinese display names. Also list the Chinese fragments actually called from the selected rows, such as business-line base visual tone, business-line visual priority, product relation hierarchy, combination arrangement, positive product visual language, composition phrase, background phrase, background visual language, and continuity rules.

## Long Review Prompt

`生图执行 Prompt` is optional review material. It may expand business scope, product appearance, relation, arrangement, composition, background, text, marketing expression, and full constraints for testing and handoff.

Never submit `生图执行 Prompt` to the image generation model. Submit only `最终 Prompt`. In the review Markdown, mark `最终 Prompt` as `参与生图：是` and mark `生图执行 Prompt` as `参与生图：否`.
