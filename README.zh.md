<div align="center">

[English](README.md) | [中文](README.zh.md)

# ColdTriad

### L4 · 治理层 —— Cold Trust Protocol Stack 的分权制衡层

[![Status](https://img.shields.io/badge/Status-Pre--Alpha--Prototype-orange)](https://github.com/cold-os/ColdTriad)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Field](https://img.shields.io/badge/Field-CSS%20%7C%20HCI-6f42c1.svg)](https://github.com/cold-os)
[![arXiv](https://img.shields.io/badge/arXiv-2512.08740-brightgreen.svg)](https://arxiv.org/abs/2512.08740)
[![DOI](https://img.shields.io/badge/DOI-10.6084/m9.figshare.31696846-blueviolet.svg)](https://doi.org/10.6084/m9.figshare.31696846)

</div>

> **层次：** L4 · 治理层 —— Cold Trust Protocol Stack  
> **研究问题：** 如何让不安全的行为*结构上*不可能发生？  
> **方法：** 面向智能体的分权制衡——不能执行的提案者、不能行动的确定性审查者、只执行已批准操作的执行者（默认拒绝）  
> **状态：** Pre-alpha 原型 · 不适用于生产环境  
> **关联：** [ColdReasoner](https://github.com/cold-os/ColdReasoner)（L3）· [Cold Trust Protocol Stack](https://github.com/cold-os) · arXiv:2512.08740 · figshare:31696846

---

## 🧊 它是什么

ColdTriad 把**分权制衡**这一原则应用于 AI 智能体。基于 **RAMEN（递归对抗元执行网络）** 与**原子化拓扑**，它演示了一种治理架构：**不安全的行为在结构上不可能发生——而不只是被劝阻**。提案者不能执行，执行者不能提案，审查者独立且确定性。

> **⚠️ Pre-Alpha：** 本项目为完全模拟的原型（仅医学场景）；代码重度依赖AI辅助生成，未经安全审查。**严禁用于任何真实决策与生产环境。**

## 🎯 它回应的结构性问题

主流智能体设计把安全机制与模型自身能力耦合在一起——安全依赖于模型"理解并遵守"规则。当安全内化于一个不可审计的概率系统内部时，缺口永远无法彻底闭合：模型可能习得绕过约束的策略，而我们缺乏独立于模型之外的验证手段。

RAMEN 与 RAMTN 共享同一思想源头，但把关注点从**认知可靠性**迁移至**执行可控性**：

- **RAMTN** —— 在*认知*之上构建对抗拓扑（建构 · 质疑 · 观察）。
- **RAMEN** —— 在*执行*之上构建对抗拓扑（提议 · 审核 · 执行）。

两者共同服务于同一个目标：**用确定性的逻辑约束概率性的模型。**

## 🎭 三层分权（三权分立）

1. **提案者** —— 可以提出方案，但**无权执行**。
2. **审查者** —— 仅运行确定性规则；**无权行动，也无权修改提案**。
3. **执行者** —— 只执行**已批准**的操作；对源数据与提案**不可见**。

决定者不能执行，执行者不能决定，审查者独立且确定性。**不存在绕过校验的路径。**

## 🩺 一个最小的治理案例

模拟一个智能诊断与处方辅助审核系统：青霉素过敏患者被推荐阿莫西林。

```
[1] 提案者建议：  阿莫西林             →  ❌ 审查者拒绝（青霉素过敏）
[2] 审查者反馈："青霉素过敏——禁用阿莫西林"
[3] 提案者修正：  阿奇霉素             →  ✅ 审查者批准（全部检查通过）
[4] 执行者执行：  阿奇霉素 500mg       →  ColdReasoner 验证：通过（9/9）
```

在一个极简但性命攸关的案例上完成了**犯错 → 拦截 → 反馈 → 修正 → 执行**的完整闭环，每一条消息都记录在审计日志中。其结构原则可迁移至其他高风险领域。

## 🔍 为什么它重要

- **AI 治理：** 分权制衡是制度设计模式，被做成了*架构属性*；默认拒绝就是治理的默认值。执法先于模型。
- **计算社会科学：** 三权结构是一种社会技术权力分配——提案/审核/执行轨迹，是研究人机系统中纠错与控制动力学的数据。
- **人机交互：** 拓扑让"谁能做什么"对人清晰可见——人类是最终的审计者。

## 🔧 可组装性

所有单元通过标准化 JSON 通信，接口完全对外暴露。每个单元可被独立测试、替换或形式化验证——这是把三权结构组装成跨领域更大安全工作流的基础。

## 🚀 快速开始

```bash
pip install dashscope
export DASHSCOPE_API_KEY="your-key"
python main.py
```

## 🧪 现状与局限

Pre-alpha 概念原型；医学场景完全模拟（无真实患者或数据）；未经安全审查；**尚无实证研究**——它产出的"犯错—拦截—修正"轨迹计划用作计算分析的数据（CSS），其分权结构计划作为人类监督研究的对象（HCI）。

## 🛣️ 路线图

1. **CSS：** 对三权轨迹的计算分析——错误检出率、纠错循环动力学。
2. **HCI：** 人类监督分权智能体系统的用户研究。
3. 把三权结构组装成更大、可复用的治理工作流。

## 📜 致谢与声明

核心理念（RAMEN、原子化拓扑）由作者提出，代码与文档由 AI 辅助生成。

## 📄 许可证

Apache 2.0

---

*隶属于 [Cold Trust Protocol Stack](https://github.com/cold-os)——以计算社会科学为锚的人机交互信任协议。*
