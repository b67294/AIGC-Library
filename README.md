# AIGC Library

个人 AIGC 工程资产库，由 Git 统一管理。

```text
AIGC-Library/
├── HOME.md          Obsidian 首页
├── library.base     可筛选的资产卡片库
├── aigc-map.canvas  可点击源文件的视觉资产总览
├── catalog/         展示索引卡，不承载源内容
├── modules/         可复用的算法、工作流和工程模块
└── skills/          可由 Codex 显式调用的个人 Skill
```

## 打开方式

公开仓库的本地位置是 `F:\AIGC-Hub\public`。统一浏览时，在 Obsidian 中选择 **Open folder as vault**，打开 `F:\AIGC-Hub`，然后进入 `private/views/HOME.md`。完成一次注册后，可以双击 `Open-AIGC-Library.url` 直接回到统一首页。

内容与展示保持分离：`skills/` 和 `modules/` 是可复制的源资产，`catalog/`、`.base` 和 `.canvas` 只是可替换的展示层。

当前 Skill：

- `prompt-explore-solutions`：实现前先探索成熟方案与完整选项空间。
- `prompt-effect-whitebox`：将已实现的效果拆解为可理解、可复用的白盒心智模型。
- `prompt-debug-explain`：修复问题的同时解释成因、判断依据和修复原理。
- `module-reuse-reviewer`：评估项目模块的复用潜力并生成透明可验证的候选知识卡。

当前 Module：

- `background-removal`：RMBG-2.0、BiRefNet 与 VITMatte 去背景流程。
