# Naija Oracle — Frontend PRD & Design System
### Visual Identity, Page Architecture & Component Specification

---

## 1. Design Philosophy

**Naija Oracle** rejects the sterile grey-and-purple aesthetic that plagues most AI products. The visual language draws from:

- **Adire textile patterns** — Yoruba hand-dyed indigo fabric, with its organic geometric repeat patterns, inspires the background textures and accent motifs
- **Lagos at golden hour** — warm amber gradients, deep terracotta, and burnt orange anchor the colour palette against rich near-black backgrounds
- **Market energy** — controlled density, layered information, confident typography — like a Balogun Market stall that knows exactly where everything is

This is not "African-themed" in a clichéd way. It is **precise and modern**, with cultural texture woven into the details, not splashed across the surface.

---

## 2. Colour System

```css
:root {
  /* Core */
  --oracle-void:      #0C0B09;   /* Near-black background */
  --oracle-charcoal:  #1A1916;   /* Card surfaces */
  --oracle-smoke:     #2A2825;   /* Elevated surfaces */
  --oracle-ash:       #3D3B37;   /* Borders, dividers */
  
  /* Naija Amber — primary accent */
  --oracle-amber-900: #7A3B00;
  --oracle-amber-700: #C46200;
  --oracle-amber-500: #F5831F;   /* PRIMARY CTA */
  --oracle-amber-300: #FFBA70;
  --oracle-amber-100: #FFF0DC;
  
  /* Terracotta — secondary accent */
  --oracle-terra-700: #8B2500;
  --oracle-terra-500: #C94020;
  --oracle-terra-300: #F28060;
  
  /* Indigo — data/info */
  --oracle-indigo-700: #1E2A6E;
  --oracle-indigo-500: #3B4EBF;
  --oracle-indigo-300: #7B8FE8;
  --oracle-indigo-100: #D0D6FF;
  
  /* Success / Positive */
  --oracle-green-500: #2DB37A;
  --oracle-green-300: #6DDCAA;
  
  /* Text hierarchy */
  --text-primary:    #F0EDE8;    /* Near-white, warm */
  --text-secondary:  #9A9590;    /* Muted warm grey */
  --text-tertiary:   #5C5955;    /* Hints */
  
  /* Adire pattern accent */
  --adire-stroke:    rgba(245, 131, 31, 0.12);  /* Subtle pattern overlay */
}
```

---

## 3. Typography

```css
/* Display / Hero */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,700;1,300&display=swap');
/* Body / UI */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');
/* Mono / Code / Data */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

/* Scale */
--font-hero:       clamp(3rem, 6vw, 5.5rem);  /* Landing headline */
--font-display:    clamp(2rem, 4vw, 3rem);     /* Section headers */
--font-heading:    1.5rem;                     /* Card/page titles */
--font-subheading: 1.125rem;
--font-body:       1rem;
--font-small:      0.875rem;
--font-micro:      0.75rem;
```

**Font pairings:**
- **Fraunces** (serif, 300–700) → Hero headings, pull quotes, the "Oracle" wordmark
- **DM Sans** (300–500) → All UI text, navigation, body copy
- **JetBrains Mono** → JSON outputs, code snippets, metric values

---

## 4. Page Architecture

```
/                   → Landing Page
/auth               → OAuth Login
/dashboard          → Main Hub
/simulate           → Task A: Review Simulator Playground
/recommend          → Task B: Recommendation Engine Playground
/persona/:id        → Persona Detail View
/demo               → Guided Live Demo (for judges)
/docs               → API Documentation (Swagger UI embedded)
```

---

## 5. Landing Page

### 5.1 Above-the-fold Hero

**Layout:** Full-viewport dark canvas with a central hero block. No navbar on first load — fades in on scroll.

**Background:** Subtle SVG Adire repeat pattern at 4% opacity — geometric circles and interlocking lines in `--adire-stroke`. A radial gradient from `--oracle-amber-500` at 8% opacity centres behind the headline, casting a barely-there warm glow.

**Hero Text:**
```
Fraunces 300 italic — "The oracle that"
Fraunces 700 bold — "speaks Naija."
DM Sans 400 — "LLM agents that simulate Nigerian consumer voices 
                and deliver hyper-personalised recommendations."
```

**CTA Block:**
- Primary button: `"Try the Oracle"` → `/demo` — Amber fill, dark text, 48px height, rounded-full, subtle pulse animation
- Secondary: `"View on GitHub"` → ghost button with amber border

**Hero Image:** A split illustration — left half shows a stylised review card with Pidgin text glowing amber; right half shows a recommendation grid with location pins in terracotta. Created as inline SVG, not a stock image.

**Scroll indicator:** Thin amber vertical line pulsing downward, `↓` in Fraunces italic.

---

### 5.2 Stats Bar (below hero)
Dark surface `--oracle-charcoal`, 80px tall, 4-column grid:

```
2 Agents Built    |   3 Datasets   |   500+ Personas   |   <200ms Latency
```
Numbers in JetBrains Mono amber; labels in DM Sans secondary.

---

### 5.3 "How It Works" Section

**Background:** `--oracle-void` with Adire pattern at 3% opacity

**Layout:** 2-column — left sticky text explaining the concept; right scrolling cards demonstrating each step.

**Step Cards** (terracotta left-border accent):
1. "Give us a persona" — user fills city, age, cultural markers
2. "Oracle reads the voice" — animated CVI lookup
3. "Reviews + Recs generated" — streamed output with Pidgin markers highlighted in amber

---

### 5.4 Live Demo Embed

Full-width panel, `--oracle-charcoal` background, with a pre-loaded persona and a "Run Oracle" button. When clicked, the review streams character-by-character in JetBrains Mono with Pidgin phrases highlighted in `--oracle-amber-300`.

---

### 5.5 Cultural Voice Section

**Headline (Fraunces italic):** *"E go sound like them."*

Three side-by-side cards showing the same product reviewed by three personas:
- **Emeka, 28, Port Harcourt** → Igbo code-switching + Pidgin
- **Aisha, 33, Kano** → Hausa markers + formal register
- **Tunde, 25, Lagos** → Heavy Lagos Pidgin + slang

Each card has a `"Voice confidence"` meter bar in amber showing CVI hit rate.

---

### 5.6 Footer

Minimal — project name in Fraunces, GitHub link, hackathon attribution (DSN × BCT). No social links. The footer has a subtle Adire border at the top (1px dashed amber at 20% opacity).

---

## 6. Dashboard

### 6.1 Navigation
Left sidebar, 240px, `--oracle-charcoal` background.

```
[Naija Oracle logo + wordmark]
─────────────────────────────
Overview
Simulate Review    [Task A]
Get Recommendations [Task B]
Personas
Experiments (MLflow)
API Docs
─────────────────────────────
[User avatar + email]
[Sign out]
```

Active nav item: left amber bar (3px), amber text.

### 6.2 Overview Page

4 metric cards in a 2×2 grid:
- Reviews Generated (total)
- Avg BERTScore (latest run)
- Avg NDCG@10 (Task B)
- CVI Hit Rate (current session)

Below: a live feed panel showing recent agent activity (Supabase Realtime subscription), each entry as a compact row:
```
[timestamp]  [persona name]  [product]  [⭐ 3.5]  [View →]
```

Below that: an experiment comparison chart (Chart.js bar chart) showing BERTScore across 5 recent prompt template versions.

---

## 7. Task A — Review Simulator Playground (`/simulate`)

### 7.1 Page Layout
Two-panel layout:
- **Left panel (420px):** Input controls
- **Right panel (flex):** Live output

### 7.2 Left Panel: Input Controls

**Section: User Persona**
- City dropdown (Lagos, Abuja, PH, Kano, Enugu, Ibadan)
- LGA text input
- Primary language (Yoruba / Igbo / Hausa / Pidgin / English)
- Review style (Expressive / Analytical / Casual / Terse)
- Pidgin intensity slider — 0 to 100%, with live label: *"Like Sunday Church"* → *"Like owambe DJ"*
- Sample review textarea (optional — paste 1-2 real reviews)

**Section: Product**
- Product name
- Category (fast food / restaurant / fashion / fintech / entertainment)
- Price tier (Budget / Mid / Premium)
- Location

**Section: Context**
- Time of day (Morning / Afternoon / Evening / Late Night)
- Occasion (Casual / After Work / Date / Celebration / Impulse)
- First visit toggle

**CTA:** `"Generate Review"` — full-width amber button, 52px

### 7.3 Right Panel: Output

Loading state: skeleton shimmer in `--oracle-smoke` + amber pulsing dot "Oracle is thinking..."

Output card (`--oracle-charcoal`, amber top-border):
```
┌─ [User Avatar Initial] Emeka O. · Lagos · Expressive ─────┐
│                                                            │
│  ⭐⭐⭐⭐  (Predicted: 3.8 / Confidence ±0.4)             │
│                                                            │
│  "The jollof rice fine die o, but service slow like NEPA   │
│   restoring light on a weekday. I go come back sha but     │
│   abeg arrange the queue."                                  │
│                                                            │
│  ─ Behavioural Fidelity: ████████░░ 82%                   │
│  ─ CVI Anchors: "fine die o" · "slow like NEPA" · "sha"   │
│  ─ Pidgin Intensity: 0.74                                  │
└────────────────────────────────────────────────────────────┘
```

Pidgin anchor phrases highlighted inline in amber background pill style.

Below: "Regenerate with different voice" ghost button + "Export JSON" button.

---

## 8. Task B — Recommendation Playground (`/recommend`)

### 8.1 Page Layout
Chat-style interface on the right; persona context panel on the left.

### 8.2 Chat Interface (right, 60% width)

Messages styled with dark bubbles. Agent messages have a small `[Oracle]` badge in terracotta.

Multi-turn example flow:
```
[User]   I want to chop good food around Lekki tonight
[Oracle] Based on your profile (Lagos, celebratory mood, ₦5k budget)...
         Here are 5 spots:
         [Card 1] Yellow Chilli — Nigerian fine dining [4.4⭐]
         [Card 2] ...
[User]   Any with live music?
[Oracle] Narrowing for live music...
```

Recommendation cards within chat:
- Restaurant name + category
- Predicted rating (amber stars)
- Distance + price tier
- One-line reasoning (DM Sans 300, secondary colour)
- "Why this?" expand toggle that shows the agent's reasoning chain

### 8.3 Context Panel (left, 40% width)

Sticky panel showing the current active persona:
- Persona name + city
- Mood signal (editable)
- Budget (editable)
- Location (editable)

Below: NDCG@10 live tracker — updates after each recommendation batch.

---

## 9. Persona Detail Page (`/persona/:id`)

Full-page persona card. Adire-inspired decorative header in amber/terracotta.

**Sections:**
- Profile (city, LGA, age range, language)
- Voice Fingerprint (radar chart — 5 axes: Pidgin intensity, Sentiment volatility, Price sensitivity, Brand loyalty, Review length)
- Review History (table — product, rating, excerpt, CVI score)
- Recommendation History (table)
- Edit Persona CTA

---

## 10. Component Library

### Buttons
```css
.btn-primary {
  background: var(--oracle-amber-500);
  color: var(--oracle-void);
  font-family: 'DM Sans'; font-weight: 500;
  padding: 12px 28px; border-radius: 6px;
  transition: background 0.15s, transform 0.1s;
}
.btn-primary:hover { background: var(--oracle-amber-300); }
.btn-primary:active { transform: scale(0.98); }

.btn-ghost {
  background: transparent;
  border: 1px solid var(--oracle-amber-700);
  color: var(--oracle-amber-300);
  /* same padding + radius */
}
```

### Cards
```css
.card {
  background: var(--oracle-charcoal);
  border: 1px solid var(--oracle-ash);
  border-radius: 10px;
  padding: 20px 24px;
}
.card--amber-accent {
  border-top: 3px solid var(--oracle-amber-500);
}
.card--terra-accent {
  border-left: 3px solid var(--oracle-terra-500);
}
```

### Metric Badge
```
[BERTScore: 0.84]  ← amber pill, JetBrains Mono, 13px
[NDCG@10: 0.847]   ← green pill
[CVI: 74%]         ← terracotta pill
```

### Pidgin Highlight
```css
.pidgin-anchor {
  background: rgba(245, 131, 31, 0.18);
  color: var(--oracle-amber-300);
  border-radius: 3px;
  padding: 1px 5px;
  font-style: italic;
}
```

### Streaming Cursor
Amber blinking cursor `|` at end of streaming text. CSS animation at 600ms.

---

## 11. Motion Design

**Philosophy:** Motion communicates state, not decoration. Every animation has a reason.

| Animation | Trigger | Duration | Easing |
|---|---|---|---|
| Hero fade-in | Page load | 800ms | ease-out |
| Nav fade-in | Scroll > 80vh | 300ms | ease |
| Card entry | Intersection Observer | 400ms | cubic-bezier(0.16, 1, 0.3, 1) |
| CTA pulse | Idle > 3s | 2s loop | ease-in-out |
| Oracle streaming cursor | Streaming active | 600ms loop | step-end |
| Fidelity bar fill | Output received | 600ms | ease-out |
| Recommendation card reveal | Staggered, 80ms delay | 350ms each | ease-out |

All animations respect `prefers-reduced-motion: reduce`.

---

## 12. Responsive Breakpoints

| Breakpoint | Layout |
|---|---|
| > 1280px | Full two-panel layouts |
| 1024–1280px | Reduced left panel (320px) |
| 768–1024px | Stacked panels, full width |
| < 768px | Mobile — single column, drawer navigation |

---

## 13. Accessibility

- Colour contrast: all text pairs ≥ 4.5:1 against backgrounds
- Focus rings: 2px amber outline on all interactive elements
- Streaming output: announced via `aria-live="polite"`
- Adire pattern: purely decorative, `aria-hidden="true"`
- All charts have accessible table fallbacks

---

## 14. Assets Checklist

- [ ] Naija Oracle logotype (Fraunces italic "Oracle" + DM Sans "Naija")
- [ ] Adire SVG pattern tile (geometric, amber on transparent)
- [ ] Hero illustration SVG (split review/recommendation scene)
- [ ] Persona avatar system (initials circles, city-coded colour)
- [ ] Empty state illustrations (3 × simple line art)
- [ ] Favicon (stylised "N" in amber on dark)

---

*The interface should feel like opening a Bloomberg terminal designed by someone who grew up in Lagos.*
