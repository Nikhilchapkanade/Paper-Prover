Paper Prover
Stop trusting sketchy research papers
Most AI tools will read a paper claiming "98.5% accuracy" and just accept it. Paper Prover? It reads like that one reviewer who actually checks your math.
We built this because we kept running into papers where the claims didn't match the data. Abstract says one thing, Figure 3 says something completely different. Someone needed to call BS on this stuff automatically.

What this thing does
Upload a research paper and Paper Prover tears into it like a peer reviewer who's had too much coffee:
Checks for missing evidence

Are the claims backed up by actual data?
Or is it just "trust me bro" science?

Analyzes the methodology

Do they have a control group?
Did they run this once and get lucky?
Are there obvious biases they're ignoring?

Reads the actual charts

Most AI can't see images. This one can.
Catches when the graph shows 93.7% but the text claims 98.5%

Finds contradictions

Compares claims across multiple papers
Spots when Paper A and Paper B can't both be right

Flags incomplete research

Missing datasets
No replication studies
Unsubstantiated conclusions


Why it works different
Two AIs argue with each other
We don't trust one AI to read the paper. That's how you get hallucinations.
Instead:

Researcher AI extracts all the claims
Skeptic AI immediately questions everything
They debate until something resembles truth emerges

Only claims that survive the argument get marked as verified.
It actually looks at figures
Uses Gemini's vision model to read charts, tables, and graphs. You'd be amazed how often the visuals contradict the text.
Remembers everything
Stores insights in a graph database (Neo4j). It can connect dots across papers:

"Wait, these three papers cite the same dataset but report different sample sizes"
"Paper A contradicts what Paper B claimed last month"
"Every paper using this methodology has the same flaw"


Real output example
Here's what it caught in an actual paper:
Claim: "Model achieves 98.5% accuracy"
Source: Abstract, line 2

What the skeptic found:
❌ No error bars shown in any figure
❌ Only one experimental run mentioned
❌ Test set size not disclosed
❌ Baseline comparison uses outdated model (2019)

Visual analysis:
📊 Figure 3 confusion matrix shows 93.7% actual accuracy
📊 Table 2 shows baseline at 92.1%
→ Real improvement: 1.6%, not 6.5%

Verdict: FLAGGED
Confidence: Low (42%)
Reasoning: Insufficient evidence, potential cherry-picking
That's the kind of stuff that gets past standard AI tools.

Quick setup
Need Python 3.10+, Neo4j, and API keys (Google AI + Groq - both have free tiers).
bashgit clone https://github.com/yourusername/paper-prover.git
cd paper-prover
pip install -r requirements.txt
```

Add your keys to `.env`:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
Run it:
bashpython app.py
```

Go to localhost:8000

---

## What you can ask it

**"Analyze this paper"**
Uploads a PDF, runs it through the debate system, tells you what holds up and what doesn't.

**"Find weak methodology"**
Scans your library for papers with missing control groups, unreported sample sizes, cherry-picked results.

**"Show contradictions"**
Compares papers you've uploaded and flags when they disagree on facts.

**"Which papers lack concrete evidence?"**
Identifies research based on assumptions rather than data.

**"What datasets are used inconsistently?"**
Finds when different papers report different stats for the same dataset.

---

## How it's built
```
paper-prover/
├── app.py              # run this
├── backend/           
│   ├── graph_db.py    # Neo4j memory system
│   ├── pdf_engine.py  # extracts text from papers
│   └── vision.py      # reads charts with Gemini
├── agents/            
│   ├── prompts.py     # instructions for each AI
│   ├── state.py       # what they remember
│   └── swarm.py       # coordinates the debates
└── data/
    └── uploads/       # PDFs go here temporarily
Tech:

LangGraph (multi-agent coordination)
Gemini 1.5 Pro (vision)
Groq (fast inference)
Neo4j (graph database)
Chainlit (UI)


The critique categories
Paper Prover checks for five main issues:
1. Lack of concrete evidence
Claims based on assumptions, not data
2. Incomplete analysis
Superficial examination that skips important details
3. Insufficient data
Can't verify claims because datasets or methods aren't disclosed
4. Methodological flaws
Unverified assumptions, missing controls, ignored biases
5. Lack of rigor
Incomplete research, unsubstantiated findings, unreliable conclusions

