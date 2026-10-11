# L11 — Reinforcement Learning (a brief intro)

> **Module 3 · Machine Learning & GenAI · Bonus lesson — added by learner request**

## What this is

A short, optional introduction to **reinforcement learning (RL)** — the one major
branch of machine learning the main course (L01–L10) deliberately left out. Several
learners asked for "just enough RL to know what it is and how it differs from what we've
built." This lesson is that: a single hands-on code-along (60–90 minutes — Parts 1–4 are the ~70-minute core, Part 5 is an optional stretch) where you build a
recommender that learns from clicks, plus an interactive explainer you can play with.

It is **lighter than L01–L10 on purpose.** There is no assignment and no quiz — just one notebook, one interactive page, and a short
slide deck to run the session from. Treat it as a guided taster, not a full
module.

## Where it sits in the story

One more chapter for Sarah Chen at NorthStar Retail — set *after* the main arc closes:

> *A few months after the L10 launch.* Sarah's churn model and shopping assistant are live. Now Marcus wants the
> homepage to **recommend the right product banner to each visitor** — and to *get better
> on its own* as real shoppers click. Nobody has a labelled "correct banner" list. The
> system has to learn by trying.

That last sentence is the whole reason this is a **reinforcement learning** problem, not a
supervised one. Every model in L01–L10 learned from an answer key. Here there is no answer
key — the only feedback is whether each visitor clicked.

## What you'll learn

By the end you will be able to:

1. **Name the RL loop** — agent → action → reward → update, repeated thousands of times.
2. **Explain the six core words** — agent, environment, action, reward, policy, value — each tied to code you actually ran.
3. **Describe the explore-vs-exploit trade-off** — and point to the single dial (`epsilon`) that controls it.
4. **Say clearly how RL differs from supervised learning** — no labels; the agent learns from the reward of what it tried.
5. **(Optional)** Recognise a **contextual bandit** and the **Q-table**, and see how the same loop scales up to full RL and to RLHF behind modern chatbots.

## How it's taught — one Kolb cycle, five parts

The notebook follows the same learn-by-doing rhythm as the rest of the course: you build
first, then reflect, then name the theory, then experiment.

| Part | Kolb stage | What you do | Time |
|---|---|---|---|
| **1 — Do it** | Concrete experience | Build a random baseline, then an ε-greedy agent that learns which banner wins | ~25 min |
| **2 — Look at it** | Reflective observation | Three questions about what just happened, then compare with Sarah's take | ~10 min |
| **3 — Name it** | Abstract conceptualisation | The theory in plain English — every term mapped to your code | ~20 min |
| **4 — Tinker** | Active experimentation | Turn the `epsilon` dial, change the world, watch behaviour shift | ~15 min |
| **5 — Go deeper** *(optional)* | Stretch | Add context → contextual bandit → the Q-table → where full RL leads | ~20 min |

## Files

| Path | Purpose |
|------|---------|
| `README.md` | This file — orientation |
| `pre-class.md` | ~15-min warm-up before the session |
| `lesson.md` | Short reference: overview, key takeaways, review questions, where RL goes next |
| `notebooks/01_rl_recommender_codealong.ipynb` | The lesson — build a recommender that learns from clicks |
| `interactive/rl_explorer.html` | Interactive explainer — drag the `epsilon` dial and watch explore vs exploit live |
| `slides/L11_slides_ntu.pptx` | NTU-template slide deck (25 slides, speaker notes) that follows the notebook's five parts |

## How to run

Open `notebooks/01_rl_recommender_codealong.ipynb` in VS Code with the `dsai-m3` kernel and
run every cell top to bottom. It uses only `numpy` and `matplotlib` — no new installs, no
GPU, no model downloads. The notebook runs in seconds on any laptop.

Prefer to explore without code first? Open `interactive/rl_explorer.html` in any browser.
