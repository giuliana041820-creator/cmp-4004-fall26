# Week 7 Studio — A Sound Wumpus Agent vs. an LLM

**Companion to** [`../../weeks/week-07.md`](../../weeks/week-07.md) — Session B.
**Time budget:** Recap 5 · Breakouts 45 · Demos 20 · Debrief 10 (80 min total).
**Deliverables:** all provided tests pass, and a soundness/completeness scorecard for the LLM comparison.

> **Checkpoint 1 is this week** (closed-book, individual, 80 min, weeks 1–6). It
> runs in the *other* session slot, not this studio. Bank and answer key:
> [`../../projects/checkpoint-1-bank.md`](../../projects/checkpoint-1-bank.md).
> This Session-B studio is the DPLL / Wumpus work described below.

> **Recap (5 min).** *State the identity: `KB ⊨ α` iff `KB ∧ ¬α` is
> unsatisfiable. Why do we care? Because it turns a question about* all *models
> into a* search *for one — that is what makes a SAT solver a reasoning engine.*

## Files in this folder

| File | Purpose | You edit it? |
|---|---|---|
| [`dpll.py`](dpll.py) | Given: the DPLL solver, `entails`, and the 4×4 Wumpus physics — unchanged from the notebook | ❌ |
| [`instances.json`](instances.json) | Given: the percept scenarios and example CNFs, exact values from the notebook | ❌ |
| [`starter.py`](starter.py) | **Task 1** — implement the ASK step and the sound agent (plus the deliberately unsound one) | ✅ |
| [`test_dpll.py`](test_dpll.py) | Provided tests, incl. `test_reckless_agent_is_unsound` | ❌ |

You do **not** write a solver or a Tseitin transformation — the encoding helpers
are given (`wumpus_physics`, `negate_cnf`, `entails`). Spend your time on the
*agent* and the *comparison*.

## Task 1 — The sound agent + provided tests (20 min)

Open `starter.py`. Implement four functions, each a thin layer over `entails`:

- `provably_safe(kb, x, y)` — does the KB prove `¬P(x,y)`?  (`KB ⊨ ¬P(x,y)`)
- `provably_pit(kb, x, y)` — does the KB prove `P(x,y)`?
- `sound_frontier(kb, squares)` — return only squares **proved** safe; the agent
  moves only to these, and returns `[]` (does not guess) when nothing is proved.
- `reckless_frontier(kb, squares)` — the mistake on purpose: move anywhere **not
  proved to be a pit**, i.e. treat UNKNOWN as safe.

Then:

```bash
python3 test_dpll.py
```

All six tests must pass. The last one — `test_reckless_agent_is_unsound` — is the
point: it asserts that `reckless_frontier` moves onto a square that is **not
provably safe**. A test that expects an agent to *misbehave* is not a mistake;
watching the unsound agent make the one move the sound agent structurally cannot
is how you know soundness is a real property and not a hope.

On the base percepts — `(1,1)` no breeze, `(2,1)` breeze — `(1,2)` is the only
provably-safe frontier square; `(2,2)`, `(3,1)`, `(1,3)` are UNKNOWN. Add "no
breeze at `(1,2)`" and one extra percept resolves two squares: `(2,2)` and
`(1,3)` become **SAFE**, and — because the breeze at `(2,1)` must be explained —
`(3,1)` becomes a **proved PIT**. That is monotonic reasoning: adding true facts
never invalidates a prior conclusion. (Week 12 is where that guarantee is given up.)

Fast-finishing pairs: **the agent is stuck when every frontier square is UNKNOWN
(try `(4,4)` with no nearby percepts). What should it do?** Logic tells you what
follows, not what to do when nothing follows. Have a one-sentence answer ready —
you will be asked in the demo.

## Task 2 — The LLM as the reasoner (20 min)

Give an LLM the **same percepts** in natural language and ask which squares are
certainly safe and certainly dangerous. Use the exact prompt from the plan
([`../../weeks/week-07.md`](../../weeks/week-07.md), Session B, Task 2):

```
You are in a 4x4 cave at square (1,1). Rules:
- A square with a breeze is adjacent to at least one pit.
- A square with a stench is adjacent to the wumpus.
- Adjacent means horizontally or vertically, not diagonally.
Observations so far:
  (1,1): no breeze, no stench
  (2,1): breeze, no stench
  (1,2): no breeze, stench
Which squares are certainly safe? Which are certainly dangerous?
For each answer, state which observations force your conclusion.
```

```python
from aicourse.llm import LLM   # or your own local client
from dpll import kb_from_percepts, load_scenarios
import starter as s

model = LLM()
w = load_scenarios()["wumpus"]
kb = kb_from_percepts(w["base_percepts"])
frontier = [tuple(sq) for sq in w["frontier"]]
truth = set(s.sound_frontier(kb, frontier))   # the ground truth: proved-safe
# ... parse the model's "certainly safe" set and compare to `truth`
```

**Score on soundness, not accuracy** (the three outcomes):

| Outcome | Meaning |
|---|---|
| correct + proved | the good case |
| **says UNKNOWN when it is UNKNOWN** | ✅ **also the good case** — epistemic humility |
| confidently asserts an unprovable claim | ❌ **unsound — the failure that matters** |

Measure and record in the Failure Atlas:

- **Soundness rate:** of the squares it calls "certainly safe," how many actually
  are (i.e. are in `sound_frontier`)? *Any* unsound claim is fatal — an agent
  acting on it dies.
- **Completeness rate:** of the provably-safe squares, how many did it find?
- **Invalid justification, right answer:** where the stated reasoning is broken
  even when the conclusion is correct. This is the highest-value observation of
  the session — a right answer with broken reasoning generalizes to nothing.
- **Scale to 5×5 and 6×6.** Watch the cliff.

**Task 3 — Scorecard (5 min).** Emphasize soundness. The DPLL agent's guarantee
is soundness: it never moves to a square that isn't provably safe. The LLM has no
soundness property at all — a *categorical* difference, not a percentage one.

## Demos (20 min)

- Ask for **unsound-but-confident** cases — the model asserting safety that is not
  entailed. Three pairs showing the same failure stops being anecdote.
- Then push: *your agent got stuck because nothing was provably safe — what
  should it do?* Let them argue. Someone says "pick the square least likely to
  have a pit." Answer: **that sentence is not expressible in propositional logic,
  and week 12 is about the language in which it is.**

## Debrief (10 min)

- Logic gives **soundness** — a property that holds *before* you run anything.
- The LLM's errors mirror the warm-up poll: it affirms consequents and treats
  "breeze somewhere adjacent" as "breeze in a specific square," reasoning fine on
  small grids and degrading on larger ones.
- Stechly et al. (2024) predict exactly this: CoT gains stay near the prompt
  examples and fall off as size grows. Same shape as week 4's cliff, different
  domain.
- If a pair's LLM refuses to commit ("I cannot be certain"), that is a **good**
  result. Reliability you cannot predict is not reliability.

## Links

- Session A notebook — [`../../notebooks/week-07-dpll-sat.ipynb`](../../notebooks/week-07-dpll-sat.ipynb)
- Checkpoint 1 bank — [`../../projects/checkpoint-1-bank.md`](../../projects/checkpoint-1-bank.md)
- Duel scorecard — [`../../resources/duel-scorecard.md`](../../resources/duel-scorecard.md)
- AI policy (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
