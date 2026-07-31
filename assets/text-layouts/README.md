# 文字版式 Profiles

`registry.json` 是所有文字合成路线的唯一入口。每个 profile 必须声明业务线、档位、规格、执行 pipeline，以及主副标题来源；调用方只能用 profile ID，不能依赖 renderer 默认值。

## 路线边界

- `membership-b-2x1`：会员 B 的 2:1 本地标题路线。`text_layout_renderer.py` 先绘制标题组并输出标题坐标，随后会员 renderer 在主标题上方左对齐增加会员标识。
- `membership-as-2x1`：会员 A 使用独立透明标题资产和固定会员日层，不能复用回收文字 profile。
- `membership-s-2x1`：会员 S 使用 `membership_s_renderer.py` 和 `membership-head-template/profiles/membership-s-2x1.json`；主标题与副标题均由调用方传入，共用 580px 参考文字区，超宽折行且每行水平居中。主标题仅在包含 X/x/× 且两侧都有文字时采用“左文案 × 右文案”布局，否则原样渲染且不添加 ×。完整会员 logo、标题、副标题作为一组在画面垂直居中，标识与文字颜色由背景采样结果决定。

新增路线时，先在 `registry.json` 注册，再在对应业务线目录新增 JSON profile；不要在 Python 中增加业务线 `if/else` 或复用其他路线的默认字体、坐标和换行规则。
