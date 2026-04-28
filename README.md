<div align="center">
    
[English](README.md) | [中文](README.zh.md)

</div>

<div align="center">

# AtomTopolo

**An Atomic Topology Agent System Prototype**

</div>

<div align="center">

[![Status](https://img.shields.io/badge/Status-Pre--Alpha--Prototype-orange)](https://github.com/cold-os/ColdOS)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![arXiv](https://img.shields.io/badge/arXiv-2512.08740-brightgreen.svg)](https://arxiv.org/abs/2512.08740)
[![DOI](https://img.shields.io/badge/DOI-10.6084/m9.figshare.31696846-blueviolet.svg)](https://doi.org/10.6084/m9.figshare.31696846)

</div>

Built upon the **RAMEN (Recursively Adversarial Meta-Execution Network)** and **Atomic Topology** architecture, this prototype demonstrates an intelligent diagnosis and prescription review system.

> ⚠️ **Warning**: This project is a **Pre-Alpha prototype**. The code relies heavily on AI-assisted generation and has not undergone any security audit. The medical scenario is entirely simulated; it involves no real diagnoses or patient data, and must not be taken as any form of medical reference. It exists solely to illustrate the concepts of Atomic Topology and RAMEN. **Use in any real decision-making or production environment is strictly prohibited.**

---

## Conceptual Overview

Current mainstream AI agents typically integrate perception, decision-making, and action within a unified framework—a design that has enabled significant advances in autonomy. At the same time, the industry has widely adopted safety training, permission controls, guardrails, and other mechanisms to address potential risks.

However, these approaches face a structural difficulty: the safety mechanisms themselves remain tightly coupled with model capabilities, relying on the model's "understanding" of and "compliance" with safety specifications. When safety depends on a probabilistic system whose internal states are not independently auditable, we face a gap that cannot be fully closed—a model may learn strategies to bypass safety constraints, and we lack verification means independent of the model itself to confirm whether safety mechanisms are genuinely effective.

If safety is internalized within the model rather than constructed as an independently auditable architectural layer, then in the worst case, the upper bound of safety assurance is constrained by the reliability and interpretability of the model itself. This observation is not a dismissal of existing work, but rather points toward a complementary possibility: whether there exists, alongside the model layer, an independent and deterministic path of constraint.

RAMEN shares the same intellectual origin as its predecessor, RAMTN, but shifts the focus from "cognitive reliability" to "execution controllability." Its core tenet is: **Do not trust the model's internals; instead, design an architecture in which unsafe behaviors are structurally impossible.**

### Atomic Topology

Agent capabilities are decomposed into indivisible atomic units, each granted only the minimum permissions necessary to perform its own function. Units share no internal state and communicate exclusively through structured JSON. Natively transparent interfaces allow any verification logic to deterministically judge whether a behavior is legitimate—without ever needing to understand the model's internals.

### RAMEN: Recursively Adversarial Meta-Execution Network

RAMEN evolves from **RAMTN (Recursively Adversarial Meta-Thinking Network)**:

- **RAMTN** addresses cognitive processes—improving reasoning reliability through a “construct–challenge–observe” adversarial topology.
- **RAMEN** addresses execution processes—enabling safety properties to emerge endogenously from the architecture through a “propose–review–execute” adversarial topology.

Both serve a common purpose: to constrain probabilistic models with deterministic logic.

---

## Demonstration Scenario

A simulated intelligent diagnosis and prescription review system.

The Diagnosis Proposer generates a diagnosis and medication recommendation based on patient data; the Prescription Reviewer checks the prescription's safety against hard-coded medical rules; the Safe Executor carries out the prescription only after approval. The three atoms each perform their own roles, with permissions strictly isolated.

The prototype illustrates a complete closed loop: the Diagnosis Proposer recommends an incorrect prescription, the Prescription Reviewer intercepts it according to built-in rules and provides feedback in the reverse direction, and the Diagnosis Proposer revises its proposal based on that feedback, which then passes review and is successfully executed.

---

## Core Conceptual Validation of the Prototype

### Validation Objective

This prototype aims to test one central hypothesis:

> When a unit capable of high-stakes decisions (determining a treatment plan) is stripped of execution rights, and the verification unit operates solely on deterministic rules without any model influence, the overall system can achieve a verifiable, auditable safety guarantee—without trusting the model.

This scenario does not capture full clinical complexity, but it completes a full safety loop—from error, to interception, to correction, to execution—on a minimal yet critical case (a penicillin-allergic patient recommended amoxicillin). Its structural design principles are transferable to other high-risk domains.

### Three-Layer Safety Structure

1. **Diagnosis Proposer**: May suggest a treatment plan but **has no authority to issue a prescription**.
2. **Prescription Reviewer**: Verifies prescription safety based on deterministic rules, but **has no authority to alter the diagnosis or execute the prescription**.
3. **Safe Executor**: Only carries out prescriptions that have passed review; **cannot access patient data or offer medical advice**.

The planner cannot execute, the executor cannot plan, and the reviewer is independent and deterministic. There exists no path to bypass verification.

### Communication and Composability

All units communicate through standardized JSON, with interfaces fully exposed. Each unit can be independently tested, replaced, or formally verified. When inputs and outputs are highly structured and verification categories are finite, atomic operations and their dedicated verification logic can be encapsulated as self-contained **Meta-Execution Units**—verification is no longer an external add-on but an organic component of execution. Based on such units, safety-oriented workflows for different scenarios can be constructed by rearranging their topological structures, providing a structural foundation for moving from “vertically specialized” toward “generally composable.”

---

## Demonstration Output

```text
================================================================================
Intelligent Diagnosis & Prescription Audit System - RAMEN Architecture Demo
Test Case: Closed-loop Diagnosis for a Patient with Penicillin Allergy
================================================================================

[Phase 1] Patient Data Input
Allergies: ['penicillin']
Chief Complaint: Fever and cough for 3 days

[Phase 2] First-Round Diagnosis - Diagnosis Proposer generates proposal (simulating model error)
Diagnosis: Upper Respiratory Tract Infection
Confidence: 0.85
Recommended Drug: Amoxicillin

[Phase 3] First-Round Audit - Prescription Reviewer checks against predefined rules
Verdict: rejected
Rationale: Patient has penicillin allergy; amoxicillin is contraindicated

[Phase 4] First-Round Execution - Safe Executor verifies execution preconditions
Result: Prescription blocked (audit not passed)

[Phase 5] Feedback Loop - Prescription Reviewer passes audit result back to Diagnosis Proposer
Feedback: Amoxicillin rejected | Patient allergies: [penicillin]

[Phase 6] Second-Round Diagnosis - Diagnosis Proposer revises proposal based on feedback
Revised Diagnosis: Community-Acquired Pneumonia (mild)
Confidence: 0.75
Revised Drug: Azithromycin
Reasoning: Fever with productive cough for 3 days, temperature 38.2°C, respiratory rate 20/min, consistent with CAP. History of diabetes increases infection risk. Penicillin allergy rules out beta-lactams. Bacterial pneumonia likely given symptoms and risk factors, though chest X-ray and CBC are unavailable, limiting confidence.

[Phase 7] Second-Round Audit - Prescription Reviewer checks revised prescription
Verdict: approved
Rationale: Prescription cleared all safety checks (whitelist, allergy, dosage, contraindications)

[Phase 8] Second-Round Execution - Safe Executor carries out the approved prescription
Result: Prescription issued — Azithromycin 500mg

[Phase 9] ColdReasoner Verification Report
Result: ✓ PASSED (9/9)
All message integrity, source authenticity, and execution precondition checks passed.

================================================================================
Key Audit Trail
================================================================================

[MSG 1] DiagnosisProposer → PrescriptionReviewer
Proposal | Diagnosis: URTI | Drug: Amoxicillin

[MSG 2] PrescriptionReviewer → SafeExecutor
Verdict: rejected | Reason: Penicillin allergy — amoxicillin contraindicated

[MSG 3] PrescriptionReviewer → DiagnosisProposer
Feedback: Rejected drug Amoxicillin | Allergies: [penicillin]

[MSG 4] DiagnosisProposer → PrescriptionReviewer
Revised Proposal | Diagnosis: CAP (mild) | Drug: Azithromycin

[MSG 5] PrescriptionReviewer → SafeExecutor
Verdict: approved | Reason: All safety checks passed

================================================================================
```

---

## Relationship to ColdOS

AtomTopolo is the engineering expression of the action-layer safety philosophy within the ColdOS ecosystem:

- It focuses on the migration of safety models from “post-hoc verification” toward “architecturally endogenous” safety;
- It provides a reference prototype that can be analyzed for establishing standardized interfaces for the ColdReasoner verification engine inside agents, moving verification logic from the ambiguity of natural language to precise positions in structured data;
- It explores composable, verifiable agent architectures based on atomic topology as a complementary path alongside mainstream frameworks.

---

## Acknowledgments and Disclaimer

This project was independently designed and implemented by Yiming Lu. The core concepts (RAMEN, Atomic Topology) were proposed by the author. Code and documentation were generated with AI assistance.

---

## Project Structure

```
AtomTopolo/
├── diagnosis_proposer.py     # Diagnosis Proposer
├── prescription_reviewer.py  # Prescription Reviewer
├── safe_executor.py          # Safe Executor
├── message_pipeline.py       # Message Pipeline & Audit Log
├── cold_reasoner.py          # ColdReasoner Verification
├── main.py                   # Main demonstration script
└── README.md
```

## Quick Start

```bash
pip install dashscope
export DASHSCOPE_API_KEY="your-key"
python main.py
```

## License

Apache 2.0
