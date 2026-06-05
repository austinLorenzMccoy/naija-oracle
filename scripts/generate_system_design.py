"""Generate Naija Oracle system design diagram for LinkedIn."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

BG        = '#0C0B09'
CHARCOAL  = '#1C1A17'
SMOKE     = '#2A2825'
ASH       = '#3D3B37'
AMBER     = '#F5831F'
TERRA     = '#C94020'
GREEN     = '#2DB37A'
BLUE      = '#4A8FD4'
PURPLE    = '#8B6DB5'
TEXT1     = '#F0EDE8'
TEXT2     = '#9A9590'
TEXT3     = '#6A6560'

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')


def box(cx, cy, w, h, edge_color, label, sub=None, tag=None,
        label_color=None, sub_color=TEXT2):
    lc = label_color or edge_color
    bg = edge_color + '18'
    rect = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.08',
        facecolor=CHARCOAL, edgecolor=edge_color,
        linewidth=1.8, zorder=3,
    )
    ax.add_patch(rect)
    ty = cy + (0.18 if sub else 0)
    ax.text(cx, ty, label, ha='center', va='center',
            color=lc, fontsize=9.5, fontweight='bold',
            fontfamily='DejaVu Sans Mono', zorder=4)
    if sub:
        ax.text(cx, cy - 0.22, sub, ha='center', va='center',
                color=sub_color, fontsize=7.5, fontfamily='DejaVu Sans Mono',
                zorder=4)
    if tag:
        ax.text(cx - w / 2 + 0.15, cy + h / 2 - 0.12, tag,
                ha='left', va='top', color=edge_color,
                fontsize=6.5, fontfamily='DejaVu Sans Mono',
                fontweight='bold', zorder=5)


def arrow(x1, y1, x2, y2, color=ASH, lw=1.4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=color, lw=lw,
                    connectionstyle='arc3,rad=0.0',
                ), zorder=2)


def bullet_list(cx, top_y, items, color=TEXT2, size=7.2):
    for i, item in enumerate(items):
        ax.text(cx, top_y - i * 0.28, f'· {item}',
                ha='center', va='center', color=color,
                fontsize=size, fontfamily='DejaVu Sans Mono', zorder=4)


# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(8, 9.65, 'NAIJA ORACLE', ha='center', va='center',
        color=AMBER, fontsize=22, fontweight='bold',
        fontfamily='DejaVu Sans Mono', zorder=4)
ax.text(8, 9.28, 'Dual-Agent LLM System for Nigerian Consumer Intelligence',
        ha='center', va='center', color=TEXT2, fontsize=9,
        fontfamily='DejaVu Sans Mono', zorder=4)

# thin divider
ax.plot([1, 15], [9.08, 9.08], color=ASH, lw=0.6)

# ── User ──────────────────────────────────────────────────────────────────────
box(8, 8.55, 3.2, 0.62, AMBER, 'USER  /  BROWSER', tag='client')
arrow(8, 8.24, 8, 7.83, AMBER)

# ── Frontend ──────────────────────────────────────────────────────────────────
box(8, 7.55, 6.5, 0.72, AMBER,
    'NEXT.JS  ·  TAILWIND  ·  NETLIFY',
    sub='/simulate  ·  /recommend  ·  /cold-start  ·  /personas',
    tag='frontend')
arrow(8, 7.19, 8, 6.79, AMBER, lw=1.6)

# ── Backend ───────────────────────────────────────────────────────────────────
box(8, 6.52, 6.5, 0.62, GREEN,
    'FASTAPI  ·  RENDER',
    sub='CORS  ·  routing  ·  Netlify _redirects proxy  ·  Docker',
    tag='backend api')
# split arrows to agents
arrow(6.3, 6.21, 4.0, 5.64, TERRA, lw=1.4)
arrow(9.7, 6.21, 12.0, 5.64, BLUE, lw=1.4)

# ── Agent A ───────────────────────────────────────────────────────────────────
agent_a_cx = 4.0
box(agent_a_cx, 4.8, 6.6, 1.75, TERRA,
    'AGENT A  ·  PERSONA SIMULATOR', tag='task a')
bullet_list(agent_a_cx, 4.45, [
    'Cultural Voice Index (CVI)  —  28 phrases',
    'Tribe · Sentiment · Rating anchors',
    'Pidgin intensity control (0.0 – 1.0)',
    'Fidelity scoring  ·  Voice radar chart',
    'BERTScore F1 = 0.87  ·  CVI hit rate = 74%',
], color=TEXT2)

# ── Agent B ───────────────────────────────────────────────────────────────────
agent_b_cx = 12.0
box(agent_b_cx, 4.8, 6.6, 1.75, BLUE,
    'AGENT B  ·  RECOMMENDATION ENGINE', tag='task b')
bullet_list(agent_b_cx, 4.45, [
    'R4 Pipeline: Reason→Retrieve→Rank→Refine',
    'Cold-start: Suya / AMVCA / GTB onboarding',
    'Cross-domain transfer (food→fashion→music)',
    'Multi-turn context  ·  Contextual boost',
    'NDCG@10 = 0.89  ·  Hit Rate@5 = 0.82',
], color=TEXT2)

# arrows from agents to cultural layer
arrow(4.0, 4.0, 5.2, 3.44, TERRA)
arrow(12.0, 4.0, 10.8, 3.44, BLUE)

# ── Cultural Context Layer ────────────────────────────────────────────────────
box(8, 3.1, 11.5, 0.62, PURPLE,
    'NIGERIAN CULTURAL CONTEXT LAYER  (NCCL)',
    sub='CVI lexicon  ·  tribal archetypes  ·  location tiers  ·  seasonal signals  ·  language register',
    label_color='#B09CD8', tag='shared context')

# arrows to infra
arrow(4.5, 2.79, 3.2, 2.29, PURPLE)
arrow(8,   2.79, 8,   2.29, PURPLE)
arrow(11.5, 2.79, 12.8, 2.29, PURPLE)

# ── Infrastructure ────────────────────────────────────────────────────────────
box(3.2,  2.0, 5.0, 0.62, AMBER,
    'GROQ  ·  LLaMA-3.1-70B',
    sub='Sub-200ms inference  ·  API-based  ·  streaming', tag='inference')

box(8.0,  2.0, 4.2, 0.62, GREEN,
    'SUPABASE  ·  pgvector',
    sub='RLS  ·  Realtime  ·  Edge functions', tag='database')

box(12.8, 2.0, 5.0, 0.62, TEXT3,
    'sentence-transformers',
    sub='all-MiniLM-L6-v2  ·  persona embeddings',
    label_color=TEXT2, tag='embeddings')

# ── Footer divider + toolchain ────────────────────────────────────────────────
ax.plot([1, 15], [1.12, 1.12], color=ASH, lw=0.5)
ax.text(8, 0.72, 'MLflow  ·  DagsHub  ·  DVC  ·  PyTorch  ·  Docker Compose  ·  Apache 2.0',
        ha='center', va='center', color=TEXT3,
        fontsize=8, fontfamily='DejaVu Sans Mono')
ax.text(8, 0.35, 'naija-oracle.netlify.app  ·  github.com/austinLorenzMccoy/naija-oracle',
        ha='center', va='center', color=AMBER + '99',
        fontsize=7.5, fontfamily='DejaVu Sans Mono')

out = 'assets/naija_oracle_system_design.png'
plt.savefig(out, dpi=180, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
plt.close()
print(f'Saved → {out}')
