# 参考图素材板生成

把一张复杂参考图转换为“元素清单 → 分板计划 → 逐板提示词 → Sheet 图片”。模块到 Sheet 图片为止，不负责去背景、切割、坐标记录、排版或无缝处理。

## 一句话流程

```text
参考图 → AI 列元素清单 → 分板 → 编译提示词 → 宿主生图 → Sheet PNG
```

## 输入

| 输入 | 必需 | 说明 |
|---|---|---|
| `reference` | 是 | 本地参考图路径或可访问 URL |
| `style` | 是 | 从参考图概括出的共同画风 |
| `assets` | 是 | 不同视觉原型的 ID 与描述 |
| `sheets` | 是 | 每张板的行列数和资产顺序 |
| `sheet_defaults` | 否 | 留白、背景和共同生成要求 |

AI 负责查看参考图并填写 `assets`。同一种视觉原型只写一次；原图中出现几次不在本模块记录。

## 输出

```text
plan.json
prompts/SHEET_ID.txt
sheets/SHEET_ID.png
```

- `plan.json`：可以人工检查和修改的清单与分板计划。
- `prompts/`：确定性编译出的实际生图提示词。
- `sheets/`：宿主生图工具返回的素材板。

输出 Sheet 后模块结束。背景是否真实透明、怎样去底以及怎样切格，由后续独立模块处理。

## 使用

1. 复制 [`examples/butterfly-mail-plan.json`](examples/butterfly-mail-plan.json) 为任务的 `plan.json`。
2. 让 AI 查看参考图，修改 `style`、`assets` 和 `sheets`。
3. 编译并检查提示词：

   ```powershell
   python scripts/compile_prompts.py TASK\plan.json
   ```

4. 对每个 `prompts/*.txt`，把原始参考图和该提示词一起交给宿主生图工具。
5. 按 `sheets[].output_file` 保存返回图片，到此结束。

编译器只验证 ID、分板容量、资产覆盖关系和路径，不会擅自识别、合并或删除视觉元素。

## 计划约束

- `assets[].id`、`sheets[].id` 必须唯一，只使用英文字母、数字、短横线和下划线。
- 每个资产必须且只能出现在一张初始 Sheet 中。
- `asset_ids` 的顺序就是从左到右、从上到下的格子顺序。
- 单板资产数不能超过 `columns × rows` 和 `max_assets_per_sheet`。
- 不要加入 `instances`、`bbox`、`same_as` 或其他排版字段。

完整机器可读格式见 [`plan.schema.json`](plan.schema.json)。

## 当前状态

`candidate`。鸟类案例和非鸟类蝴蝶信件案例均已生成 Sheet；清单、分板、提示词编译和语义内容正确。非鸟类案例两张图都出现了不透明棋盘格，证明透明要求不能仅靠提示词保证，但去底仍留给后续独立模块。详情见 [`examples/test-report.md`](examples/test-report.md)。
