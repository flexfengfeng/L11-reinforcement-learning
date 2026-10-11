# Lesson — L11 Reinforcement Learning (bonus intro)

> **A bonus chapter of the NorthStar Retail story — added by learner request.** *Sarah Chen · Customer Experience Analyst · NorthStar Retail · a few months after the L10 launch.*
> Sarah's churn model and shopping assistant are live. Marcus's new ask: *"Make the homepage recommend the right product banner to each visitor — and get better on its own as real shoppers click."* There's no labelled "correct banner" list. The system has to learn by trying.
> That last sentence is the whole reason this is a *reinforcement learning* problem, not a supervised one.

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
| **Part 5 — Go deeper** *(optional)* | same notebook — contextual bandit & the Q-table |

The notebook is the spine. Run it top to bottom. Come back here for the consolidated takeaways and review questions.

---

## Overview

For ten lessons, every model Sarah built learned from an **answer key** — a column of correct labels, or a true value to forecast. L11 removes the answer key. NorthStar's homepage can show one of three banners — *A · New arrivals*, *B · 50% off*, *C · Trending now* — and the only feedback is whether each visitor clicks. Nobody knows in advance which banner is best; the system must **discover it by trying banners and watching clicks.**

The lesson builds that system twice. First a **random baseline** that shows banners with no strategy — the number any real method has to beat. Then an **ε-greedy agent** that keeps a running click-rate scoreboard, mostly shows the best banner so far, but explores a random one a small fraction of the time. Watching its click rate climb toward the best banner's true rate — with no labelled training set — *is* reinforcement learning happening. Part 3 then names every moving piece, Part 4 lets you turn the one dial that matters, and an optional Part 5 adds visitor **context** to reach a contextual bandit and the Q-table. The whole point is one mindset shift: supervised learning answers *"what is this?"* from labelled examples; reinforcement learning answers *"what should I do?"* from the reward of what it tried.

---

## Key takeaways

1. **RL learns without an answer key.** There are no labels — only a reward signal (here, click = 1, no click = 0) for actions the agent actually took. This is the single line that separates RL from everything in L01–L10.
2. **Every RL system is one loop.** An agent observes its situation, takes an action, receives a reward, and updates how it will act next time — repeated thousands of times. Games, robots, self-driving cars, and the fine-tuning of modern chatbots all run this same loop.
3. **Six words cover the vocabulary.** *Agent* (the learner), *environment* (the world it acts on), *action* (what it does), *reward* (the feedback), *policy* (its strategy for choosing), and *value* (its estimate of how good a choice is). Each maps directly to a line in the banner code.
4. **Explore vs. exploit is the defining tension.** *Exploit* = use what you know to get reward now; *explore* = give up reward now to learn something that pays off later. You can't do both at once, and getting the balance wrong is costly either way.
5. **`epsilon` is the dial for that trade-off.** `epsilon = 0.1` means explore 10% of the time, exploit the rest. Too low (`0`) and the agent usually locks onto whichever banner got lucky early and never discovers the better one. Too high (`1.0`) and it's just the random baseline. A small value (`0.05`–`0.1`) usually wins.
6. **The agent learns a policy, not "the rules."** It never learns the true click rates as facts; it learns *what to do* — which banner to show — from the reward each click gave. That estimated click-rate scoreboard is its value estimate; "mostly show the best" is its policy.
7. **Context turns a bandit into a smarter recommender.** A first-time visitor and a loyal member respond to different banners. A **contextual bandit** keeps a **Q-table** — a score per action *for each kind of situation* — and chooses based on what it knows before acting. That's a half-step toward full RL.
8. **Full RL adds sequences.** A bandit's choices are independent; full reinforcement learning is for when your action *changes the world's state*, so you must weigh long-term reward, not just the next click. Q-learning over states, policy gradients, and deep RL are this same loop scaled up — and it's how chatbots are tuned with RLHF.

---

## Is this an RL problem? — a quick checklist

Before reaching for RL on a real problem, check all three. Miss any one and a simpler method (or supervised learning) is usually the better tool:

1. **Is there no answer key?** If you already have labelled correct answers, use supervised learning — it's simpler and stronger. RL earns its keep only when the correct action isn't known in advance and must be discovered.
2. **Do your actions produce feedback you can measure?** RL needs a reward signal — clicks, score, revenue, a thumbs-up. No measurable reward, no learning.
3. **Can you afford to experiment?** RL learns by trying things, and some of those trials will be worse than your current best. If every wrong action is unacceptable (safety-critical, one-shot decisions), RL in production is risky without a simulator or strict guardrails.

The banner problem passes all three: no correct-banner label, a clean reward (clicks), and a low cost to occasionally showing a weaker banner. That's why it's a textbook RL starter.

---

## Check your understanding

Work through these after the notebook. Attempt each on your own first.

**Q1 — Why isn't this supervised learning?** Marcus says: "We have thousands of past visits and whether each clicked — that's labelled data. Why not just train a classifier?" What's the gap?

> **Sample answer:** A classifier trained on past visits could predict "will this visitor click *the banner we happened to show them*?" — but it only ever saw the banner that was actually shown, never the clicks the *other* banners would have earned. There's no label for "the best banner for this visitor," because that counterfactual was never observed. RL closes the gap by *acting*: it deliberately shows different banners, collects the reward each earns, and improves its choice from that. The learning comes from the agent's own actions, not a fixed labelled set.

**Q2 — The `epsilon = 0` trap.** What can go wrong if the agent never explores, and why is a little exploration "insurance"?

> **Sample answer:** With `epsilon = 0` the agent shows each banner once, then always shows whichever banner currently looks best. If a genuinely weaker banner gets a lucky early click, its running average jumps to the top, the agent commits to it, and — because it never tries the others again — it never collects the evidence that would correct the mistake. It gets stuck. A small exploration rate guarantees every banner keeps getting *some* traffic, so a truly better option eventually reveals itself. That ongoing trickle of trials is the insurance premium against bad early luck.

**Q3 — What did the agent actually learn?** It was never told the true click rates (5% / 11% / 8%). So what did it learn?

> **Sample answer:** It learned a **policy** — a rule for what to do — not the rules of the world. Its scoreboard of estimated click rates (its *value* estimates) ended up close to the true 5/11/8%, but those estimates were a means, not the goal. What it produced was behaviour: "mostly show banner B." It learned which action to take, purely from the reward of the actions it tried — which is exactly what reinforcement learning is.

**Q4 — Where does RLHF fit?** You've heard that ChatGPT and Claude are "trained with RLHF." How does that connect to the banner agent?

> **Sample answer:** RLHF (reinforcement learning from human feedback) is the same loop scaled up. The *agent* is the language model; an *action* is the response it generates; the *reward* comes from human preferences (which of two answers people prefer), distilled into a reward model; and the model updates its *policy* to produce responses that earn higher reward. The banner agent learns "which banner earns clicks"; an RLHF'd chatbot learns "which kind of response earns human approval." No answer key in either case — just reward for what was tried.

---

## Where L11 fits — and where you go next

L11 is a bonus taster, not part of the core ten-lesson arc, so it carries no assignment. But it fills the one conceptual gap the rest of the module left open: the three big families of ML are now all on your map — **supervised** (L01–L04, L07–L10), **unsupervised** (L05), and **reinforcement** (L11). If RL caught your interest, the natural next steps are a proper contextual-bandit library for real recommenders, then the classic full-RL toolkit — Q-learning, policy gradients, and deep RL — usually learned against a simulator such as Gymnasium (formerly OpenAI Gym) before anything touches production. But the mindset is the durable part: when there's no answer key, only the reward of what you tried, you now know there's a whole branch of ML built for exactly that.

---

> *"You spent ten weeks teaching models from answer keys. This one had none — and it still figured out which banner to show. I didn't think that was possible."* — Marcus, after the homepage relaunch.
>
> Sarah's take: *"It's the same idea as everything else — show the computer examples, let it learn. The twist is the examples are the ones it chose to try."*
