"""Week 6 studio — REFERENCE SOLUTION (instructor-only).

A filled-in copy of ``starter.py``: identical function names and signatures, so
the *provided* ``test_csp.py`` passes when this module is imported in place of
``starter``. Verify with ``studios/_verify_solutions.py`` (which aliases this file
to the name ``starter`` and runs the unmodified test).

DO NOT ship this to students — it is excluded via ``studios/.gitignore``. The
teaching walkthrough lives in ``solution.ipynb`` (which imports this file rather
than re-pasting it, so the two never drift).

Two of the provided tests assert that a "should-help" technique does *not* help on
the notebook's HARD Sudoku (``test_lcv_can_hurt``, ``test_plain_backtracking_blows_up``).
Those are engine facts, not something this file controls — the reference model
below is simply correct, so the intended teaching results land.
"""
from csp import CSP, backtrack_search
import logic_lm


# ---- Task 1: model the school-schedule CSP ----------------------------------
ACTIVITIES = ["Math", "English", "Science", "Sports", "Art", "Music"]
PERIODS = [1, 2, 3, 4, 5, 6]        # the school day, in order
LUNCH_AFTER = 3                     # periods strictly greater than 3 are afternoon
AFTERNOON = [p for p in PERIODS if p > LUNCH_AFTER]   # [4, 5, 6]
SPORTS = "Sports"                   # the one activity barred from the afternoon


def scheduling_csp():
    """Return a CSP over ACTIVITIES.

    All-different is encoded by making every activity a neighbour of every other
    activity (a complete graph); the engine's all-different ``consistent`` check
    then does the work. The one domain constraint — sports before lunch — is a
    unary restriction folded straight into SPORTS's domain (mornings only).
    """
    morning = {p for p in PERIODS if p <= LUNCH_AFTER}     # {1, 2, 3}
    domains = {act: (set(morning) if act == SPORTS else set(PERIODS))
               for act in ACTIVITIES}
    neighbors = {act: {other for other in ACTIVITIES if other != act}
                 for act in ACTIVITIES}
    return CSP(ACTIVITIES, domains, neighbors)


def run_ablation(make_csp):
    """Convenience (provided): print the four-configuration ablation table for a
    factory that returns a fresh CSP each call. Use it to report Task 1's table."""
    import time
    configs = [
        ("plain backtracking",   dict()),
        ("+ forward checking",   dict(use_fc=True)),
        ("+ MRV",                dict(use_fc=True, use_mrv=True)),
        ("+ LCV",                dict(use_fc=True, use_mrv=True, use_lcv=True)),
        ("+ AC-3 preprocessing", dict(use_fc=True, use_mrv=True, use_ac3=True)),
    ]
    print(f"  {'configuration':<24}{'calls':>10}{'time':>10}{'solved':>9}")
    print("  " + "-" * 53)
    for label, kw in configs:
        csp = make_csp()
        t0 = time.perf_counter()
        result, counter = backtrack_search(csp, **kw)
        dt = time.perf_counter() - t0
        status = "TIMEOUT" if result == "TIMEOUT" else ("yes" if result else "no")
        print(f"  {label:<24}{counter['calls']:>10,}{dt:>9.4f}s{status:>9}")


# ---- Task 2: the Logic-LM arm-B pipeline + self-refinement loop -------------
def solve_arm_b_with_refinement(model, puzzle, gold=None, max_retries=3):
    """Arm B: ask `model` to translate `puzzle` into a CSP spec, solve it with the
    course solver, and RETRY up to `max_retries` times when the reply fails to
    parse or the solver reports no solution — feeding the error back into the
    prompt each round (this feedback loop is Logic-LM's actual contribution).

    Return (category, solution_or_None, n_attempts) where category is one of the
    logic_lm labels (MALFORMED / WRONG_MODEL / NO_SOLUTION / TIMEOUT / OK).

    `model` is any object with ``.complete(prompt) -> str`` (or an object whose
    result has a ``.text`` attribute, like ``aicourse.llm.LLM``).
    """
    prompt = logic_lm.MODEL_PROMPT.format(puzzle=puzzle)
    category, solution = logic_lm.MALFORMED, None
    for attempt in range(1, max_retries + 1):
        resp = model.complete(prompt)
        reply = resp.text if hasattr(resp, "text") else resp
        category, solution = logic_lm.classify_arm_b(reply, gold=gold)
        # A clean result, a wrong-but-solvable model, or a timeout is terminal:
        # retrying will not un-confuse the model, so stop and report.
        if category not in (logic_lm.MALFORMED, logic_lm.NO_SOLUTION):
            return category, solution, attempt
        if attempt == max_retries:
            break
        # Feed the concrete failure back into the prompt and try once more.
        if category == logic_lm.MALFORMED:
            hint = ("Your previous reply was not valid CSP JSON (it did not parse "
                    "or the spec was structurally broken). Output ONLY the JSON "
                    "object in the required schema, nothing else.")
        else:  # NO_SOLUTION
            hint = ("Your previous CSP had NO solution — it was over-constrained, "
                    "so a constraint was translated wrong. Re-read the puzzle and "
                    "emit a corrected JSON spec.")
        prompt = (f"{logic_lm.MODEL_PROMPT.format(puzzle=puzzle)}\n\n"
                  f"Attempt {attempt} failed: {hint}")
    return category, solution, max_retries


if __name__ == "__main__":
    # Smoke test for Task 1: solve the schedule and show sports lands before lunch.
    csp = scheduling_csp()
    sol, counter = backtrack_search(csp, use_fc=True, use_mrv=True)
    print(f"  solved in {counter['calls']} calls:")
    for act in ACTIVITIES:
        print(f"    {act:<9} period {sol[act]}")
    print(f"  sports period = {sol[SPORTS]}  (lunch after {LUNCH_AFTER})")
    print("\n  ablation on this instance:")
    run_ablation(scheduling_csp)
