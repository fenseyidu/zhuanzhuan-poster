# 文字版式 Profiles

`registry.json` 是所有文字合成路线的唯一入口。每个 profile 必须声明业务线、档位、规格、执行 pipeline，以及主副标题来源；调用方只能用 profile ID，不能依赖 renderer 默认值。

## 路线边界

- `membership-b-2x1`：会员 B 的 2:1 本地标题路线。`text_layout_renderer.py` 先绘制标题组并输出标题坐标，随后会员 renderer 在主标题上方左对齐增加会员标识。
- `membership-as-2x1`：会员 A/S 使用独立透明标题资产和固定会员日层，不能复用回收文字 profile。

新增路线时，先在 `registry.json` 注册，再在对应业务线目录新增 JSON profile；不要在 Python 中增加业务线 `if/else` 或复用其他路线的默认字体、坐标和换行规则。
