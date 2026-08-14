<div align="center">

[English](README.md) | [中文](README.zh.md)

# ColdTriad

### L4 · Governance — the Separation-of-Powers Layer of the Cold Trust Protocol Stack

[![Status](https://img.shields.io/badge/Status-Pre--Alpha--Prototype-orange)](https://github.com/cold-os/ColdTriad)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Field](https://img.shields.io/badge/Field-CSS%20%7C%20HCI-6f42c1.svg)](https://github.com/cold-os)
[![arXiv](https://img.shields.io/badge/arXiv-2512.08740-brightgreen.svg)](https://arxiv.org/abs/2512.08740)
[![DOI](https://img.shields.io/badge/DOI-10.6084/m9.figshare.31696846-blueviolet.svg)](https://doi.org/10.6084/m9.figshare.31696846)

</div>

> **Layer:** L4 · Governance — Cold Trust Protocol Stack  
> **Research Question:** How can unsafe actions be made *structurally* impossible?  
> **Method:** Separation of powers applied to agents — a proposer that cannot execute, a deterministic reviewer that cannot act, an executor that only runs approved actions (default-deny).  
> **Status:** Pre-alpha prototype · not for production use.  
> **Related:** [ColdReasoner](https://github.com/cold-os/ColdReasoner) (L3) · [Cold Trust Protocol Stack](https://github.com/cold-os) · arXiv:2512.08740 · figshare:31696846

---

## 🧊 What It Is

ColdTriad applies the principle of **separation of powers** to AI agents. Built on **RAMEN (Recursive Adversarial Meta-Execution Network)** and **atomic topology**, it demonstrates a governance architecture in which **unsafe behavior is structurally impossible — not merely discouraged**. The proposer cannot execute, the executor cannot propose, and the reviewer is independent and deterministic.

> **⚠️ Pre-Alpha:** this is a fully simulated prototype (medical scenario only); code is heavily AI-assisted and not security-audited. **Not for any real decision-making or production use.**

## 🎯 The Structural Problem It Addresses

Mainstream agent designs couple safety mechanisms to the model's own capability — safety depends on the model "understanding and obeying" rules. When safety lives inside an un-auditable probabilistic system, the gap can never be fully closed: the model may learn to bypass its constraints, and there is no model-independent way to verify that the safety mechanism actually holds.

RAMEN shares its origin with RAMTN but shifts the focus from **cognitive reliability** to **execution controllability**:

- **RAMTN** — adversarial topology over *cognition* (construct · challenge · observe).
- **RAMEN** — adversarial topology over *execution* (propose · review · execute).

Both serve one goal: **constrain a probabilistic model with deterministic logic.**

## 🎭 Three-Layer Separation (the triad)

1. **Proposer** — may generate plans, but **cannot execute**.
2. **Reviewer** — deterministic rules only; **cannot act or modify** the proposal.
3. **Executor** — runs **only approved** actions; **blind** to source data and proposals.

The one who decides cannot execute; the one who executes cannot decide; the reviewer is independent and deterministic. **There is no path around the check.**

## 🩺 A Minimal Governance Case Study

A simulated intelligent diagnosis and prescription-review system: a penicillin-allergic patient is recommended amoxicillin.

```
[1] Proposer suggests:  amoxicillin            →  ❌ Reviewer rejects (penicillin allergy)
[2] Reviewer feeds back: "penicillin allergy — amoxicillin prohibited"
[3] Proposer revises:    azithromycin          →  ✅ Reviewer approves (all checks passed)
[4] Executor runs:       azithromycin 500mg    →  ColdReasoner verification: pass (9/9)
```

A complete closed loop — **error → interception → feedback → correction → execution** — on a minimal but life-critical case, with every message recorded in the audit log. The structural principle transfers to other high-risk domains.

## 🔍 Why It Matters

- **AI governance:** separation of powers is an institutional-design pattern made *architectural*; default-deny is the governance default. Enforcement precedes the model.
- **Computational social science:** the triad is a sociotechnical power distribution — proposal/review/execute traces are data on error-correction and control dynamics in human–AI systems.
- **HCI:** the topology makes "who can do what" legible to the human — the human is the ultimate auditor.

## 🔧 Composability

All units communicate via standardized JSON with fully exposed interfaces. Each unit can be independently tested, replaced, or formally verified — the foundation for composing triads into larger safety workflows across domains.

## 🚀 Quick Start

```bash
pip install dashscope
export DASHSCOPE_API_KEY="your-key"
python main.py
```

## 🧪 Status & Limitations

Pre-alpha concept prototype; the medical scenario is fully simulated (no real patients or data); no security audit; **no empirical studies yet** — the error–intercept–correction traces it produces are intended as data for computational analysis (CSS), and its triadic structure as a subject of human-oversight studies (HCI).

## 🛣️ Roadmap

1. **CSS:** computational analysis of triad traces — error-detection rates, correction-loop dynamics.
2. **HCI:** user studies on human oversight of triadic agent systems.
3. Compose triads into larger, reusable governance workflows.

## 📜 Acknowledgement & Statement

Core ideas (RAMEN, atomic topology) were proposed by the author; code and documentation were AI-assisted.

## 📄 License

Apache 2.0

---

*Part of the [Cold Trust Protocol Stack](https://github.com/cold-os) — trust protocols for human–AI interaction, anchored in computational social science.*
