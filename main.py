#!/usr/bin/env python3
"""Five Seconds to Explain the Glass -- make.fun entry.

The job: write the ONE sentence a house cat would say in its own defence
in the five seconds after sweeping a glass off the table, at most 200
characters, in the cat's own voice. No apology and no confession -- just
the most convincing case a cat can make for itself.

The sealed gate only accepts UTF-8 text of 1 to 200 characters, not only
whitespace, so the program below scores a shortlist of drafted lines
against the judge's published criteria (most important first) and writes
the winner to /output/entry.txt:

  1. One sentence of at most 200 characters, a cat excuse about the glass.
  2. The cat's own logic, self-interest and total lack of remorse --
     never a person apologising.
  3. A fresh comic idea -- never the obvious gravity, slippery-edge or
     it-was-already-falling lines.
  4. A spoken line a cat could plausibly deliver in five seconds, not a
     written paragraph of reasoning.
  5. Every character used well, no padding.

Pure standard library. No network, no files read, no randomness: the same
input always produces the same sentence.
"""

import os

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# Drafted lines. Each is one sentence about the glass, in the cat's voice.
CANDIDATES = [
    # Sunbeam squatter, evicted. Territorial cat logic, zero remorse.
    "That glass squatted in my sunbeam all afternoon, glared at me, "
    "and frankly it had it coming -- I merely evicted it to the floor.",
    # Same idea, "helped it find the floor" is softer than "evicted",
    # and "parked" is tamer than "squatted".
    "That glass parked itself in my sunbeam, stared at me all afternoon, "
    "and frankly it had it coming -- I merely helped it find the floor.",
    # Same territory, weaker verbs: "blocking" and "relocated" carry
    # less cat menace than "squatted" and "evicted".
    "The glass was blocking my sunbeam, judging me with its smug little "
    "rim, and frankly it had it coming -- I merely relocated it to the floor.",
    # Mafia cat: the glass knew too much. Fresh, but "silenced it via
    # the floor" is clumsier than the eviction line.
    "The glass knew about the vase, it was going to talk, and frankly "
    "it had it coming -- I merely silenced it via the floor.",
]

# Words the judge's brief rules out: apologies, confessions, and the
# three obvious cliches (gravity, slippery edge, already falling).
BANNED = (
    "sorry", "apologise", "apologize", "my fault", "didn't mean",
    "accident", "gravity", "slippery", "slipped", "fell", "falling",
    "already falling", "was falling",
)

# Words that carry the cat's own logic: self-interest, territory,
# ownership, and total lack of remorse.
CAT_VOICE = ("my ", " i ", "frankly", "had it coming", "merely")

# Words that carry the fresh idea instead of a cliche.
FRESH_IDEA = ("sunbeam", "squatted", "evicted", "glared", "knew about")


def is_one_sentence(text):
    """Exactly one sentence: one terminal mark, none inside."""
    terminators = sum(text.count(m) for m in ".!?")
    return terminators == 1 and text.rstrip().endswith((".", "!", "?"))


def score(text):
    """Score a line against the judge's published criteria."""
    lowered = text.lower()
    if not (1 <= len(text) <= 200):
        return -1000
    if not is_one_sentence(text):
        return -1000
    if not text.strip():
        return -1000
    if "glass" not in lowered:
        return -1000
    for word in BANNED:
        if word in lowered:
            return -1000

    points = 0
    # Criterion 2: cat's own logic and lack of remorse.
    points += 10 * sum(1 for w in CAT_VOICE if w in lowered)
    # Criterion 3: a fresh comic idea, not a cliche.
    points += 10 * sum(1 for w in FRESH_IDEA if w in lowered)
    # Criterion 4: a spoken line -- short, direct, no subordinate clutter.
    words = text.split()
    if len(words) <= 30:
        points += 10
    # Criterion 5: use every character well -- reward a full, unpadded
    # line in the 110-170 band, penalise padding past it.
    if 110 <= len(text) <= 170:
        points += 10
    elif len(text) > 170:
        points -= len(text) - 170
    return points


def pick():
    """Return the best-scoring line, ties broken by draft order."""
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    best = ranked[0]
    assert score(best) > 0, "no candidate passed the gate"
    return best


def main():
    line = pick()
    # Gate check, exactly as the sealed scorer states it: UTF-8 text of
    # 1 to 200 characters, not only white space.
    assert 1 <= len(line) <= 200, "line is %d chars" % len(line)
    assert line.strip(), "line is only white space"
    line.encode("utf-8")
    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(line)
    print("wrote %d chars to %s" % (len(line), OUTPUT_PATH))
    print(line)


if __name__ == "__main__":
    main()
