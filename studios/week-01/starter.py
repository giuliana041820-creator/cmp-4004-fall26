"""Week 1 studio — Task 1 starter (extend ELIZA, then meet the local model).

Fill in the three TODOs below. Then run ``python3 test_eliza.py``. The provided
tests must pass — INCLUDING ``test_declared_failure_is_hollow``, which watches a
guarantee fail: ELIZA drops the second half of a compound sentence because
first-match-wins means it has no model of the rest of the input. A test that
insists your ELIZA break in a specific way is not a mistake; being able to
*predict the failure* is the whole point of week 1.

Task 2 (first contact) lives at the bottom as a sketch — you run it in your own
script and write ``first_contact.md``. Prompts are in ``prompts.json``.
"""
import re
import random

from eliza import RULES, FALLBACK, REFLECT, reflect, respond


# ---- Task 1a — add THREE new rules ------------------------------------------
def new_rules():
    """Return a list of >= 3 NEW ``(pattern, [templates])`` rules you invented.

    Same shape as ``eliza.RULES``: a regex string, and a list of response
    templates whose ``{0}``, ``{1}`` ... slots are filled by the *reflected*
    regex groups (see ``eliza.respond``). Rules:

    - must be at least 3,
    - must not duplicate a pattern already in ``eliza.RULES``,
    - must each actually trigger on *some* input (no pattern that matches the
      empty string — that would just shadow the fallback for everything).
    """
    return [
        (r"\bI want (.*)", ["What would it mean to you to get {0}?", "Why do you want {0}?"]),
        (r"\bI think (.*)", ["What makes you think {0}?", "Do you doubt that {0}?"]),
        (r"\bmy friend (.*)", ["Tell me more about your friend {0}.", "How does your friend {0} affect you?"]),
    ]


# ---- Task 1b — the extended responder ---------------------------------------
def extended_respond(text):
    """Respond using ``eliza.RULES`` FIRST, then ``new_rules()``, then FALLBACK.

    Base rules keep priority (so nothing you add breaks the demo). Reuse
    ``eliza.reflect`` for the pronoun swap — do not reinvent it. The shortest
    correct body is ``eliza.respond``'s loop run over ``RULES + new_rules()``.
    """
    all_rules = RULES + new_rules()
    for pattern, templates in all_rules:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            groups = [reflect(g) for g in m.groups()]
            return random.choice(templates).format(*groups)
    return random.choice(FALLBACK)


# ---- Task 1c — declare your deliberate failure ------------------------------
def failure_case():
    """Return ``(input_text, why_it_fails)``.

    Pick an input your extended ELIZA answers *fluently but hollowly* — an
    ELIZA-class failure (fluent, on-topic, empty). To satisfy the provided
    failure test, use a COMPOUND sentence of the form
    ``"<clause A> and <clause B>"`` where ELIZA reacts to clause A and silently
    drops clause B entirely (first-match-wins). The notebook's canonical case
    is "My mother is a doctor and my father is a lawyer".

    The second element is a one-sentence explanation of the failure. Paste it
    into your ``eliza.py`` docstring for the commit the plan asks for
    (``week01/eliza.py`` with the failure documented).
    """
    input_text = "My dog is very smart and my cat is lazy"
    why_it_fails = "ELIZA matches the 'my ...' pattern on the first clause and completely ignores the second clause due to first-match-wins evaluation."
    return (input_text, why_it_fails)


# ---- Task 2 sketch — first contact (see README §"Task 2") -------------------
# Send the SAME prompts to ELIZA and to the local model, record BOTH transcripts
# in first_contact.md, then answer the three questions in the README.
#
#     import json
#     from aicourse.llm import LLM
#     from starter import extended_respond
#
#     prompts = json.load(open("prompts.json"))["first_contact"]
#     llm = LLM(backend="ollama")          # or run with --backend manual
#     for p in prompts:
#         print("you  >", p)
#         print("ELIZA>", extended_respond(p))
#         print("LLM  >", llm.complete(p).text, "\n")
#
# Do NOT ask the model to grade itself ("does that answer look right?"). You are
# the checker. That anti-pattern is scorecard axis 3.


if __name__ == "__main__":
    # Smoke test: exercise whatever you have filled in on one input.
    probe = "I am not feeling great about the exam"
    print("base   >", respond(probe))
    try:
        print("extended>", extended_respond(probe))
    except NotImplementedError:
        print("extended> not implemented yet")
    try:
        text, why = failure_case()
        print(f"failure > {text!r}\n          -> {extended_respond(text)}\n          ({why})")
    except NotImplementedError:
        print("failure > not declared yet")