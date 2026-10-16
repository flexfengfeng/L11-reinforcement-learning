# Lesson — L11 Reinforcement Learning (bonus intro)

> **A bonus chapter of the NorthStar Retail story — added by learner request.** *Sarah Chen · Customer Experience Analyst · NorthStar Retail · a few months after the L10 launch.*
> Sarah's churn model and shopping assistant are live. Marcus's new ask: *"Make the homepage recommend the right product banner to each visitor — and get better on its own as real shoppers click."* There's no labelled "correct banner" list. The system has to learn by trying.
> That is a useful RL example because the agent chooses which banner to show, receives the resulting feedback, and uses it to choose again. The missing "correct banner" list helps motivate the example, but the absence of labels by itself does not define RL.

This document is a **short reference** — the lesson itself is taught in the notebook. Read it for orientation, then come back to it for the takeaways, the "is this an RL problem?" checklist, the review questions, and where RL goes next. This is a lighter, optional lesson: one code-along, no assignment, no quiz.

---

## How L11 is taught

| Stage | Where to go |
|---|---|
| **Warm-up** | `pre-class.md` + `interactive/rl_explorer.html` |
| **Part 1 — Do it** | `notebooks/01_rl_recommender_codealong.ipynb` (build a random baseline, then an ε-greedy agent) |
| **Part 2 — Look at it** | same notebook — reflect on what happened |
| **Part 3 — Name it** | same notebook — the theory, each term tied to your code |
| **Part 4 — Tinker** | same notebook — turn the `epsilon` dial |
| **Part 5 — Go deeper** *(optional)* | same notebook — contextual bandit & an action-value table |

The notebook is the spine. Run it top to bottom. Come back here for the consolidated takeaways and review questions.

---

## Overview

For ten lessons, most of Sarah's models predicted a fixed target from an existing dataset. L11 instead starts with a **multi-armed bandit**, the simplest useful RL setting: there is no changing state between rounds, and each round is one action followed by one reward. NorthStar's homepage can show one of three banners — *A · New arrivals*, *B · 50% off*, *C · Trending now* — and the feedback is whether the banner shown gets clicked. Nobody knows in advance which banner is best; the system must **discover it by trying banners and watching clicks.**

The lesson builds that system twice. First a **random baseline** that shows banners with no strategy — the number any real method has to beat. Then an **ε-greedy agent** that keeps a running click-rate scoreboard, mostly shows the best banner so far, but explores a random one a small fraction of the time. Watching reward estimates guide decisions — while choices determine which evidence arrives — is the RL loop in miniature. A finite-run click-rate curve can rise or fall. Part 3 then names every moving piece, Part 4 lets you turn the exploration dial, and an optional Part 5 adds visitor **context** to reach a contextual bandit with a context-action value table. The whole point is one mindset shift: supervised learning learns to predict targets; reinforcement learning learns how to choose actions to earn reward.

---

## Key takeaways

1. **This lesson is a multi-armed bandit.** It is a stateless, one-step RL problem: the agent chooses one banner, gets a click reward, updates its estimate, and starts the next round. Full RL also handles changing states and long-term consequences.
2. **RL is an action-feedback loop.** An agent observes its situation, takes an action, receives a reward, and updates how it will act next time — repeated thousands of times. The absence of a ready-made answer key can be a clue, but it is not a definition: offline RL can learn from logged trajectories, and supervised models can predict rewards or preferences.
3. **Six words cover the vocabulary.** *Agent* (the learner), *environment* (the world it acts on), *action* (what it does), *reward* (the feedback), *policy* (its strategy for choosing), and *value* (its estimate of how good a choice is). Each maps directly to a line in the banner code.
4. **Explore vs. exploit is a central tension.** *Exploit* = use what you know to get reward now; *explore* = try actions to gain information, potentially sacrificing immediate reward. Exploring can also earn reward; the trade-off is how much to prioritize information.
5. **`epsilon` is the dial for that trade-off, not a universal setting.** `epsilon = 0.1` means explore 10% of the time, exploit the rest. Too low (`0`) and the agent can lock onto a banner that got lucky early; too high (`1.0`) is the random baseline. The best setting depends on the cost of exploration, the time horizon, and whether rates change. In this stationary toy world, values around `0.05`–`0.1` are useful examples, not a general rule. With perfect estimates, the 11% oracle that always chooses B becomes about **10.7%** at `epsilon = 0.1`: 90% exploitation plus 10% random choices.
6. **Results are stochastic.** A single run can look unusually good or bad because clicks and early choices are random. Compare independent seeds and report a mean, a standard deviation, and how often the agent identifies the best banner before drawing conclusions.
7. **The agent learns a policy, not "the rules."** It never learns the true click rates as facts; it learns *what to do* — which banner to show — from the reward each click gave. That estimated click-rate scoreboard is its value estimate; "mostly show the best" is its policy. The sample-average update is a good fit for this stationary simulator, but it adapts slowly if rates change; a recency-weighted update is a better next experiment for a non-stationary world.
8. **Context turns a bandit into a smarter recommender.** A first-time visitor and a loyal member may respond to different banners. A **contextual bandit** can keep an action-value table — a score per action *for each kind of situation*, often written `Q(context, action)` — and choose based on what it knows before acting. That table is not yet Q-learning: Q-learning is a sequential method that updates values toward future rewards.
9. **Full RL adds sequences.** A bandit's choices are independent; full reinforcement learning is for when your action *changes the world's state*, so you must weigh long-term reward, not just the next click. Q-learning over states, policy gradients, and deep RL are this same loop scaled up — and it's how chatbots are tuned with RLHF.

---

## Is this an RL problem? — a quick teaching heuristic

Use these questions to orient yourself, not as a strict taxonomy:

1. **Is the goal prediction from fixed examples?** Start with supervised learning when you have a target to predict. A model can also predict clicks, rewards, or preferences as part of an RL system.
2. **Must an agent choose actions and learn from feedback caused by those choices?** That action-feedback loop is the signal that RL may fit. RL can use live interaction or logged trajectories (offline RL), so the mere absence of labels is not enough.
3. **Can you measure reward and safely explore?** RL needs feedback — clicks, score, revenue, or a preference — and some trials may be worse than the current best. Use a simulator, constraints, or a safer method when experimentation is costly.

The banner problem has actions (which banner to show), rewards (click/no click), and cheap repeated experiments. Because each round is independent and has no changing state, it is specifically a multi-armed bandit.

---

## Check your understanding

Work through these after the notebook. Attempt each on your own first.

**Q1 — Why isn't this supervised learning?** Marcus says: "We have thousands of past visits and whether each clicked — that's labelled data. Why not just train a classifier?" What's the gap?

> **Sample answer:** A classifier trained on past visits could predict "will this visitor click *the banner we happened to show them*?" That can be useful, but it does not directly reveal what the *other* banners would have earned. The counterfactual outcome was never observed. This bandit closes the gap by *acting*: it deliberately shows different banners, collects the reward each earns, and improves its choice from that. The key distinction is the action-feedback loop, not simply whether the data has labels.

**Q2 — The `epsilon = 0` trap.** What can go wrong if the agent never explores, and why is a little exploration "insurance"?

> **Sample answer:** With `epsilon = 0` the agent shows each banner once, then always shows whichever banner currently looks best. If a genuinely weaker banner gets a lucky early click, its running average jumps to the top, the agent commits to it, and — because it never tries the others again — it never collects the evidence that would correct the mistake. It gets stuck. A positive exploration rate gives every banner a chance of more traffic, but does not guarantee identification within a finite visitor budget. Exact ties are broken randomly, so the common all-zero warm-up does not systematically favor A. That ongoing trickle of trials is the insurance premium against bad early luck.

**Q3 — What did the agent actually learn?** It was never told the true click rates (5% / 11% / 8%). So what did it learn?

> **Sample answer:** It learned a **policy** — a rule for what to do — not the rules of the world. Its scoreboard of estimated click rates (its *value* estimates) aims to approximate the true 5/11/8%, with uncertainty depending on traffic. Those estimates guide its choices. When B is estimated best, the resulting behavior is "mostly show banner B." It learned which action to take, purely from the reward of the actions it tried — which is exactly what reinforcement learning is.

**Q4 — Where does RLHF fit?** You've heard that ChatGPT and Claude are "trained with RLHF." How does that connect to the banner agent?

> **Sample answer:** RLHF (reinforcement learning from human feedback) is the same loop scaled up. The *agent* is the language model; an *action* is the response it generates; the *reward* comes from human preferences (which of two answers people prefer), distilled into a reward model; and the model updates its *policy* to produce responses that earn higher reward. The banner agent learns "which banner earns clicks"; an RLHF'd chatbot learns "which kind of response earns human approval." In both cases, the optimization target is feedback for actions the system tried.

---

## Where L11 fits — and where you go next

L11 is a bonus taster, not part of the core ten-lesson arc, so it carries no assignment. But it fills the one conceptual gap the rest of the module left open: the three big families of ML are now all on your map — **supervised** (L01–L04, L07–L10), **unsupervised** (L05), and **reinforcement** (L11). If RL caught your interest, the natural next steps are a proper contextual-bandit library for real recommenders, then the classic full-RL toolkit — Q-learning, policy gradients, and deep RL — usually learned against a simulator such as Gymnasium (formerly OpenAI Gym) before anything touches production. The durable mindset is knowing when a system must improve its choices from feedback rather than only predict a fixed target.

---

> *"We gave it actions and click feedback, and it improved its banner choices. I didn't think that was possible."* — Marcus, after the homepage relaunch.
>
> Sarah's take: *"It's the same idea as everything else — show the computer examples, let it learn. The twist is the examples are the ones it chose to try."*
