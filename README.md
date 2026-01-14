# Paper Prover

### Stop trusting sketchy research papers

**Most AI tools will read a paper claiming "98.5% accuracy" and just accept it. Paper Prover reads like that one reviewer who actually checks your math.**

We built this because we kept running into papers where the claims didn't match the data. The abstract says one thing, Figure 3 says something completely different. Someone needed to call BS on this stuff automatically.

---

## What this tool does

Upload a research paper and Paper Prover tears into it like a rigorous peer reviewer:

* **Checks for missing evidence:** Are claims backed up by data, or is it just assumption?
* **Analyzes methodology:** Do they have a control group? Did they run it once and get lucky?
* **Reads the actual charts:** Most AI is blind to images. This tool sees when a graph shows 93% but the text claims 98%.
* **Finds contradictions:** Compares claims across multiple papers to find inconsistencies.
* **Flags incomplete research:** Highlights missing datasets, no replication studies, and unsubstantiated conclusions.

---

## Why it works differently

### 1. Two AIs argue with each other
We don't trust a single AI to interpret a paper (that leads to hallucinations). Instead:
1.  **The Researcher** extracts the claims.
2.  **The Skeptic** immediately questions them.
3.  They debate until the truth emerges. Only verified claims make it to the database.

### 2. It actually looks at figures
It uses **Gemini 1.5 Pro** to read charts, tables, and heatmaps. It catches discrepancies between the visual data and the written text.

### 3. It remembers everything
It stores insights in a **Neo4j** graph database. This allows it to connect dots across your entire library:
> "Wait, these three papers cite the same dataset but report different sample sizes."



---

## Real output example

<img width="1174" height="1106" alt="Screenshot 2026-01-12 172125" src="https://github.com/user-attachments/assets/7d8d0925-b6ff-44d2-9b57-2b76fa1b4d77" />


```text


# 1. Get the code
git clone [https://github.com/yourusername/paper-prover.git](https://github.com/yourusername/paper-prover.git)
cd paper-prover

# 2. Install dependencies
pip install -r requirements.txt

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

python -m chainlit run app.py -w

Command,Function
"""Analyze this paper""",Upload a PDF to run the debate system.
"""Find weak methodology""",Scans your library for missing controls or unreported sample sizes.
"""Show contradictions""",Flags when two uploaded papers disagree on facts.
"""Which papers lack evidence?""",Identifies research based on assumptions rather than data.

paper-prover/
├── app.py              # Main entry point
├── backend/
│   ├── graph_db.py     # Neo4j memory system
│   ├── pdf_engine.py   # Text extractor
│   └── vision.py       # Chart reader (Gemini)
├── agents/
│   ├── prompts.py      # System instructions
│   ├── state.py        # Shared memory during debates
│   └── swarm.py        # Debate coordination logic
└── data/
    └── uploads/        # Temporary storage

Tech Stack:

LangGraph: Multi-agent coordination

Gemini 1.5 Pro: Computer Vision

Groq: Fast inference

Neo4j: Graph database

Chainlit: User Interface

Critique Categories
The system classifies issues into five buckets:

Lack of concrete evidence (Claims without data)

Incomplete analysis (Superficial examination)

Insufficient data (Hidden datasets or methods)

Methodological flaws (Missing controls, bias)

Lack of rigor (Unsubstantiated findings)
Verdict: FLAGGED
Confidence: Low (42%)
Reasoning: Insufficient evidence, potential cherry-picking
