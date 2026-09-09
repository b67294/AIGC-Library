---
name: prompt-explore-solutions
description: Explore mature, commonly used solution options before implementation. Use only when explicitly invoked to compare approaches, dependencies, trade-offs, and switching conditions before choosing a solution.
---

# Explore Solutions

在开始实现前，先探索问题当前已有的成熟解决方案与完整选项空间。不要写代码，也不要过早锁定单一技术路线。

## 工作方式

1. 搜索并核实当前成熟、常用且有人实际采用的开源项目、模型、算法、框架、工具或现成模块。优先使用一手资料，并为时效性或技术性结论提供来源。
2. 给出至少三个有代表性的可行方案；如果不足三个真正实用的选择，应如实说明，不为凑数加入明显不适用的方案。
3. 对每个方案说明：适用场景、必要前提、依赖与限制、实现和使用复杂度，以及效果、速度和成本等关键差异。
4. 解释方案之间的关系，包括主流默认、轻量或低成本方案、备用方案、补充或后处理方案，以及从一个方案切换到另一个方案的条件。
5. 最后根据用户已经提供的实际条件给出推荐与理由，并说明条件变化后应考虑的其他方案。

## 约束

- 不替用户假设未提供的关键条件。
- 当不同前提会导致不同结论时，分别列出对应分支。
- 如果用户当前思路已局限于某条技术路线，主动指出更成熟或不同路线。
- 本轮目标是帮助用户决定做什么，而不是直接开始实现。

