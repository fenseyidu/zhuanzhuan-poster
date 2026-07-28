# Business Rules v0.1

## Business Boundaries

| business_line_id | Boundary | Base Visual Tone | Default negative_rule_ids |
|-|-|-|-|
| `biz_n_category` | Interest consumption, professional gear, lifestyle and niche goods. | 内容审美、兴趣消费、商品专题感、轻生活方式或专业器材感。 | `neg_product_identity`, `neg_visual_clutter`, `neg_no_template_sale` |
| `biz_consumer_electronics` | Consumer electronics sale and conversion. | 干净、专业、商品清晰、轻科技、轻量文字信息层、低到中装饰密度；文字系统偏现代广告标题宋体或当代高对比中文 Serif 气质。 | `neg_product_identity`, `neg_no_unprovided_facts`, `neg_no_brand_hallucination` |
| `biz_recycle` | Idle item recycle service. | 可信、安全、简单省心、平台感、克制稳定；浅色简洁背景承托商品或回收对象，并继承少量产品自带色彩。 | `neg_business_recycle_not_sale`, `neg_service_claims_source`, `neg_no_unprovided_facts` |
| `biz_membership` | 转转平台会员日与会员季节活动；不包含第三方会员充值、点卡或权益卡。 | 高级、温暖、克制的会员活动感；A/S 默认使用暖金质感图生图底图与固定代码合成层。 | `neg_no_unprovided_facts`, `neg_membership_no_fixed_layer_redraw`, `neg_membership_no_third_party_card` |

## Visual Tone Inheritance

Use business line as the highest visual tone layer, then modulate with category, marketing type, product relation, product combination, composition, and background.

```text
business_line base_visual_tone
-> category semantic context
-> marketing intensity and information structure
-> product hierarchy and arrangement
-> composition energy
-> background carrier and continuity
```

Responsibilities:

- Business line decides the base aesthetic.
- Category explains what kind of content or usage context is appropriate.
- Marketing type changes strength and information density.
- Product relation and combination decide how products are displayed.
- Composition controls camera, perspective, and visual energy.
- Background recipe provides the carrier, but must not override the inherited tone.

## Visual Avoidance Notes

Use these as business-line tone boundaries. Formal prohibitions still come from `12_negative_rules.csv`; these notes help prevent positive prompt language from drifting.

- N 品类：避免纯折扣模板、无关通用舞台、没有品类逻辑的商品堆叠，以及不能解释兴趣或品类价值的背景装饰。
- 消费电子：保持干净、专业、商品识别清楚的商品呈现；科技感以材质、屏幕光、局部聚光、精致反射、深浅对比和主题色点睛体现。
- 回收：避免普通售卖海报语气、商品英雄式售卖重点、虚假官方保障、无来源服务承诺，以及遮蔽回收服务语义的价格优先促销表达。
- 会员：避免第三方充值卡语义、虚构会员等级/折扣/有效期/权益；固定标识、日期、规则按钮和底部弧形由合成层负责，不能让 AI 重画。

## Consumer Electronics Typography

For `biz_consumer_electronics`, use this typography direction in the final prompt when text style is helpful:

- Main title: modern advertising display Songti / contemporary high-contrast Chinese Serif feel.
- Weight: SemiBold to Heavy.
- Tracking: slightly expanded, about 4% - 8%.
- Line height: compact with breathing room, about 1.05 - 1.15.
- Character: stable structure, clear thick-thin contrast, broad and clean letterface, flat commercial-title feeling, suitable for consumer electronics.
- Color: use black, deep color, product/main brand color, or restrained two-color hierarchy when it improves recognition.
- Subtitle and benefit modules: inherit the same modern Chinese type feel, but use a more restrained hierarchy for readability.

This is a consumer electronics tone modulation only. Keep global text constraints from `12_negative_rules.csv`: front-facing flat typography, no outline, no shadow, no 3D, no metallic, no heavy gradient, and no over-pressing font weight.

## Recycle Typography

For `biz_recycle`, use this typography direction in the final prompt when text style is helpful:

- Main title: modern display Heiti / title Heiti feel.
- Weight: Heavy, with firm strokes and stable visual weight.
- Structure: upright, stable, slightly compact letterface, strong center of gravity, clear block-like rhythm, direct and trustworthy.
- Color: primarily black, near-black, deep blue, deep gray, or a product-derived accent color when the background is light enough for clear reading.
- Subtitle and subsidy line: use a lighter and more restrained hierarchy; subsidy numbers may use the product-derived accent color or business highlight color.
- Character: simple, direct, reliable, and easy to read, matching the `简单、省心、值得信任` recycle tone.

This is a recycle tone modulation only. Keep global text constraints from `12_negative_rules.csv`: front-facing flat typography, no outline, no shadow, no 3D, no metallic, no heavy gradient, and no over-pressing font weight.

## Facts That Must Come From User or Data

Resolve factual prohibitions through `12_negative_rules.csv`, especially `neg_no_unprovided_facts`, `neg_ranking_requires_source`, `neg_bundle_requires_source`, and `neg_service_claims_source`.

Facts that require user or data source:

- price
- subsidy amount
- coupon amount
- ranking
- sales number
- brand or exact model
- parameters
- activity date or countdown
- service promise
- bundle or giveaway relationship

If such facts appear in title/subtitle, preserve them but ask for confirmation when the source is unclear.

## Recycle Specific Rules

Recycle posters should emphasize:

- recyclable categories
- estimate or subsidy when provided
- platform trust
- inspection
- privacy
- payment
- process convenience

For current v0.1 recycle visual presets, B/A/S all resolve to the same B-level stable support route: simple light-toned background, clear product or recyclable object, product-color inheritance, restrained information layer, and the recycle title typography defined above.

For recycle light backgrounds, the support surface is optional. Prefer no visible platform when products can be held by light shadow, card grouping, or a continuous clean space. If a platform/tabletop is needed, use at most one continuous support surface. Do not create two or more separated podiums, round platforms, stone blocks, trays, or support blocks.

For recycle multi-category posters, default to `combo_multi_recyclable / 多品类回收组合` as a staggered product-led group rather than a card matrix. When there are exactly 2 products or categories, do not force a main/support hierarchy; keep both products at reasonable visual weight and create stagger through front/back, high/low, size, angle, light perspective, slight overlap, or visibly offset bottom edges. Avoid aligned bottom edges, equal-height side-by-side placement, or ordinary product-pair posing. When there are 3 or more products or categories, one main recyclable object may be larger and clearer while supporting objects form front/back, high/low, size, angle, and light-perspective variation. All products share the same light, shadow, and continuous background. Use cards, icon grids, entrance matrices, or flow-node grouping only when the user explicitly asks for them or when the information structure requires it.

For recycle prohibitions, use `neg_business_recycle_not_sale`, `neg_service_claims_source`, and `neg_no_unprovided_facts` from `12_negative_rules.csv`.

## Visual Defaults

Default user preference for v0.1 is inherited from the selected business line, then modulated by marketing type:

```text
base_visual_tone: 来自 01_business_lines.csv
marketing_intensity: 根据营销类型调节
visual_cleanliness: 默认适中偏干净；消费电子和回收优先更干净稳定
info_density: 中
decoration_density: 低到中
```

Use stronger marketing for flash sale, subsidy, and ranking only within the business-line tone. Use cleaner, more stable visuals for service trust, professional recommendation, premium categories, consumer electronics single-product showcases, and recycle.
