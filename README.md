<p align="center">
  <h1 align="center">📄 Paper-Prover</h1>
  <p align="center"><strong>Two AIs debate every research paper claim until one admits they're wrong</strong></p>
  <p align="center"><em>Catches inflated accuracy numbers, missing control groups, and contradictions your PDF reader will never see.</em></p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-Swarm-7C3AED?style=flat-square&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/Neo4j-Graph_DB-008CC1?style=flat-square&logo=neo4j&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini_1.5_Pro-Vision-4285F4?style=flat-square&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Chainlit-UI-FF6B6B?style=flat-square"/>
</p>

---

## 🤔 The Problem

Most AI tools read a paper claiming **"98.5% accuracy"** and just accept it. Paper-Prover reads like that one reviewer who actually checks your math.

We built this because we kept finding papers where the abstract says one thing and Figure 3 says something completely different. Someone needed to call BS on this automatically.

---

## ⚡ How It Works

Upload a PDF and Paper-Prover tears into it like a rigorous peer reviewer:

```
              ┌──────────────┐
              │  Upload PDF  │
              └──────┬───────┘
                     │
         ┌───────────▼───────────┐
         │   PDF Engine          │
         │  (Text + Chart Extract)│
         └───────────┬───────────┘
                     │
    ┌────────────────▼────────────────┐
    │        LangGraph Swarm          │
    │                                 │
    │  🔬 Researcher ←→ 🤨 Skeptic   │
    │     (extracts)    (questions)   │
    │         └───── Debate ─────┘    │
    └────────────────┬────────────────┘
                     │
         ┌───────────▼───────────┐
         │   Neo4j Knowledge     │
         │   Graph Database      │
         └───────────────────────┘
```

### The Debate System

| Agent | Role | What It Does |
|-------|------|-------------|
| 🔬 **Researcher** | Claim Extractor | Reads the full paper + figures, extracts every testable claim |
| 🤨 **Skeptic** | Devil's Advocate | Immediately challenges each claim with counter-evidence |
| 🧠 **Verdict Engine** | Final Judge | Only verified claims survive into the knowledge graph |

### What It Catches

- **Missing evidence** — claims with no backing data
- **Methodology gaps** — no control group, ran it once and got lucky
- **Figure discrepancies** — graph shows 93% but text says 98% *(uses Gemini 1.5 Pro vision)*
- **Cross-paper contradictions** — two papers cite the same dataset with different sample sizes
- **Incomplete research** — missing datasets, no replication studies

---

## 📸 Demo

<img width="1174" alt="Paper-Prover in action" src="https://github.com/user-attachments/assets/7d8d0925-b6ff-44d2-9b57-2b76fa1b4d77" />

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/Nikhilchapkanade/Paper-Prover.git
cd Paper-Prover

# 2. Install
pip install -r requirements.txt

# 3. Environment variables (.env)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

# 4. Run
python -m chainlit run app.py -w
```

---

## 💬 Example Commands

| Prompt | What Happens |
|--------|-------------|
| *Upload a PDF* | Runs the full debate system on the paper |
| `"Find weak methodology"` | Scans your library for missing controls |
| `"Show contradictions"` | Flags when two uploaded papers disagree |
| `"Which papers lack evidence?"` | Identifies assumption-based research |

---

## 📁 Project Structure

```
paper-prover/
├── app.py                # Chainlit entry point
├── backend/
│   ├── graph_db.py       # Neo4j knowledge graph
│   ├── pdf_engine.py     # PDF text extraction
│   └── vision.py         # Chart analysis (Gemini 1.5 Pro)
├── agents/
│   ├── prompts.py        # System instructions for each agent
│   ├── state.py          # Shared state during debates
│   └── swarm.py          # LangGraph debate orchestration
├── config.py             # LLM configuration
└── data/
    └── uploads/          # Temporary PDF storage
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Multi-Agent Orchestration | LangGraph |
| Computer Vision | Gemini 1.5 Pro |
| Fast Inference | Groq (Llama 3) |
| Knowledge Graph | Neo4j |
| User Interface | Chainlit |
| PDF Processing | PyMuPDF |

---

## 📊 Critique Categories

The system classifies issues into five severity levels:

1. **Lack of concrete evidence** — claims without supporting data
2. **Incomplete analysis** — superficial examination of results
3. **Insufficient data** — hidden datasets or undisclosed methods
4. **Methodological flaws** — missing controls, selection bias
5. **Lack of rigor** — unsubstantiated or unreproducible findings
