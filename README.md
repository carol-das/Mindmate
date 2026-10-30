# MindMate: The Privacy-First AI Mediator

**A local, confidential AI preparation space designed to help individuals organize their thoughts, navigate emotional complexities, and transition into professional human therapy.**

---

## 1. Executive Overview

The therapeutic environment is inherently personal and requires a high degree of trust. Individuals may find it difficult to express their vulnerabilities, organize their thoughts, or prepare for professional consultations.

**MindMate** addresses this challenge through a Privacy-First AI Mediator.

Rather than functioning as an autonomous AI therapist, MindMate acts as a supportive bridge between self-reflection and professional human care.

The platform provides:
- A private environment for preliminary self-reflection.
- Context-aware, empathetic conversations.
- Structured pre-session summaries for human therapists.
- Local mood tracking and personal reflection storage.
- Access to relevant human therapist directories.
- Safety mechanisms for identifying potentially high-risk interactions.

Its primary objective is to facilitate meaningful preparation for professional mental healthcare while prioritizing user privacy and data ownership.

## 2. Problem Statement

Existing AI conversational applications raise important concerns regarding sensitive personal information, clinical reliability, and dependence on automated responses.

Individuals may also struggle to communicate their emotional concerns effectively during their first interaction with a mental health professional.

MindMate explores an alternative approach: a locally executed AI mediator that helps users organize their thoughts and prepare for human clinical engagement without attempting to diagnose or independently treat psychological conditions.

## 3. Core Innovation and Novelty

MindMate introduces a **Privacy-First AI Mediation Framework** built around three principles:

### 3.1 AI as a Mediator, Not a Therapist

Unlike autonomous AI therapy applications, MindMate focuses on preliminary reflection and therapy preparation.

It converts multi-turn conversations into structured summaries containing:
- Primary Concerns
- Emotional Themes
- Key Questions for Clinical Intake

These summaries can help users communicate their concerns during professional consultations.

### 3.2 The Sensitive Cubicle Privacy Framework

MindMate emphasizes local execution and user-controlled data storage.

- **Local Inference:** Uses Ollama to execute language-model inference on the user's local machine.
- **Local Data Storage:** Stores mood records and reflection notes in a local SQLite database.
- **Data Ownership:** Allows users to view, edit and permanently erase their stored reflection history.
- **Safety Interception:** Uses Llama Guard 3 and Prompt Guard as safety mechanisms.

### 3.3 Human-in-the-Loop Mental Healthcare

MindMate encourages professional human engagement instead of positioning AI as a replacement for clinicians.

The platform connects users to relevant therapist directories and supports preparation for professional consultations.

## 4. Core Application Features

The Streamlit interface (`app.py`) is organized into three primary modules.

### 4.1 Reflection Space

An empathetic conversational environment designed to help users reflect on their concerns.

**Features:**
- Context-aware, non-judgmental conversational responses.
- Quick-prompt starters such as:
  - Feeling overwhelmed
  - Hesitant about therapy
  - Hard to express feelings
- Multi-turn conversational interaction.
- Automated pre-session summary generation.

### 4.2 Private Mood Vault

A personal space for recording and reviewing emotional check-ins.

**Features:**
- Daily mood tracking using a 1–5 slider.
- Custom reflection notes.
- Local storage using SQLite.
- Tabular viewing of recorded reflections.
- One-click data deletion through `purge_vault()`.

### 4.3 Human Therapist Directory

A directory designed to help users explore professional mental healthcare resources.

**Features:**
- Filtering practitioner profiles by primary concern.
- Categories include Anxiety, Burnout, Work Stress, Life Transitions and Overwhelm.
- Links to external healthcare directories:
  - Psychology Today
  - SAMHSA Behavioral Health Locator
  - Association for Behavioral and Cognitive Therapies (ABCT).

## 5. System Architecture

MindMate follows a modular architecture consisting of the following components:

1. **User Interface Layer:** Streamlit-based interface for conversational interaction, mood tracking and therapist discovery.
2. **Inference Layer:** Ollama-based local language-model execution.
3. **Safety Layer:** Input and output safety interception using Llama Guard 3 and Prompt Guard.
4. **Summary Generation Layer:** Converts conversational history into structured pre-session summaries.
5. **Data Management Layer:** SQLite-based storage and management of mood records and reflection notes.
6. **Therapist Matching Layer:** Filters practitioner profiles and provides external healthcare resources.

### High-Level Workflow

```text
              USER
                |
                v
        STREAMLIT INTERFACE
                |
       +--------+--------+
       |        |        |
       v        v        v
   Reflection  Mood   Therapist
     Space     Vault   Directory
       |
       v
   Safety Guard
       |
       v
   Ollama Local LLM
       |
       v
   Conversational Response
       |
       v
   Summary Engine
       |
       v
   Pre-Session Summary
       |
       v
   HUMAN THERAPIST
```

## 6. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend / UI | Streamlit |
| Local LLM Runtime | Ollama |
| Language Model | Llama 3.1 8B Instruct Mental Health Classification |
| Model Format | Quantized GGUF |
| Safety Mechanisms | Llama Guard 3, Prompt Guard |
| Database | SQLite |
| Data Processing | Pandas |
| Version Control | Git and GitHub |

## 7. Project Directory Structure

```text
MindMate/
│
├── app.py
├── Modelfile
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── mindmate_vault.db
│
└── src/
    ├── inference.py
    ├── safety_guard.py
    ├── summary_engine.py
    ├── memory_vault.py
    └── therapist_match.py
```

**Module descriptions:**

| File | Responsibility |
|---|---|
| `app.py` | Main Streamlit application and interface |
| `Modelfile` | Ollama model configuration and system prompts |
| `inference.py` | Local LLM inference |
| `safety_guard.py` | Safety interception and filtering |
| `summary_engine.py` | Structured pre-session summary generation |
| `memory_vault.py` | SQLite storage, mood logging and data deletion |
| `therapist_match.py` | Therapist directory filtering and care resources |

The local database and model weights are excluded from Git tracking.

## 8. Installation and Setup

### Prerequisites

- Python 3.10, 3.11 or 3.12
- Git
- Ollama
- Sufficient local storage and memory for the selected language model

### Step 1: Clone the Repository

```bash
git clone https://github.com/carol-das/Mindmate.git
cd Mindmate
```

### Step 2: Install Dependencies

```bash
pip install streamlit pandas ollama
```

Alternatively, install the dependencies listed in the project requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Configure Ollama

Install Ollama and ensure its local service is running.

For the standard Llama 3.1 8B model:

```bash
ollama run llama3.1:8b
```

Alternatively, configure the custom GGUF model using the included `Modelfile`, following the model path and configuration specified in that file.

### Step 4: Launch MindMate

```bash
streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

## 9. Privacy and Safety Considerations

MindMate is designed around the following privacy and safety principles:

- Local model inference rather than cloud-based LLM API calls.
- Local storage of personal reflection records.
- User-controlled deletion of stored records.
- Input and output safety interception.
- Clear distinction between AI-assisted reflection and professional clinical care.

**Important:** Local execution does not automatically guarantee complete data security. Database encryption, operating-system security, backup handling and other storage protections must be verified independently.

## 10. Collaboration and Development Workflow

MindMate follows a two-person modular development workflow.

| Role | Responsibilities |
|---|---|
| Role A: AI/ML and Safety Lead | `inference.py`, `safety_guard.py`, local model configuration |
| Role B: UI/UX and Data Sovereignty Lead | `app.py`, `memory_vault.py`, `summary_engine.py`, `therapist_match.py` |

### Git Branching Guidelines

1. Avoid committing large model-weight files such as `.gguf` and `.bin`.
2. Keep model files outside the main Git repository.
3. Develop features using dedicated branches.
4. Use pull requests to integrate completed features into `main`.

Example feature branches:

```text
feature/safety-guard
feature/vault-encryption
feature/summary-engine
feature/therapist-directory
```

## 11. Research and Evaluation Foundations

The project draws on research and datasets relevant to conversational AI and mental healthcare:

- **Conversational AI in Psychotherapy:** Research into conversational agents, therapeutic alliance and patient disclosure.
- **Agentic AI in Psychiatric Care:** Research on constrained AI copilots and human-in-the-loop mental healthcare.
- **MentalChat16K:** A conversational dataset relevant to mental health dialogue evaluation.
- **DAIC-WOZ:** A clinical interview database used in research on distress analysis.

These resources provide potential foundations for evaluating conversational quality, safety and model behaviour. Their suitability and permitted use should be assessed before incorporating them into experiments.

## 12. Future Enhancements

- Improved conversational context retention.
- More comprehensive safety evaluation.
- Enhanced pre-session summary quality.
- User-controlled conversation history and privacy settings.
- Improved therapist discovery and matching.
- Systematic evaluation of empathetic and context-aware responses.
- Stronger local data protection mechanisms.

## 13. Disclaimer

MindMate is an experimental AI-assisted reflection and therapy preparation tool. It is not a licensed medical provider, clinical diagnostic system, psychotherapy service or crisis intervention system.

It does not diagnose or treat mental health conditions. AI-generated responses may be inaccurate and should not replace professional advice.

Users experiencing an immediate mental health emergency should contact local emergency services or appropriate crisis support resources.

## 14. License

Distributed under the Apache License 2.0.

---

**Developed by Carol Das and the MindMate project team.**

[GitHub Repository](https://github.com/carol-das/Mindmate)