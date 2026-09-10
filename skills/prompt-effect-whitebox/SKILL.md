---
name: prompt-effect-whitebox
description: Explain an already implemented effect as a concise, reusable white-box mental model for developers. Use only when explicitly invoked after an effect or feature already works.
---

# Effect Whitebox

当一个效果已经实现后，不要只解释代码怎么写。站在开发者角度，把它拆解成可理解、可复用的白盒心智模型。

## 输出内容

1. **核心原理**
   - 这个效果本质上如何成立。
   - 用简单语言说明背后的机制。
2. **技术骨架**
   - 列出实际依赖的具体技术栈、框架、SDK、模块或能力。
   - 说明各部分分别负责什么。
3. **实现流程**
   - 从输入到最终效果说明主要步骤。
   - 用一个简单流程呈现整体结构。
4. **可复用部分**
   - 区分通用骨架与当前实现特有部分。
   - 说明以后面对类似效果时可以迁移哪些思路。
5. **掌握边界**
   - 说明开发者至少应该理解的概念。
   - 指出当前不必深入的底层细节。

## 目标与风格

让用户理解：效果为什么能成立、由什么组成、各部分如何协作，以及下次如何迁移。保持简洁、易懂，不用过多底层细节淹没用户，也不要只给代码。

