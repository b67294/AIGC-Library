# 窗贴去背景：实现原理与复刻说明

核对日期：2026-09-09。

## 1. 项目实际采用的方法

当前常规去背景流程是：**纯白背景生产母版 → ComfyUI 的 RMBG-2.0 模型 → VITMatte 边缘细化 → 透明 RGBA PNG → 原样保留软 Alpha**。

具体通过 `LayerMask: LoadBiRefNetModelV2` 加载 `RMBG-2.0`，由 `LayerMask: BiRefNetUltraV2` 执行，开启 `process_detail`，选择 `VITMatte`。

### 1.1 RMBG-2.0 与 BiRefNet 的关系

准确名称是 **BiRefNet**，BiRefNet 全称为 *Bilateral Reference Network*，是一种面向高分辨率二分图像分割（Dichotomous Image Segmentation）的网络架构。它通过定位模块获得全局语义，再通过重建模块和双边参考机制恢复精细边缘，适合把图像分为“前景”和“背景”并生成蒙版。

RMBG-2.0 不是原始 BiRefNet 权重的另一个名字。
它是 BRIA AI 以 BiRefNet 为架构基础，结合 BRIA 自有数据集和训练方案训练出来的背景移除模型。可按以下关系理解：

```text
BiRefNet：网络架构和原始研究项目
    └── BRIA 使用 BiRefNet 架构 + 自有数据与训练方案
            └── RMBG-2.0：BRIA 发布的具体去背景模型权重
                    └── 本项目再使用 VITMatte 处理模型输出的边缘细节
```

因此，本项目的实际效果不能简单地用任意 `BiRefNet` 权重代替。复刻时要加载 `briaai/RMBG-2.0`，并继续使用当前工作流中的 VITMatte 细化参数。

官方资料地址：

- [BRIA RMBG-2.0 官方 Hugging Face 模型页](https://huggingface.co/briaai/RMBG-2.0)
- [RMBG-2.0 模型文件列表](https://huggingface.co/briaai/RMBG-2.0/tree/main)
- [原始 BiRefNet 官方 Hugging Face](https://huggingface.co/ZhengPeng7/BiRefNet)
- [原始 BiRefNet 官方 GitHub](https://github.com/ZhengPeng7/BiRefNet)
- [BiRefNet 论文：Bilateral Reference for High-Resolution Dichotomous Image Segmentation](https://arxiv.org/abs/2401.03407)

RMBG-2.0 的 Hugging Face 仓库包含 `birefnet.py`、`BiRefNet_config.py`、`model.safetensors`、PyTorch 权重和 ONNX 文件。模型页当前标注约 2 亿参数，主要权重文件约 885 MB。官方示例通过 Transformers 加载：

```python
from transformers import AutoModelForImageSegmentation

model = AutoModelForImageSegmentation.from_pretrained(
    "briaai/RMBG-2.0",
    trust_remote_code=True,
).eval()
```

## 2. 输入母版的约束

背景完全均匀为 `#ffffff`；

## 3. 完整 ComfyUI 工作流与参数

可直接复制或用于 API 调用的原始工作流附件：

- [birefnet-rmbg2-vitmatte-api.json](workflows/birefnet-rmbg2-vitmatte-api.json)

该附件与项目中的 `comfyui/BiRefNet.json`、服务端的 `birefnet_cutout.json` 内容一致。下面保留等效 JSON，方便只阅读本文档时直接核对参数。

下面是项目工作流的等效完整 API JSON。

```json
{
  "35": {
    "inputs": {"filename_prefix": "ComfyUI", "images": ["37", 0]},
    "class_type": "SaveImage"
  },
  "37": {
    "inputs": {
      "detail_method": "VITMatte",
      "detail_erode": 4,
      "detail_dilate": 3,
      "black_point": 0.01,
      "white_point": 0.99,
      "process_detail": true,
      "device": "cuda",
      "max_megapixels": 41.4,
      "image": ["49", 0],
      "birefnet_model": ["39", 0]
    },
    "class_type": "LayerMask: BiRefNetUltraV2"
  },
  "39": {
    "inputs": {"version": "RMBG-2.0"},
    "class_type": "LayerMask: LoadBiRefNetModelV2"
  },
  "49": {
    "inputs": {"url": "#{image}", "speak_and_recognation": true},
    "class_type": "LoadImagesFromURL"
  }
}
```

| 参数或连接 | 项目值 | 复刻时需要注意 |
|---|---|---|
| 模型版本 | `RMBG-2.0` | 通过上述加载节点使用 |
| 细节方法 | `VITMatte` | 使用该节点的细化实现 |
| `process_detail` | `true` | 开启边缘细化 |
| `detail_erode` / `detail_dilate` | `4` / `3` | 与细节区腐蚀、膨胀有关；先照抄数值 |
| `black_point` / `white_point` | `0.01` / `0.99` | 黑白端点控制；先保持不变 |
| `device` | `cuda` | 服务端需要可用的 CUDA 环境 |
| `max_megapixels` | `41.4` | 节点的处理规模参数，不代表强制输出 41.4 MP |
| URL 加载附加参数 | `speak_and_recognation=true` | 按原节点参数保留，不推断其内部作用 |
| 保存连接 | `35.images = ["37", 0]` | 保存节点 37 的第 0 个输出，不能误接为蒙版预览 |
