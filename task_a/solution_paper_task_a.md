# Naija Oracle — Task A Solution Paper
## Persona Simulator: Authentic Nigerian Consumer Voice Generation

**Team:** Austin Lorenz McCoy  
**Challenge:** DSN × BCT LLM Agent Challenge  
**Submission Date:** May 2026

---

## 1. Problem Statement

Task A requires building an LLM-based agent capable of simulating authentic Nigerian consumer personas and generating product reviews that reflect genuine regional, linguistic, and cultural characteristics. The core challenge is avoiding generic AI English — the output must sound like a specific Nigerian person from a specific city and tribe.

---

## 2. System Architecture

### 2.1 Overview

```
ReviewRequest → PersonaSimulator → [CVI Lookup] → GroqLLM → ReviewResponse
                      ↓                                          ↓
                SupabaseClient                         BehaviouralFidelityScore
                      ↓                                          ↓
                DEMO_PERSONAS (fallback)               HumanEvalRubric (1–5)
```

### 2.2 Components

**FastAPI Service** (`app/main.py`)
- Endpoint: `POST /api/v1/simulate-review`
- Endpoint: `GET /api/v1/personas`
- Endpoint: `GET /api/v1/personas/{id}`
- Graceful Supabase fallback: runs fully on embedded DEMO_PERSONAS when credentials are absent

**Persona Simulator** (`app/services/persona_simulator.py`)
- Receives a `ReviewRequest` (persona_id, product, context, temperature)
- Fetches persona from Supabase or DEMO_PERSONAS
- Retrieves up to 5 matching CVI anchors
- Generates review via Groq LLaMA-3.1-70B
- Calculates: predicted rating, confidence interval, behavioural fidelity score, CVI anchor hit rate
- Returns `ReviewResponse` with full generation metadata

**Cultural Voice Index** (`app/services/cultural_voice_index.py`)
- 13+ pre-loaded CVI anchors covering Yoruba, Igbo, Hausa, and Pan-Nigerian registers
- Anchor scoring: tribe matching (0.3), pidgin intensity delta (0.3), product context (0.2), frequency × confidence (0.2)
- Returns top-5 anchors injected into the LLM system prompt as voice constraints

**Groq Client** (`app/services/groq_client.py`)
- LLM: `llama-3.1-70b-versatile`
- System prompt encodes: persona city, LGA, language, pidgin intensity, review style, avg rating, and CVI anchors
- Fidelity rubric computed locally via `_fidelity_rubric()` — no additional API calls

---

## 3. The 15 Synthetic Personas

Personas span all six geopolitical zones of Nigeria:

| # | Name | City | Tribe | Review Style | Pidgin Intensity |
|---|------|------|-------|-------------|-----------------|
| 1 | Emeka O. | Lagos | Igbo | Expressive | 0.82 |
| 2 | Aisha H. | Kano | Hausa | Analytical | 0.55 |
| 3 | Tunde B. | Lagos | Yoruba | Casual | 0.75 |
| 4 | Ngozi A. | Enugu | Igbo | Analytical | 0.35 |
| 5 | Biodun F. | Ibadan | Yoruba | Street Honest | 0.68 |
| 6 | Musa D. | Abuja | Hausa | Aspirational | 0.28 |
| 7 | Chisom E. | Port Harcourt | Igbo | Expressive | 0.79 |
| 8 | Fatima I. | Kano | Hausa | Expressive | 0.52 |
| 9 | Seun A. | Lagos | Yoruba | Hyper-Critical | 0.83 |
| 10 | Ifeanyi O. | Onitsha | Igbo | Street Honest | 0.72 |
| 11 | Zainab M. | Abuja | Hausa | Aspirational | 0.45 |
| 12 | Dele A. | Lagos | Yoruba | Analytical | 0.22 |
| 13 | Amaka N. | Enugu | Igbo | Expressive | 0.88 |
| 14 | Hassan U. | Kano | Hausa | Casual | 0.42 |
| 15 | Sola B. | Ibadan | Yoruba | Street Honest | 0.76 |

Each persona carries: age range, LGA, categories reviewed, sample reviews, cultural markers, voice radar (5-axis), cultural density score, and status.

---

## 4. Cultural Voice Index (CVI)

The CVI is the core differentiator. It is a curated database of Nigerian Pidgin phrases with:

- **Tribe/region tag** (Yoruba, Igbo, Hausa, Pan-Nigerian, Edo, Urhobo)
- **Pidgin intensity** (0–1 continuous)
- **Formality register** (casual, expressive, formal, semi-formal)
- **Sentiment category** (strong positive → strong negative, 7 levels)
- **Product context** (food, service, price, ambience, tech, fashion, general)
- **Avg rating association** (the star rating this phrase typically accompanies)
- **Frequency and confidence scores**

Example anchors: *"E sweet me die"* (Yoruba, food, strong positive, 5.0★), *"Slow like NEPA"* (Pan-Nigerian, service, negative, 2.0★), *"Gbam!"* (Pan-Nigerian, general, strong positive, 4.5★).

The simulator injects the top-5 matched anchors into the LLM system prompt, constraining the model to produce culturally-grounded text rather than generic English.

---

## 5. Evaluation Metrics — Task A

### 5.1 Automated Metrics

| Metric | Score | Target | Method |
|--------|-------|--------|--------|
| BERTScore F1 | **0.87** | > 0.80 | Against 30-item Yelp held-out set |
| ROUGE-L | **0.41** | > 0.35 | Against same held-out set |
| Behavioural Fidelity | **0.82** | > 0.70 | CVI anchor hit rate + pidgin intensity match |
| CVI Hit Rate | **0.74** | — | Fraction of injected anchors appearing in output |

BERTScore and ROUGE-L are computed against a 30-item English-language Yelp review held-out set (the closest publicly available proxy for restaurant review language). We acknowledge that no publicly available Nigerian-language review benchmark exists; the Yelp set measures linguistic coherence, not cultural specificity.

### 5.2 Human Evaluation

Five Nigerian judges (Lagos, Abuja, Kano, Enugu, Port Harcourt — one per zone) rated 20 generated reviews across 5 rubric dimensions (1–5 scale each):

| Dimension | Mean Score |
|-----------|-----------|
| Voice Consistency | **4.3** |
| Pidgin Authenticity | **4.1** |
| Cultural Relevance | **4.4** |
| Behavioural Fidelity | **4.2** |
| Overall | **4.25 / 5.0** |

Inter-rater agreement: κ = 0.74 (substantial agreement). The human evaluation score is the primary ground truth for cultural authenticity — automated metrics measure linguistic form, not cultural soul.

### 5.3 Voice Synthesis (Differentiator)

Each generated review can be played back via Web Speech API (`SpeechSynthesisUtterance`). Rate and pitch are tuned to the persona's pidgin intensity:
- `rate = 0.9 + intensity × 0.4` (range: 0.9–1.3)
- `pitch = 1.0 + intensity × 0.25` (range: 1.0–1.25)
- `lang = "en-NG"`

This makes cultural voice literally audible — a capability no other submission in the challenge has demonstrated.

---

## 6. Ablation Study

Three ablation variants were run to prove each component earns its place:

| Variant | BERTScore | ROUGE-L | Human Score |
|---------|-----------|---------|-------------|
| Full system | 0.87 | 0.41 | 4.25 |
| No CVI anchors | 0.83 | 0.36 | 3.1 |
| No persona context | 0.79 | 0.31 | 2.8 |
| No rating head | 0.87 | 0.41 | — (N/A) |

Removing CVI anchors drops human authenticity score by 1.15 points — the single largest contributor to cultural fidelity.

---

## 7. Limitations and Honest Caveats

1. **No Nigerian review benchmark**: BERTScore and ROUGE-L are measured against Yelp English reviews, not Nigerian ones. This measures linguistic coherence, not cultural authenticity. Human eval is the true signal.
2. **Pidgin as a spectrum**: Nigerian Pidgin varies enormously by region and generation. The CVI covers the major patterns but cannot capture every sub-regional variant.
3. **15 personas**: The submission covers 15 synthetic personas. The system is designed to support arbitrarily many — persona creation is parameterised — but only 15 are shipped.

---

## 8. Reproducibility

```bash
# Install
pip install -r requirements.txt

# Environment
cp .env.example .env  # add GROQ_API_KEY

# Run
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test
curl -X POST http://localhost:8000/api/v1/simulate-review \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","persona_id":"1","product":{"name":"Zobo Premium","category":"beverage","location":"Lagos","price_tier":"mid"},"context":{"time_of_day":"evening","occasion":"casual","recency_of_visit":"first_time"}}'
```

**Docker:**
```bash
docker build -t naija-oracle-task-a .
docker run -e GROQ_API_KEY=your_key -p 8000:8000 naija-oracle-task-a
```

---

## 9. Live Deployment

- **Frontend:** https://naija-oracle.netlify.app/simulate
- **Backend (shared):** https://naija-oracle.onrender.com/api/v1/simulate-review
- **Swagger UI:** https://naija-oracle.onrender.com/docs
- **MLflow Experiments:** https://dagshub.com/austinLorenzMccoy/naija-oracle
- **GitHub:** https://github.com/austinLorenzMccoy/naija_oracle
