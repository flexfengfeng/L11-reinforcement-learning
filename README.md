# L11 — Reinforcement Learning (a brief intro)

> **Module 3 · Machine Learning & GenAI · Bonus lesson — added by learner request**

## What this is

A short, optional introduction to **reinforcement learning (RL)** — the one major
branch of machine learning the main course (L01–L10) deliberately left out. Several
learners asked for "just enough RL to know what it is and how it differs from what we've
built." This lesson is that: a single hands-on code-along (80–110 minutes — ~20 minutes of key ideas on the slides, then Parts 1–4 as the ~70-minute notebook core; Part 5 is an optional ~20-minute stretch) where you build a
recommender that learns from clicks, plus an interactive explainer you can play with.

It is **lighter than L01–L10 on purpose.** There is no assignment and no quiz — the learner materials are one notebook, one interactive page, and short reference notes. Treat it as a guided taster, not a full
module.

## Where it sits in the story

One more chapter for Sarah Chen at NorthStar Retail — set *after* the main arc closes:

> *A few months after the L10 launch.* Sarah's churn model and shopping assistant are live. Now Marcus wants the
> homepage to **recommend the right product banner to each visitor** — and to *get better
> on its own* as real shoppers click. Nobody has a labelled "correct banner" list. The
> system has to learn by trying.

That last sentence points toward a **reinforcement learning** problem. More precisely, this
is a **multi-armed bandit**: a simple, stateless RL
setting where the agent repeatedly chooses one action, observes that action's reward, and
then chooses again. A click log can still contain labels, and the absence of labels alone
does not prove that RL is the right tool. The distinctive feature here is that the agent
chooses which banner to show, and that choice determines which feedback it gets.

## What you'll learn

By the end you will be able to:

1. **Name the RL loop** — agent → action → reward → update, repeated thousands of times.
2. **Explain the seven core words** — agent, environment, state, action, reward, policy, value — each tied to code you actually ran (state is "nothing yet" in the bandit, until Part 5 adds visitor type).
3. **Describe the explore-vs-exploit trade-off** — and point to the single dial (`epsilon`) that controls it.
4. **Say clearly how this bandit differs from supervised learning** — the agent chooses an action, receives feedback for that choice, and improves its future choices.
5. **(Optional)** Recognise a **contextual bandit** and its context-action value table, and see how the same loop scales up to sequential RL and to RLHF behind modern chatbots.

## How it's taught — one Kolb cycle, five parts

The notebook follows the same learn-by-doing rhythm as the rest of the course: you build
first, then reflect, then name the theory, then experiment.

| Part | Kolb stage | What you do | Time |
|---|---|---|---|
| **1 — Do it** | Concrete experience | Build a random baseline, then an ε-greedy agent that learns which banner wins | ~25 min |
| **2 — Look at it** | Reflective observation | Three questions about what just happened, then compare with Sarah's take | ~10 min |
| **3 — Name it** | Abstract conceptualisation | The theory in plain English — every term mapped to your code | ~20 min |
| **4 — Tinker** | Active experimentation | Turn the `epsilon` dial, change the world, watch behaviour shift | ~15 min |
| **5 — Go deeper** *(optional)* | Stretch | Add context → contextual bandit → an action-value table → where full RL leads | ~20 min |

## Files

| Path | Purpose |
|------|---------|
| `README.md` | This file — orientation |
| `pre-class.md` | ~15-min warm-up before the session |
| `lesson.md` | Short reference: overview, key takeaways, review questions, where RL goes next |
| `notebooks/01_rl_recommender_codealong.ipynb` | The lesson — build a recommender that learns from clicks |
| `docs/index.html` | Interactive explainer — drag the `epsilon` dial and watch explore vs exploit live |


## How to run

Create a fresh environment if needed, then open
`notebooks/01_rl_recommender_codealong.ipynb` in VS Code:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

The examples use `numpy` and `matplotlib`; `ipykernel` supports notebook execution,
and `nbformat`/`nbclient` support automated checks. In VS Code, install the Python and
Jupyter extensions, select the `.venv` kernel, and run every cell top to bottom.
A separate Jupyter server application is optional. There is no GPU or model download, and the notebook runs in
seconds on any laptop.

The slide deck is instructor-only and is not distributed with this repository. The
notebook, this reference, and the interactive page are the learner materials.

Prefer to explore without code first? Open `docs/index.html` in any browser.

## Checks

With the environment above active:

```bash
python -m unittest discover -s tests -v
node tests/test_explorer.cjs
```

The JavaScript check needs Node.js and no npm packages. It checks simulation and event
handler behavior using a minimal DOM stub; it does not replace visual browser checks.
For full notebook validation, run all cells in a fresh kernel. Saved outputs are from
a complete run; individual experiments use explicit seeds and report stochastic variability.
