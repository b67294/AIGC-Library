---
name: prompt-debug-explain
description: Explain why a software problem happened, how the diagnosis was reached, and why the proposed fix works. Use only when explicitly invoked together with an error, symptom, or relevant code.
---

# Debug Explain

用户遇到下面的问题时，不要只给出修改结果。用不熟悉这部分实现的开发者也能听懂的语言，简洁说明：

1. **为什么发生**：区分表面现象与真正原因，并指出触发条件。
2. **判断依据**：说明从哪些报错、代码或行为得出结论。
3. **如何解决**：给出修复方法，并解释修改为什么有效。
4. **验证与预防**：说明怎样确认已经修好，以及以后如何避免。

明确区分已经确认的事实与推测。信息不足时，先指出缺少的最小信息，不要把猜测写成结论。

保持简短、通俗；代码只服务于解释和修复，不要让代码取代原因说明。
