# Naija Oracle — Product Requirements Document
### DSN × BCT LLM Agent Challenge Submission
**By:** Chibueze Augustine Chidera  
**Model Family:** Task A (User Modeling) + Task B (Recommendation)  
**Stack:** Groq API · Supabase · FastAPI · React/TypeScript · Docker  

---

## 1. Executive Summary

**Naija Oracle** is a dual-agent LLM system that reads how real Nigerian users think, speak, and choose — then simulates their voice to generate authentic reviews *and* delivers hyper-personalised recommendations tuned to Nigerian consumer context.

The name is deliberate: an *oracle* knows what you'll say before you say it. "Naija" anchors the system in Nigerian cultural specificity — the kind of Pidgin-inflected, context-aware voice that generic recommendation systems erase entirely.

> *"No be say the product bad — the vibe no catch me."*  
> A Naija Oracle system would predict exactly this sentiment for the right user.

---

## 2. Problem Statement

Existing LLM-based review and recommendation systems suffer from three compounding failures when applied to Nigerian users:

1. **Cultural voice erasure** — models produce sanitised Standard English that sounds nothing like how Nigerian users actually write reviews (Pidgin, Yoruba/Igbo/Hausa code-switching, localised slang).
2. **Static user modelling** — users are bucketed into fixed profiles rather than treated as dynamic agents shaped by context (price sensitivity shifts, peer influence, local events).
3. **Cold-start ignorance** — Nigerian product categories (suya joints, pepper soup spots, local fabric sellers, fintech apps) are severely underrepresented in training data.

**Naija Oracle** solves all three.

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   NAIJA ORACLE                       │
│                                                     │
│  ┌───────────────┐        ┌───────────────────────┐ │
│  │  AGENT A      │        │  AGENT B              │ │
│  │  Persona      │        │  Recommendation       │ │
│  │  Simulator    │        │  Engine               │ │
│  └──────┬────────┘        └──────────┬────────────┘ │
│         │                            │               │
│  ┌──────▼────────────────────────────▼────────────┐ │
│  │          Shared Intelligence Layer              │ │
│  │  Cultural Context DB · Supabase Vector Store   │ │
│  │  Groq LLaMA-3.1-70B · RAG Pipeline            │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### 3.1 Core Components

| Component | Technology | Role |
|---|---|---|
| LLM Backbone | Groq API (LLaMA-3.1-70B-Versatile) | Zero-latency inference, free tier |
| Vector Store | Supabase `pgvector` + RLS | Embeddings, per-user context isolation |
| Auth | Supabase OAuth (Google) | Session management, multi-tenant |
| Real-time | Supabase Realtime | Live agent streaming to UI |
| Backend | FastAPI + Python 3.11 | Agent orchestration, REST API |
| Frontend | React + TypeScript + Vite | Dashboard, demo playground |
| Containerisation | Docker + Docker Compose | Reproducible deployment |
| CI/CD | GitHub Actions + MLflow | Experiment tracking, deployment |
| Edge Functions | Supabase Edge Functions | Notification hooks, post-submission triggers |

---

## 4. Task A — Persona Simulator Agent

### 4.1 Objective
Given a user persona and product details, generate a plausible star rating AND written review that sounds like *that specific user*, including cultural voice, sentiment history, and contextual signals.

### 4.2 Input Schema
```json
{
  "user_id": "usr_NG_001",
  "persona": {
    "age_range": "25-34",
    "city": "Lagos",
    "lga": "Surulere",
    "primary_language": "Yoruba",
    "review_style": "expressive",
    "avg_rating": 3.8,
    "sentiment_volatility": "high",
    "categories_reviewed": ["food", "fashion", "fintech"],
    "sample_reviews": ["...", "..."],
    "cultural_markers": ["Pidgin_user", "price_sensitive", "brand_loyal_food"]
  },
  "product": {
    "name": "Chicken Republic Spicy Wings",
    "category": "fast_food",
    "location": "Ikeja",
    "price_tier": "mid",
    "metadata": {...}
  },
  "context": {
    "time_of_day": "late_night",
    "weather": "harmattan",
    "occasion": "after_work",
    "recency_of_visit": "first_time"
  }
}
```

### 4.3 Agent Architecture (Task A)

```
Input Payload
      │
      ▼
┌─────────────────────────────────────┐
│  STEP 1: Persona Embedding Retrieval│
│  pgvector similarity search for     │
│  analogous past users/reviews       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  STEP 2: Cultural Calibration       │
│  Groq: map persona → voice profile  │
│  (Pidgin %, sentiment range, etc.)  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  STEP 3: Rating Prediction          │
│  Fine-tuned regression head on      │
│  historical user ± product signals  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  STEP 4: Review Generation          │
│  Groq LLaMA → culturally-aware,     │
│  persona-consistent review text     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  STEP 5: Behavioural Fidelity Check │
│  Score against persona priors;       │
│  regenerate if drift > threshold    │
└─────────────────────────────────────┘
```

### 4.4 The Nigerian Voice Layer

This is the differentiator that earns the bonus marks.

The system maintains a **Cultural Voice Index (CVI)** — a Supabase table of linguistic patterns tagged by:
- Tribe / region (`Yoruba`, `Igbo`, `Hausa`, `Pan-Nigerian`)
- Pidgin intensity (`0.0` – `1.0`)
- Formality register (`casual`, `expressive`, `formal`)
- Sentiment anchors (phrases that signal specific rating ranges)

**Example CVI entries:**
```
"E sweet me die" → positive, food, Yoruba, Pidgin 0.8, rating 5.0
"E dey manage" → neutral-negative, general, 0.6, rating 2.5
"Dem cheat me" → negative, service, 0.9, rating 1.0
"The vibe no catch me" → neutral, ambience, 0.7, rating 3.0
```

The Groq prompt template dynamically injects 3-5 CVI anchors matched to the user's cultural profile, steering output away from generic AI-sounding text.

### 4.5 Output Schema (Task A)
```json
{
  "predicted_rating": 3.5,
  "confidence_interval": [3.0, 4.0],
  "review_text": "This Chicken Republic for Ikeja, the wings fine but e too small for the price o. My guy at the counter no even smile. Abeg 3.5 stars — I go come back sha if hunger catch me late night.",
  "voice_profile_used": {
    "pidgin_intensity": 0.72,
    "sentiment_category": "mixed-positive",
    "cultural_markers_activated": ["price_sensitivity", "Yoruba_casual"]
  },
  "behavioural_fidelity_score": 0.87
}
```

### 4.6 Evaluation Metrics (Task A)

| Metric | Method | Target |
|---|---|---|
| Review Text Quality | BERTScore F1 (multilingual-bert) | > 0.82 |
| Review Text Quality | ROUGE-L | > 0.35 |
| Rating Accuracy | RMSE | < 0.75 |
| Behavioural Fidelity | Human eval rubric (voice, tone, plausibility) | > 4.0/5.0 |
| Nigerian Voice Score | CVI match rate | > 60% anchor hits |

---

## 5. Task B — Recommendation Engine Agent

### 5.1 Objective
Given a user persona, produce a ranked list of personalised recommendations — going beyond collaborative filtering by using contextual signals, multi-turn reasoning, and agentic retrieval.

### 5.2 Input Schema
```json
{
  "user_id": "usr_NG_001",
  "persona": { ... },
  "context": {
    "current_time": "Saturday 8PM",
    "location": "Lekki Phase 1",
    "mood_signal": "celebratory",
    "recent_searches": ["shawarma near me", "cold stone"],
    "budget_naira": 5000
  },
  "domain": "food",
  "turn_history": [],
  "cold_start": false
}
```

### 5.3 Agent Architecture (Task B)

The Task B agent implements a **Reason → Retrieve → Rank → Refine** (R4) loop:

```
User Persona + Context
        │
        ▼
┌───────────────────────┐
│  REASON               │
│  Groq: derive intent, │
│  constraints, gaps    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  RETRIEVE             │
│  pgvector similarity  │
│  + collaborative      │
│  filtering fallback   │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  RANK                 │
│  NDCG-aware re-ranker │
│  + contextual boost   │
│  (time, mood, budget) │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  REFINE               │
│  Multi-turn follow-up │
│  correction; cold-    │
│  start graph hop      │
└───────────────────────┘
```

### 5.4 Cold-Start & Cross-Domain Strategy

**Cold-start** (new user, no history):  
→ Ask 3 onboarding questions framed as Nigerian cultural probes:  
  *"Suya or shawarma?" / "AMVCA or BBNaija?" / "GTB or Kuda?"*  
→ Map answers to a cold-start persona cluster using cosine similarity on seed vectors.  
→ Bootstrap recommendations from the cluster's top-N items.

**Cross-domain transfer:**  
→ Users who review Afrobeats music are likely to enjoy Afrocentric fashion → map via latent category graph.  
→ Supabase graph table stores `(category_a, category_b, transfer_weight)` tuples.

### 5.5 Output Schema (Task B)
```json
{
  "recommendations": [
    {
      "rank": 1,
      "item_id": "res_NG_4421",
      "name": "Yellow Chilli Restaurant",
      "category": "Nigerian fine dining",
      "location": "Victoria Island",
      "reasoning": "User's Lekki location + celebratory mood + ₦5k budget aligns with Yellow Chilli's weekend vibe. 3 similar users in your cluster visited last Saturday.",
      "predicted_rating": 4.4,
      "context_score": 0.91
    }
  ],
  "explanation": "Based on your current mood (celebratory), location (Lekki), and budget, here are places that work for a Saturday night...",
  "next_turn_prompt": "Want me to narrow to places with live music?",
  "cold_start_used": false,
  "ndcg_at_10": 0.847
}
```

### 5.6 Evaluation Metrics (Task B)

| Metric | Points | Method |
|---|---|---|
| NDCG@10 | 30 | Standard ranking eval |
| Hit Rate @5 | 30 | % relevant items in top 5 |
| Cold-Start Performance | 25 | Separate cold-start test set |
| Cross-Domain Transfer | 25 | Cross-category hit rate |
| Contextual Relevance | 20 | Human eval panel |

---

## 6. Supabase Feature Integration

### 6.1 Authentication with OAuth
- Google OAuth for team/judge demo access
- Session-bound user context isolates each demo persona
- `AuthContext.tsx` wraps the React app; all API calls inject `Authorization: Bearer <token>`

```typescript
// src/contexts/AuthContext.tsx
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: { redirectTo: `${window.location.origin}/dashboard` }
});
```

### 6.2 Row Level Security (RLS)
All persona data and review history is locked per authenticated session — critical for multi-team judging demos.

```sql
-- RLS: personas table
CREATE POLICY "Users see own personas"
  ON personas FOR ALL
  USING (auth.uid() = user_id);

-- RLS: embeddings table  
CREATE POLICY "Users see own embeddings"
  ON user_embeddings FOR SELECT
  USING (auth.uid() = owner_id);
```

### 6.3 Real-time Subscriptions
Agent streaming responses are published via Supabase Realtime — judges see tokens arrive live in the UI, demonstrating the LLM agent's reasoning chain in real time.

```typescript
// Subscribe to agent output stream
const channel = supabase.channel(`agent-${sessionId}`)
  .on('broadcast', { event: 'token' }, ({ payload }) => {
    setAgentOutput(prev => prev + payload.token);
  })
  .subscribe();
```

### 6.4 Auto-generated REST APIs
CRUD for personas, products, and review history all via Supabase PostgREST — zero custom backend endpoints for data operations.

```typescript
// src/lib/supabase.ts
export const savePersona = async (persona: Persona) => {
  return supabase.from('personas').upsert(persona).select();
};
```

### 6.5 Database Functions & Triggers
Auto-timestamp maintenance and embedding update triggers.

```sql
-- Auto-update embedding when persona is modified
CREATE OR REPLACE FUNCTION refresh_persona_embedding()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM net.http_post(
    url := current_setting('app.edge_function_url') || '/embed-persona',
    body := row_to_json(NEW)::text
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER persona_embedding_refresh
  AFTER UPDATE ON personas
  FOR EACH ROW EXECUTE FUNCTION refresh_persona_embedding();
```

### 6.6 Edge Functions
Serverless handlers for embedding generation and post-submission notification.

```typescript
// supabase/functions/embed-persona/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

serve(async (req) => {
  const persona = await req.json();
  const embedding = await generateEmbedding(persona); // Groq API
  await supabaseClient
    .from('user_embeddings')
    .upsert({ owner_id: persona.user_id, embedding });
  return new Response(JSON.stringify({ success: true }));
});
```

---

## 7. Groq API Integration

Groq's free tier (LLaMA-3.1-70B-Versatile) is used as the primary inference backbone. The key advantages:
- **Sub-200ms latency** — enables streaming in the real-time demo
- **Free tier** — ample for hackathon volumes
- **LLaMA-3.1-70B** — strong multilingual and code-switching support

```python
# agents/persona_simulator.py
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_review(persona: dict, product: dict, context: dict, cvi_anchors: list) -> dict:
    system_prompt = f"""
    You are Naija Oracle — a cultural intelligence system that generates authentic Nigerian consumer reviews.
    
    VOICE PROFILE:
    - City: {persona['city']} | LGA: {persona['lga']}
    - Language: {persona['primary_language']} | Pidgin intensity: {persona['pidgin_intensity']:.1f}/1.0
    - Style: {persona['review_style']} | Avg rating: {persona['avg_rating']}
    
    CULTURAL ANCHORS (use similar voice):
    {chr(10).join(f'- "{a["phrase"]}" → {a["context"]}' for a in cvi_anchors)}
    
    Generate a review that sounds EXACTLY like this person. 
    Do NOT write generic English. Capture their voice.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Review this: {product['name']} in {product['location']}. Context: {context}"}
        ],
        temperature=0.85,
        max_tokens=400,
        stream=True
    )
    return response
```

---

## 8. Dataset Strategy

### Primary Datasets
| Dataset | Use | Size |
|---|---|---|
| Yelp Open Dataset | User modelling baseline, restaurant reviews | ~7M reviews |
| Amazon Reviews (Electronics, Fashion) | Cross-domain recommendation | ~10M reviews |
| Goodreads | Cold-start, literary taste transfer | ~15M reviews |

### Nigerian Augmentation Layer
To earn the bonus cultural fidelity marks, the system augments base datasets with:

1. **Synthetic Nigerian Persona Generation** — Use Groq to generate 500+ Nigerian user personas with realistic city/LGA/cultural distributions.
2. **CVI Construction** — Manually curated + Groq-assisted expansion of the Cultural Voice Index from Nigerian Twitter, Nairaland, and Jiji review samples.
3. **Location Grounding** — Map Yelp restaurant categories to Nigerian equivalents (`fast_food → mama_put/bukka`, `bar → joints`).

---

## 9. Evaluation Framework

### Automated Metrics Pipeline
```python
# evaluation/run_eval.py
class NaijaOracleEvaluator:
    def task_a_metrics(self, predictions, references):
        return {
            "bertscore_f1": compute_bertscore(predictions, references),
            "rouge_l": compute_rouge(predictions, references)["rougeL"],
            "rmse": compute_rmse(pred_ratings, true_ratings),
            "cvi_hit_rate": compute_cvi_hits(predictions, self.cvi_db)
        }
    
    def task_b_metrics(self, recommendations, ground_truth):
        return {
            "ndcg_at_10": compute_ndcg(recommendations, ground_truth, k=10),
            "hit_rate_at_5": compute_hit_rate(recommendations, ground_truth, k=5),
            "cold_start_ndcg": compute_cold_start_ndcg(...)
        }
```

### MLflow Experiment Tracking
Every experiment is logged to MLflow (hosted on DagsHub, consistent with the candidate's existing setup):
- Prompt template versions
- Temperature / sampling parameters
- Persona cluster configurations
- BERTScore / ROUGE / RMSE runs

---

## 10. API Specification

### Task A Endpoint
```
POST /api/v1/simulate-review
Content-Type: application/json
Authorization: Bearer <supabase_jwt>

Body: { user_id, persona, product, context }
Response: { predicted_rating, review_text, voice_profile_used, behavioural_fidelity_score }
```

### Task B Endpoint
```
POST /api/v1/recommend
Content-Type: application/json
Authorization: Bearer <supabase_jwt>

Body: { user_id, persona, context, domain, turn_history }
Response: { recommendations[], explanation, next_turn_prompt, ndcg_at_10 }
```

### Streaming Endpoint (Real-time Demo)
```
GET /api/v1/stream/{session_id}
Accept: text/event-stream

Pushes SSE tokens → Supabase Realtime channel → React UI
```

---

## 11. Docker Deployment

```yaml
# docker-compose.yml
version: '3.9'
services:
  api:
    build: ./backend
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
    ports:
      - "8000:8000"
  
  frontend:
    build: ./frontend
    environment:
      - VITE_SUPABASE_URL=${SUPABASE_URL}
      - VITE_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    ports:
      - "3000:3000"
    depends_on:
      - api
```

---

## 12. Scoring Strategy & Differentiation

### Points Target
| Category | Available | Target |
|---|---|---|
| Task B: Ranking Quality (NDCG@10) | 30 | 27 |
| Task B: Cold-Start & Cross-Domain | 25 | 22 |
| Task B: Contextual Relevance | 20 | 18 |
| Solution Paper | 15 | 15 |
| Code Reproducibility | 10 | 10 |
| **Nigerian Cultural Bonus** | **+5** | **+5** |
| **Total** | **105** | **97** |

### Why This Wins
1. **The Nigerian Voice Layer is unreplicable in 3 weeks** without cultural knowledge. Most teams will produce technically sound but culturally tone-deaf outputs.
2. **The CVI bonus is free marks** — the brief explicitly states additional marks for Nigerian contextualisation, and most international-style solutions will skip this.
3. **Groq's speed enables live demos** — streaming responses in the UI during the judging presentation creates a wow moment that static API demos cannot match.
4. **Augustine's existing stack maps 1:1** — RAG (Financial Oracle project), MLOps (Network Security, AgriPreserve), FastAPI + Docker — zero ramp-up time.

---

## 13. Risk Mitigation

| Risk | Mitigation |
|---|---|
| Groq rate limits during demo | Pre-cache 20 demo scenarios in Supabase |
| BERTScore too low for Nigerian Pidgin | Use multilingual-bert; supplement with CVI hit rate as secondary signal |
| Cold-start cluster quality | Bootstrap from cultural onboarding questions; fallback to popularity baseline |
| Submission deadline (24 May) | Complete Task B first (higher points); Task A is additive |

---

## 14. Deliverables Checklist

- [ ] Containerised Task A API (FastAPI + Docker)
- [ ] Containerised Task B API (FastAPI + Docker)
- [ ] Solution Paper (4–8 pages, LaTeX or Google Docs)
- [ ] GitHub Repository (clean, modular, README.md)
- [ ] MLflow experiment logs (public DagsHub link)
- [ ] Live demo URL (Render or Railway deployment)

---

*Naija Oracle — because the machine should sound like it grew up here.*
