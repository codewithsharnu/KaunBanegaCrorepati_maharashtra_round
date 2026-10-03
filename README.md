# Re:Learn - Adaptive Multimodal Learning Environment
> **BIT N BUILD International Hackathon (Maharashtra Round - Oct 3-4, 2026)**  
> **Host:** GDG on Campus, Fr. Conceicao Rodrigues College of Engineering (Fr. CRCE), Bandra, Mumbai  
> **Problem Statement #3:** *Re:Learn: Adaptive Multimodal Learning Environment*  
> **Selected Domain:** **Introductory Python Programming**

---

## 🌟 Executive Summary & Problem Context
Traditional Learning Management Systems (LMS) treat incorrect learner answers as simply **"Incorrect"** (Binary 0/1 grading). Showing a student the correct answer does not repair the underlying conceptual flaw in their mental model.

**Re:Learn** is an AI-powered diagnostic and pedagogical environment designed to:
1. Parse the learner's code using **Abstract Syntax Trees (AST)** and **Lexical TF-IDF representations**.
2. Identify the **underlying cognitive misconception** causing the error, rather than just marking it wrong.
3. **Differentiate** between different misconceptions that produce identical or similar incorrect outputs.
4. Deliver **adaptive multimodal interventions** (conceptual rules, visual execution traces, mental analogies, and code contrast diffs).
5. Conduct a **Resolution Assessment** via transfer-testing to verify that the misconception has been genuinely resolved.
6. Maintain a dynamic **Learner Model** tracking recurring cognitive bugs and mastery trajectory over time.

---

## 🚀 Key Features Implemented

### 1. Misconception Dataset (`data/misconceptions_dataset.json`)
A curated dataset of authentic introductory Python student code submissions with annotated underlying misconceptions across 8 categories:
- `M1_INDEXING_OFF_BY_ONE`: 1-Based Indexing Assumption.
- `M2_SLICE_INCLUSIVITY`: Inclusive Stop Bound Assumption (`[start:stop)`).
- `M3_ASSIGNMENT_VS_EQUALITY`: Using single `=` in place of `==` in conditions.
- `M4_MUTABLE_DEFAULT_ARG`: Persistent mutable default parameter (`def f(x=[])`).
- `M5_STRING_NUM_CONCAT`: Implicit type casting assumption in string concatenation.
- `M6_VARIABLE_SCOPE_LEAK`: Modifying outer scope without `global` / local leakage.
- `M7_INTEGER_VS_FLOAT_DIVISION`: Single `/` vs floor `//` division semantics.
- `M8_LOOP_ACCUMULATOR_RESET`: Intra-loop accumulator reinitialization.

### 2. Misconception Diagnostic Model (`misconception_engine.py`)
- Hybrid architecture combining AST tree walker heuristics with a TF-IDF Cosine Centroid classifier.
- Zero external C-extension binary dependencies: pure-Python architecture ensuring 100% cross-platform stability.
- Evaluated on a held-out test split of unseen student responses.

### 3. Misconception Differentiation Module
- Specially engineered to address the hackathon requirement: *distinguish between different misconceptions producing similar wrong answers*.
- Example: Slicing `[10, 20, 30]` to get `[10, 20]`:
  - Student A writes `arr[1:2]` (Output: `[20]`) -> Diagnosed as **1-Based Indexing**.
  - Student B writes `arr[0:1]` (Output: `[10]`) -> Diagnosed as **Inclusive Stop Bound**.
  - Re:Learn's AST disambiguator isolates the exact syntactic shift vs boundary inclusivity flaw.

### 4. Adaptive Multimodal Interventions
When a misconception is identified, the student receives:
- **Mental Model Analogy:** Concrete real-world intuition.
- **Targeted Concept Rule:** Precise, jargon-free rule of thumb.
- **Visual Execution Trace / Diagram:** ASCII memory and index layouts.
- **Corrective Code Diff:** Erroneous code juxtaposed against idiomatic Python.

### 5. Resolution Assessment (Transfer Testing)
- Unlike naive systems that re-test the identical question, Re:Learn presents an **isomorphic transfer challenge** requiring the same mental rule in a new context.
- Traps and verifies that the misconception has been genuinely resolved.

### 6. Dynamic Learner Model
- Tracks learner profiles, attempt histories, and recurring misconception frequencies.
- Evaluates mastery score:  
  $$\text{Mastery \%} = \frac{\text{Verified Transfer Resolutions}}{\text{Total Attempted Interventions}} \times 100$$

### 7. Quantitative Evaluation & Analytics Dashboard
- Live performance metrics (Test Accuracy, Precision, Recall, F1-Score).
- Confusion matrix heatmap.
- Categorical distribution of misconceptions.

---

## 📊 Model Evaluation Results (Held-Out Test Set)

| Metric | Score |
|---|---|
| **Test Accuracy** | **80.00%** |
| **Precision (Weighted)** | **100.00%** |
| **Recall (Weighted)** | **80.00%** |
| **F1-Score (Weighted)** | **88.89%** |
| **Total Benchmark Samples** | **34** |
| **Cognitive Misconception Classes** | **8** |

---

## 🛠️ Tech Stack
- **Backend & Logic:** Python 3.14, Abstract Syntax Tree (`ast`), `re`, `json`, `math`, `collections`
- **Web Application:** Flask 3.1.3
- **Frontend & UI:** Tailwind CSS, FontAwesome 6, Chart.js
- **Dataset Format:** Structured JSON / CSV
- **Deployment & Sync:** Standalone REST API / Automated GitHub REST synchronizer

---

## 💻 How to Run Locally

### 1. Prerequisites
Ensure Python 3.10+ is installed on your computer.

### 2. Start the Server
Double-click `run_relearn.bat` or run in terminal:
```bash
python app.py
```
Open your browser at:
```
http://localhost:5000
```

---

## ⏱️ 3-Hour Commit Schedule & Milestone Log

| Interval | Milestone Commit Message | Key Accomplishment |
|---|---|---|
| **Hour 0 – 3** | `init: Problem #3 Re:Learn architecture & Python misconception dataset schema` | Initialized repository, defined JSON dataset across 8 Python misconceptions. |
| **Hour 3 – 6** | `feat: AST semantic parser & ML misconception classification engine` | Implemented hybrid AST + TF-IDF classifier with training and evaluation pipeline. |
| **Hour 6 – 9** | `feat: Misconception differentiation module & adaptive multimodal interventions` | Added comparator for similar incorrect outputs and generated tailored interventions. |
| **Hour 9 – 12** | `feat: Interactive diagnostic portal, resolution assessment & teacher evaluation dashboard` | Built responsive Flask web application, transfer tests, and mastery analytics. |
| **Final** | `docs: Complete hackathon submission documentation, evaluation report & demo readiness` | Finalized README, submission text, and test verification suite. |

---

## 👥 Hackathon Team & Acknowledgments
- **Hackathon:** BIT N BUILD International Hackathon 2026 (Maharashtra Round)
- **Organized By:** GDG on Campus, Fr. CRCE Bandra, Mumbai
- **Track:** Problem #3 — Re:Learn: Adaptive Multimodal Learning Environment
- Built with focus on pedagogical AI and cognitive education technology.
