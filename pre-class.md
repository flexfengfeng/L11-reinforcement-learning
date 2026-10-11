# Before the session — L11 — Reinforcement Learning

**Estimated time: ~15 minutes.** This is a bonus lesson, so the warm-up is light. You can
even do it in the first few minutes of the session if you're short on time.

This warm-up has no code. Its only job is to get one idea into your head before you build:
**RL learns without an answer key.** Everything in the session hangs off that.

| Step | Time | What you do |
|---|---|---|
| **1. Play** | ~8 min | Open the interactive explainer and turn the dial |
| **2. Reflect** | ~5 min | Three short questions below |

---

## Step 1 — Play with the explainer (~8 min)

Open **`interactive/rl_explorer.html`** in any web browser (just double-click it). There's
nothing to install.

You'll see NorthStar's homepage choosing between three product banners. Each banner has a
hidden true click rate the agent can't see. Drag the **exploration dial** (`epsilon`) and
watch what changes:

- Set it near **0** — the agent almost never tries alternatives.
- Set it near **1** — the agent picks at random every time.
- Find the **sweet spot** in between where the agent learns fastest.

You don't need to understand *why* yet. Just build a feel for "more exploring" vs "more
using what I already know."

---

## Step 2 — Quick reflection (~5 min)

Jot a sentence for each — on paper, in a notes app, or just in your head.

**Q1. Every model you built in L01–L10 learned from labelled examples — an answer key.**

This homepage problem has no answer key: nobody can tell you in advance which banner is
"correct" for a visitor. So how could a system *possibly* learn the best banner? Take a
guess before the session answers it.

**Q2. There's a cost to trying a banner you're unsure about.**

Every time you show a *worse* banner just to learn about it, you probably lose a click.
But if you *never* try alternatives, you might be stuck on a mediocre one forever. In your
own words: what's the tension here?

**Q3. Name one real system that "gets better the more it's used."**

A game-playing AI, a recommendation feed, a robot learning to walk — anything. Hold it in
mind; by the end you'll see they all run the same loop.

---

## Bring to the session

- Your gut answer to Q1 — how *could* a system learn with no labels?
- One thing the explainer did that surprised you.

**Ran out of time?** Just open the explainer for two minutes and drag the dial. That single
bit of hands-on feel is enough to start.
