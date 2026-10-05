"""Week 7 studio — Task 1 starter (a sound Wumpus agent).

Fill in the functions below, then run ``python3 test_dpll.py``. All required
tests must pass, INCLUDING ``test_reckless_agent_is_unsound`` — which asserts
that an agent WITHOUT the entailment check moves to a square that is not
provably safe. A guarantee you cannot watch fail is not a guarantee you
understood: the sound agent structurally cannot make that error, and the test
proves the reckless one does.

The engine (DPLL, ``entails``, the Wumpus physics) is provided in ``dpll.py``.
You are writing the *agent* — the ASK step of perceive → TELL → ASK → act — on
top of it. Everything you need is ``entails`` and the ``Pv`` proposition helper.
"""
from dpll import Pv, entails


# ---- Task 1: the ASK step ---------------------------------------------------
# Each of these asks the KB ONE question via the central identity.

def provably_safe(kb, x, y) -> bool:
    """Does the KB PROVE there is no pit at (x, y)?  i.e.  KB ⊨ ¬P(x,y).

    Use ``entails(kb, [frozenset({-Pv(x, y)})])``. Note the sign: ¬P(x,y) is the
    literal ``-Pv(x, y)`` wrapped as a one-clause CNF.
    """
    # TODO: return whether KB entails ¬P(x,y)
    raise NotImplementedError


def provably_pit(kb, x, y) -> bool:
    """Does the KB PROVE there is a pit at (x, y)?  i.e.  KB ⊨ P(x,y)."""
    # TODO: return whether KB entails P(x,y)
    raise NotImplementedError


# ---- Task 1: the act step, two ways -----------------------------------------

def sound_frontier(kb, squares) -> list:
    """The SOUND agent. Return only the squares that are PROVED safe.

    This is the whole point of the week: the agent moves only where it can prove
    there is no pit. If nothing is proved safe it returns [] — and an honest
    agent then stops or takes a *declared* risk. It never treats UNKNOWN as safe.
    """
    # TODO: return [sq for sq in squares if provably_safe(kb, *sq)]
    raise NotImplementedError


def reckless_frontier(kb, squares) -> list:
    """The UNSOUND agent — the mistake, implemented on purpose so we can watch it.

    It skips the entailment check and moves anywhere NOT proved to be a pit,
    i.e. it treats UNKNOWN as safe. This is exactly the error the LLM makes in
    Task 2: "probably safe" is not "provably safe." An agent that acts on it dies
    the first time UNKNOWN hides a pit.
    """
    # TODO: return [sq for sq in squares if not provably_pit(kb, *sq)]
    raise NotImplementedError


# ---- Task 2 sketch (the LLM as the reasoner) --------------------------------
# See README.md §"Task 2". Give an LLM the SAME percepts in natural language and
# score its "certainly safe" claims for SOUNDNESS against ``sound_frontier``:
# any square it calls safe that is not in sound_frontier(kb, frontier) is an
# unsound claim — the failure that matters. Record every one in the Failure Atlas.


if __name__ == "__main__":
    from dpll import kb_from_percepts, classify, load_scenarios
    sc = load_scenarios()["wumpus"]
    base = sc["base_percepts"]
    frontier = [tuple(s) for s in sc["frontier"]]
    kb = kb_from_percepts(base)

    print("Percepts: (1,1) no breeze, (2,1) breeze.\n")
    for (x, y) in frontier:
        print(f"  ({x},{y}): {classify(kb, x, y)}")

    try:
        print("\nsound_frontier :", sound_frontier(kb, frontier))
        print("reckless_frontier:", reckless_frontier(kb, frontier))
    except NotImplementedError:
        print("\n  (implement sound_frontier / reckless_frontier to compare)")
