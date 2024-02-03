# MM-ChatOcr

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Stargazers][stars-shield]][stars-url]


<br />
<!-- PROJECT LOGO -->


<p align="center">
  <a href="https://github.com/8baby8/internllm-ocr/">
    <img src="logo.png" alt="Logo" width="50%">
  </a>

<h3 align="center">mm-chatocr</h3>
  <p align="center">
    <br />
    <a href="https://github.com/8baby8/internllm-ocr"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://openxlab.org.cn/apps/detail/Farewell1/CHAT-OCR">查看Demo</a>
    ·
    <a href="https://github.com/8baby8/internllm-ocr/issues">报告Bug</a>
    ·
    <a href="https://github.com/8baby8/internllm-ocr/issues">提出新特性</a>
  </p>

</p>

<!-- 本篇README.md面向开发者 -->

**mm-chatocr** 是一个能够支持 **文字提取-特定字段提取** 的大模型，由 [InternLM2-chat-7B](https://github.com/InternLM/InternLM) 指令微调而来，欢迎大家star~⭐⭐

---

ChatOCR的核心思想是实现OCR模型提取文字信息，并使用LLM（Large Language Model）分析其识别结果，直接给出所关注的关键信息。

ChatOCR的工作原理主要基于OCR（Optical Character Recognition，光学字符识别）技术和大型语言模型（LLM）的结合。

- 首先，OCR模型被用来对输入图像进行文字检测和识别处理。在这个阶段，ChatOCR可能采用了一系列高级的OCR技术，如深度学习算法，来准确地检测和识别图像中的文字。这些文字信息随后被提取出来，作为后续处理的输入。

- 接下来，识别出的文字信息被送入大型语言模型进行处理。LLM具有强大的自然语言处理能力，可以理解并分析这些文字信息的含义。通过对文字信息的语义理解，LLM能够提取出关键信息，并生成相应的自然语言回复。

- 具体来说，ChatOCR可能首先使用OCR模型对图像进行预处理，将图像中的文字转换成机器可读的文本格式。然后，这些文本信息被送入LLM进行进一步的分析和处理。LLM可能会根据文本的语义内容和上下文信息，生成与输入图像相关的回复或执行相应的任务。

- 需要注意的是，ChatOCR的工作原理可能还涉及到其他一些技术和方法，如图像处理、文本预处理、自然语言生成等，以提高系统的准确性和效率。此外，具体的实现方式可能会因不同的应用场景和需求而有所差异。

### 最近更新
- 2024.2.3 完成mm-chatocr第一版并部署上线 https://openxlab.org.cn/apps/detail/Farewell1/CHAT-OCR 😀

## 目录

- [mm-chatocr](#关键信息提取大模型)
  - [开发前的配置要求](#开发前的配置要求)
  - [**使用指南**](#使用指南)
    - [数据构建](#数据构建)
    - [微调指南](#微调指南)
    - [部署指南](#部署指南)
    - [使用到的框架](#使用到的框架)
    - [如何参与本项目](#如何参与本项目)
    - [版本控制](#版本控制)
    - [作者（排名不分先后）](#作者排名不分先后)
    - [版权说明](#版权说明)
    - [特别鸣谢](#特别鸣谢)
  - [🌟 Contributors](#-contributors)

###### 开发前的配置要求

- 硬件：A100 40G（目前测试调节app.py中的参数显存推理时显存最低占用6G,使用Xtuner微调时占用16G左右）

###### **使用指南**

1. Clone the repo

```sh
git clone https://github.com/8baby8/internllm-ocr.git
```

2. 依次阅读或者选择感兴趣的部分阅读：
   - [数据构建](#数据构建)
   - [微调指南](#微调指南)
   - [部署指南](#部署指南)
   - 查看更多详情

<details>
<summary>更多详情</summary>


### 数据构建

请阅读[数据构建指南](generate_data/tutorial.md)查阅

本次微调用到的数据集见[datasets](datasets/data.json)

### 微调指南

详见[微调指南](xtuner_config/README.md)

### 部署指南

详见[部署指南](demo/README.md)

### 使用到的框架

- [Xtuner](https://github.com/InternLM/xtuner)
- [Transformers](https://github.com/huggingface/transformers)
- [Pytorch](https://pytorch.org/)
- …



#### 如何参与本项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

</details>

### 作者（排名不分先后）

[Farewell](https://github.com/8baby8)@飞桨星河社区UID:2460331

[侯玉鹏](https://aistudio.baidu.com/personalcenter/thirdview/2544861)@

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE](https://github.com/aJupyter/EmoLLM/blob/master/LICENSE)

### 特别鸣谢

- [上海人工智能实验室](https://www.shlab.org.cn/)
- [闻星大佬（小助手）](https://github.com/vansin)

<!-- links -->

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/in/aJupyter -->

<!-- 太少了，没必要放 -->

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=8baby8/internllm-ocr&type=Date)](https://star-history.com/#8baby8/internllm-ocr&Date)

## 🌟 Contributors

[![mm-chatocr contributors](https://contrib.rocks/image?repo=8baby8/internllm-ocr&max=50)](https://github.com/8baby8/internllm-ocr/graphs/contributors)

[your-project-path]: 8baby8/internllm-ocr
[contributors-shield]: https://img.shields.io/github/contributors/8baby8/internllm-ocr.svg?style=flat-square
[contributors-url]: https://github.com/8baby8/internllm-ocr/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/8baby8/internllm-ocr.svg?style=flat-square
[forks-url]: https://github.com/8baby8/internllm-ocr/network/members
[stars-shield]: https://img.shields.io/github/stars/8baby8/internllm-ocr.svg?style=flat-square
[stars-url]: https://github.com/8baby8/internllm-ocr/stargazers
[issues-shield]: https://img.shields.io/github/issues/8baby8/internllm-ocr.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/8baby8/internllm-ocr.svg
[license-shield]: https://img.shields.io/github/license/8baby8/internllm-ocr.svg?style=flat-square
[license-url]: https://github.com/8baby8/internllm-ocr/tree/main/LICENSE
