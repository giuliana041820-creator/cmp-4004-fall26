"""Provided tests for the week-7 studio.

Run: ``python3 test_dpll.py``. Passes ⇒ your Task 1 agent is defensible and you
are ready for the LLM comparison in Task 2. Prints one line per test.

The *failure* test — ``test_reckless_agent_is_unsound`` — asserts that the agent
built WITHOUT the entailment check (``reckless_frontier``) steps onto a square
that is not provably safe. That is the point of the exercise: a sound agent
structurally cannot make that move; watch the unsound one make it.
"""
import sys

from dpll import Pv, entails, kb_from_percepts, classify, load_scenarios
import starter as s

SC = load_scenarios()
WUMPUS = SC["wumpus"]
BASE = WUMPUS["base_percepts"]
EXTRA = WUMPUS["extra_percept"]
FRONTIER = [tuple(sq) for sq in WUMPUS["frontier"]]


# ---- the engine: the central identity ---------------------------------------

def test_modus_ponens():
    # {P -> Q, P} entails Q, and does NOT entail ¬Q.
    P, Q = 1, 2
    kb = [frozenset({-P, Q}), frozenset({P})]
    assert entails(kb, [frozenset({Q})]), "modus ponens should entail Q"
    assert not entails(kb, [frozenset({-Q})]), "must not entail ¬Q"
    print("  ok  modus ponens: {P→Q, P} ⊨ Q")


def test_affirming_consequent_is_invalid():
    # {P -> Q, Q} does NOT entail P — the warm-up-poll fallacy; the solver agrees.
    P, Q = 1, 2
    kb = [frozenset({-P, Q}), frozenset({Q})]
    assert not entails(kb, [frozenset({P})]), (
        "{P→Q, Q} ⊨ P would be affirming the consequent — it is INVALID"
    )
    print("  ok  affirming the consequent {P→Q, Q} ⊭ P (invalid, as it should be)")


# ---- the Wumpus KB: proofs, and monotonic growth ----------------------------

def test_wumpus_base_classification():
    # From the base percepts: (1,2) is proved safe; the rest are UNKNOWN.
    kb = kb_from_percepts(BASE)
    expected = WUMPUS["expected_base"]
    for (x, y) in FRONTIER:
        got = classify(kb, x, y)
        assert got == expected[f"{x},{y}"], (
            f"({x},{y}): expected {expected[f'{x},{y}']!r}, got {got!r}"
        )
    print("  ok  base percepts: (1,2) SAFE, (2,2)/(3,1)/(1,3) UNKNOWN")


def test_extra_percept_resolves_two_squares():
    # Adding 'no breeze at (1,2)' proves (2,2) & (1,3) safe and (3,1) a PIT.
    kb2 = kb_from_percepts(BASE + EXTRA)
    expected = WUMPUS["expected_after_extra"]
    for key, want in expected.items():
        x, y = (int(t) for t in key.split(","))
        got = classify(kb2, x, y)
        assert got == want, f"({key}): expected {want!r}, got {got!r}"
    print("  ok  one extra percept resolves (2,2) SAFE, (1,3) SAFE, (3,1) PIT "
          "(monotonic reasoning)")


# ---- the sound agent ---------------------------------------------------------

def test_sound_agent_only_moves_to_proved_safe():
    # Every square the sound agent moves to must independently be provably safe,
    # and on the base percepts that is exactly {(1,2)}.
    kb = kb_from_percepts(BASE)
    moves = s.sound_frontier(kb, FRONTIER)
    for (x, y) in moves:
        assert entails(kb, [frozenset({-Pv(x, y)})]), (
            f"sound agent moved to ({x},{y}) which is NOT provably safe"
        )
    assert set(moves) == {(1, 2)}, (
        f"sound agent should move only to (1,2) here, got {sorted(moves)}"
    )
    print("  ok  sound agent moves only to proved-safe squares: [(1, 2)]")


def test_reckless_agent_is_unsound():
    """The point of the week. The no-entailment-check agent moves to a square
    that is NOT provably safe — the error the sound agent structurally cannot
    make."""
    kb = kb_from_percepts(BASE)
    reckless = set(s.reckless_frontier(kb, FRONTIER))
    sound = set(s.sound_frontier(kb, FRONTIER))
    unsound_moves = [(x, y) for (x, y) in reckless
                     if not entails(kb, [frozenset({-Pv(x, y)})])]
    assert unsound_moves, (
        "reckless_frontier proved safe on every square it chose — it is not "
        "actually skipping the entailment check. It must treat UNKNOWN as safe."
    )
    assert reckless > sound, (
        "reckless agent should move to MORE squares than the sound one "
        f"(it treats UNKNOWN as safe): reckless={sorted(reckless)} "
        f"sound={sorted(sound)}"
    )
    print(f"  ok  reckless agent made {len(unsound_moves)} UNSOUND move(s) "
          f"{sorted(unsound_moves)} — proved-safe check omitted (the lesson)")


TESTS = [
    test_modus_ponens,
    test_affirming_consequent_is_invalid,
    test_wumpus_base_classification,
    test_extra_percept_resolves_two_squares,
    test_sound_agent_only_moves_to_proved_safe,
    test_reckless_agent_is_unsound,
]


def main():
    failed = 0
    for t in TESTS:
        try:
            t()
        except NotImplementedError:
            print(f"  --  {t.__name__}: agent not implemented yet")
            failed += 1
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


if __name__ == "__main__":
    main()
