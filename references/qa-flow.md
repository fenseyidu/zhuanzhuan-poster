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
- 4:3 and 16:9 long main titles include the semantic two-line title rule when applicable; 2:1 main titles stay single-line when readable and use semantic two-line handling only when a long line would squeeze product space or reduce readability.
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
- The final prompt omits product source, output format, title/subtitle, or core product identity constraints.
- The final prompt uses `生图执行 Prompt`, parameter traces, or full merged negative rules as model input.
- The prompt adds unprovided readable factual information or unrelated readable text.
- The prompt asks for people, hands, wearing, operation, props, or scene extensions that do not serve the theme, product value, selected visual expression mode, or provided assets.

## Visual QA

Visual QA checks the generated image against the normalized task card and selected parameters.

Required action:

1. Read `references/visual-qa.md`.
2. Inspect the generated image against each required layer. When uploaded product images exist, explicitly compare the generated product against the uploaded product image before deciding `通过`.
3. Classify result as `通过`, `需定向重生`, or `需人工后期`.
4. If any layer fails and image generation is available, list the failed layer, concrete failure point, and passed layers to keep unchanged; then use one local targeted correction prompt from `generation-execution.md` and regenerate once by default. When the failed layer is `商品层` and the product no longer matches the uploaded product image, prefer the fixed product-fidelity correction prompt from `generation-execution.md` instead of rewriting the full brief.
5. Write the conclusion into `review.md` and user-facing notes.

Use this output shape:

```text
QA 结论：通过 / 需定向重生 / 需人工后期
保留项：{what works and should stay}
问题分层：{failed_layers_or_无}
修正项：{only failed items}
定向修正 Prompt：{targeted_retry_prompt_or_无}
```

## Technical QA

Technical QA is a simple deterministic check after saving files. No script is required by default.

PASS:

- Generated image path is recorded.
- `review.md` is saved when image generation runs.
- Test archive is outside the skill folder, under `<skill-parent>/zhuanzhuan-poster-prompt-test-cases/`.
- Output image can be opened or displayed by the current environment.
- Image aspect ratio matches requested `1:1`, `4:3`, `16:9`, or `2:1` when dimensions are inspectable.

FAIL:

- Generated image is missing or cannot be opened.
- `review.md` is missing after image generation.
- Archive was written inside `zhuanzhuan-poster-prompt/`.
- Inspectable image dimensions do not match requested format.

When Technical QA fails, fix file/archive issues once if possible. If image dimensions are wrong and image generation is available, regenerate once with a targeted format correction.
