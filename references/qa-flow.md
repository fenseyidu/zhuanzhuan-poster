# QA Flow v0.1

## Purpose

Use this file to schedule QA for Zhuanzhuan poster prompt generation and image generation. This file owns QA timing, required references, retry policy, and where QA notes are recorded.

Do not duplicate visual judging rules here. Run visual judging through `references/visual-qa.md`.

## QA Timing

```text
assembled task + final prompt
-> Pre-output QA
-> if PASS: prompt output or image generation
-> if FAIL before generation: fix final prompt once
-> generated image
-> Visual QA with visual-qa.md
-> if FAIL: one targeted retry by default
-> archive generated image + review.md
-> Technical QA
-> final delivery
```

Run QA at these moments:

1. Pre-output QA before returning a prompt-only answer or before submitting `最终 Prompt` to image generation.
2. Visual QA after an image is generated.
3. Technical QA after saving generated files and `review.md`.

Default retry policy:

- PASS: continue to the next step.
- FAIL before image generation: fix the final prompt once before submitting it.
- FAIL after image generation: classify the failed layer with `visual-qa.md`, list passed layers to keep unchanged, write one local targeted correction prompt from `generation-execution.md`, and regenerate once when image generation is available.
- FAIL after one targeted retry: stop and state the specific blocker.

Membership override:

- For `会员` image generation, automatically allow up to two targeted regenerations after a visual QA failure, with QA after each version.
- Each regeneration uses the latest failed image as the sole edit target and changes only the active failed layer.
- If the second targeted regeneration still fails, stop and state the specific blocker; do not ask the user whether to continue.
- For `会员` S, do not apply the A/S slot, title-asset, or fixed-layer checks below: those legacy A/S references now apply to A only. Check the selected 圣诞/中秋 background, the zero-product gift branch or resolved product relation, the left reading field, right theme focus, and shared theme light. For 圣诞, also compare the title-free AI base with `source/membership-s-christmas-background-master.png`: retain the wide left reading field and the right star-crown/light-tree/gift structure before accepting product changes. Then run `membership_s_renderer.py` and verify the complete alpha-mask logo, a single-line fitted main title, the conditional X-title behavior, and one background-adaptive color shared by logo and text.

Default report policy:

- Do not create a separate QA report unless the user explicitly asks.
- For prompt-only output, summarize QA in `自检清单`.
- For image generation, write structured QA notes in `review.md` under `生图 QA 备注`.

## Required QA References

Read these files only when their QA stage is reached:

| Stage | Read |
|-|-|
| Pre-output QA | `references/prompt-assembly.md`, selected CSV rows, `12_negative_rules.csv` |
| Visual QA | `references/visual-qa.md`, `references/generation-execution.md`, normalized task card, selected parameter traces |
| Technical QA | this file |

## Pre-output QA

Pre-output QA checks the assembled task and `最终 Prompt` before output or image generation.

PASS:

- Required inputs are present: product assets, main title, subtitle or `无`, business line, and format.
- Optional inputs are normalized when present: label text, decorative text, visual expression mode, people participation, and supplement.
- `视觉表达模式` and `人物参与` are either user-provided or resolved from `自动`, and they affect product combination before composition and background selection.
- Product relation, product combination, composition, and background are selected from the CSV library.
- When `biz_consumer_electronics / 消费电子` matches a B/A/S preset row, the selected background is one of that row's `preferred_background_ids`, or the review records an explicit user/safety/advanced-test override reason.
- When `biz_consumer_electronics / 消费电子` matches B/A/S, the review records an active expression direction and concrete lighting strategy; for A/S, the review records one concrete combination direction from `08_product_combinations.csv`, including ID and Chinese name, and the final prompt uses that direction as the primary scene or arrangement language.
- When the selected background recipe defines candidate elements, count caps, optional carriers, or hard light/spatial rules, the review records one concrete `背景选用清单`, and `最终 Prompt` writes only that selected subset rather than the full candidate pool.
- `最终 Prompt` is concise and suitable for direct image generation.
- `最终 Prompt` includes selected format behavior, product source, product arrangement, background, title/subtitle handling, and essential constraints.
- In the `会员` B `2:1` local-composition route, a non-empty title-group subtitle is excluded from the AI text request and has a local-composition plan using `assets/subtitle-typography.json`; the review records its final font size, visible box, color, and title gap after rendering. In every other route, the exact subtitle remains in the AI text request and no local subtitle layer is planned.
- In the `会员` B `2:1` route, the final Prompt explicitly keeps the left 60% as continuous text-reading background and confines the main product group to the right 40%; do not express this as a reservation, placeholder, or blank-block instruction.
- In the `会员` B `2:1` local-composition route, inspect visible bounds after rendering: the member mark → main-title gap and main-title → subtitle gap are both 62px at the 2250px-wide final canvas, and the three-layer group is vertically centered. Recompute the group for a wrapped main title instead of preserving the single-line y-coordinate.
- 4:3 and 16:9 long main titles include the semantic two-line title rule when applicable. For 2:1, follow the active route's measured width policy: 会员 A uses 908px at 1125px reference width and shrinks an over-width title while keeping one line; 会员 S keeps the main title on one line by shrinking it inside the registered 580px MasterGo reference text region; 会员 B uses 590px at the same reference width and semantically wraps an over-width title.
- User-provided copy uses one carrier only and does not duplicate subtitle/list content.
- Selected `negative_rule_ids` are deduplicated through `12_negative_rules.csv`.
- No unprovided readable factual information is introduced, such as price, discount, subsidy, ranking, brand, model, date, IP name, game name, or service promise.

FAIL:

- Required input is missing and cannot be safely inferred.
- A risky factual claim needs source confirmation.
- `视觉表达模式` or `人物参与` conflicts with product combination, people/use relation, composition, or background.
- `biz_consumer_electronics / 消费电子` matches a B/A/S preset row, but the selected background is outside that row's `preferred_background_ids` and no explicit override reason is recorded.
- `biz_consumer_electronics / 消费电子` A/S stays at the parent A/S route, or only lists candidate directions such as 微缩主题场景 or 超现实商品场景, without selecting one concrete combination direction from `08_product_combinations.csv` and making it the primary final-prompt language.
- `biz_consumer_electronics / 消费电子` uses a real-scene route but the final prompt describes only a plain photographic scene without a consumer-electronics lighting strategy, material/light detail, or advertising design layer.
- A selected background row defines candidate elements, count caps, or hard light/spatial rules, but the final prompt leaves the background as an unresolved candidate pool, expands beyond the row, or omits the required selected subset record.
- The final prompt omits product source, output format, title/subtitle handling, or core product identity constraints.
- The final prompt uses `生图执行 Prompt`, parameter traces, or full merged negative rules as model input.
- The prompt adds unprovided readable factual information or unrelated readable text.
- The prompt asks for people, hands, wearing, operation, props, or scene extensions that do not serve the theme, product value, selected visual expression mode, or provided assets.

## Visual QA

Visual QA checks the generated image against the normalized task card and selected parameters.

Required action:

1. Read `references/visual-qa.md`.
2. Inspect the generated image against each required layer. When uploaded product images exist, explicitly compare the generated product against the uploaded product image before deciding `通过`.
3. Classify result as `通过`, `需定向重生`, or `需人工后期`.
4. For every `会员` A 2:1 head, before fixed-layer composition check the title-free base against the lower product region and slots, then check the title-only PNG for exact copy, transparency, style, title-box fit, and fixed-layer reservations. Retry only the failed asset, following the membership override of at most two targeted regenerations. After composition, check all layers for collisions and confirm the date/subtitle uses the global subtitle typography policy. For `会员` S 2:1, verify its title-free base, exact `title` and `subtitle` inputs, their shared 580px reference reading box, a single-line main title fitted by proportional font reduction, subtitle wrapping/horizontal centering when needed, the recomputed vertical-group center, the complete alpha-mask logo, the conditional X-title behavior, and the shared background-adaptive color. For `会员` B 2:1, first verify that the full recycle B visual route was used: stable support, no people, `bg_recycle_service_graphic`, no support surface or one continuous support surface, and—when two or more physical product assets are supplied—the `combo_multi_recyclable` product geometry. Verify that the generated poster base omits only the main title and subtitle while preserving source-product text and screen content. Compose with `text_layout_renderer.py --profile membership-b-2x1 --trace-output <title-layout.json>`, then with `membership_head_renderer.py --mode membership-b --title-layout <title-layout.json>`; verify the local member mark is left-aligned above the local title and does not collide with title, subtitle, product, or background details. The review must record membership business wording and must not add recycle coverage or service claims. For non-membership failures, if image generation is available, list the failed layer, concrete failure point, and passed layers to keep unchanged; then follow the `Targeted Edit Input Contract` in `generation-execution.md`: use the current generated image as the only untyped retry input, write one local targeted correction prompt, and regenerate once by default. When the failed layer is `商品层` and the product no longer matches the uploaded product image, use a source product image only if the editing capability can explicitly assign it a product-reference role; otherwise prefer `需人工后期` to an untyped multi-image retry.
5. Write the conclusion into `review.md` and user-facing notes.

Use this output shape:

```text
QA 结论：通过 / 需定向重生 / 需人工后期
保留项：{what works and should stay}
问题分层：{failed_layers_or_无}
修正项：{only failed items}
定向修正 Prompt：{targeted_retry_prompt_or_无}
```

## Membership B Mark QA Override

For `会员` B 2:1, fail Visual QA if the AI base contains a membership-mark reservation, blank rounded placeholder, empty card/block, or an AI-generated membership logo. The AI prompt must contain no reservation instruction. Only after the base passes does the renderer dynamically place the 60px mark from the measured title top/left boundary and representative title color.

## Technical QA

Technical QA is a simple deterministic check after saving files. No script is required by default.

PASS:

- Generated image path is recorded.
- `review.md` is saved when image generation runs.
- Output archive is under `~/Documents/转转海报输出/`, not in or beside the skill installation directory.
- Output image can be opened or displayed by the current environment.
- Image aspect ratio matches requested `1:1`, `4:3`, `16:9`, or `2:1` when dimensions are inspectable.

FAIL:

- Generated image is missing or cannot be opened.
- `review.md` is missing after image generation.
- Archive was written in or beside the skill installation directory instead of `~/Documents/转转海报输出/`.
- Inspectable final image dimensions do not match requested format. For `会员` A/S 2:1, a non-2:1 AI base is not itself a failure: the renderer normalizes it by cover-scaling and cropping before final-size QA.

When Technical QA fails, fix file/archive issues once if possible. For `会员` A/S 2:1, normalize a first-generation AI-base ratio mismatch in the renderer; do not regenerate solely for that mismatch. Regenerate only if the final composed image still has a distinct foreground, slot, or collision failure that cropping cannot resolve.
