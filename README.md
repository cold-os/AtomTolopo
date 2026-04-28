# AtomTopolo

**An Atomic Topology Agent System Prototype**

Built upon the **RAMEN (Recursively Adversarial Meta-Execution Network)** and **Atomic Topology** architecture, this prototype demonstrates an intelligent diagnosis and prescription review system.

> ⚠️ **Warning**: This project is a **Pre-Alpha prototype**. The code relies heavily on AI-assisted generation and has not undergone any security audit. The medical scenario is entirely simulated; it involves no real diagnoses or patient data, and must not be taken as any form of medical reference. It exists solely to illustrate the concepts of Atomic Topology and RAMEN. **Use in any real decision-making or production environment is strictly prohibited.**

---

## Conceptual Overview

Mainstream AI agents tightly couple perception, decision-making, and action within a single framework. When one model is responsible both for understanding the world and for executing operations, safety can only depend on the model's own "character"—something we cannot audit, cannot verify, and cannot trust.

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
Intelligent Diagnosis & Prescription Review System
RAMEN Architecture Bidirectional Communication Demo
Test Case: Closed-Loop Diagnosis for a Penicillin-Allergic Patient
================================================================================

[Phase 1] Patient data input
Patient allergies: ['penicillin']
Chief complaint: fever, cough for 3 days

[Phase 2] First-round diagnosis – Diagnosis Proposer generates a proposal (simulating a large model error)
Diagnosis: Upper respiratory tract infection
Confidence: 0.85
Recommended drug: Amoxicillin

[Phase 3] First-round review – Prescription Reviewer evaluates the prescription
Verdict: rejected
Rationale: Patient is allergic to penicillin; amoxicillin is contraindicated

[Phase 4] First-round execution – Safe Executor attempts to execute the prescription
Result: Prescription blocked (review not passed)

[Phase 5] Feedback loop – Prescription Reviewer sends the interception information back to the Diagnosis Proposer
Feedback: Amoxicillin rejected; patient allergies: [penicillin]

[Phase 6] Second-round diagnosis – Diagnosis Proposer revises the proposal based on feedback
Revised diagnosis: Acute bacterial bronchitis
Confidence: 0.75
Revised recommended drug: Azithromycin
Reasoning: The patient presents with fever and productive cough with white sputum for 3 days, consistent with an acute respiratory infection. A history of diabetes increases the risk of bacterial infection, but the absence of typical pneumonia signs (chest pain, dyspnea) and imaging evidence does not support a pneumonia diagnosis at this time. Penicillin allergy requires avoidance of β-lactam antibiotics; considering common community-acquired respiratory pathogens, an atypical pathogen or susceptible bacterial infection is more likely.

[Phase 7] Second-round review – Prescription Reviewer evaluates the revised prescription
Verdict: approved
Rationale: Prescription complies with safety rules

[Phase 8] Second-round execution – Safe Executor carries out the revised prescription
Result: Prescription issued: Azithromycin 500mg

[Phase 9] Complete audit log output

================================================================================
Audit Log
================================================================================

[MSG 1] DiagnosisProposer → PrescriptionReviewer
Proposal | Diagnosis: Upper respiratory tract infection | Recommended drug: Amoxicillin

[MSG 2] PrescriptionReviewer → SafeExecutor
Review result: rejected | Reason: Patient is allergic to penicillin; amoxicillin is contraindicated

[MSG 3] PrescriptionReviewer → DiagnosisProposer
Feedback: Rejected drug Amoxicillin | Patient allergies: [penicillin]

[MSG 4] DiagnosisProposer → PrescriptionReviewer
Revised proposal | Diagnosis: Acute bacterial bronchitis | Recommended drug: Azithromycin

[MSG 5] PrescriptionReviewer → SafeExecutor
Review result: approved | Reason: Prescription complies with safety rules

================================================================================

[Phase 10] ColdReasoner Verification Report
Verification result: Passed (9/9)
All message integrity, source legitimacy, and execution precondition checks passed.
```

---

## Relationship to ColdOS

AtomTopolo is the engineering expression of the action-layer safety philosophy within the ColdOS ecosystem:

- It focuses on the migration of safety models from “post-hoc verification” toward “architecturally endogenous” safety;
- It provides a reference prototype that can be analyzed for establishing standardized interfaces for the ColdReasoner verification engine inside agents, moving verification logic from the ambiguity of natural language to precise positions in structured data;
- It explores the paradigm shift of agent architectures from monolithic black boxes toward composable, verifiable atomic topologies.

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