---
name: asd-ste-100-chat-no-slop
description: Always apply to every chat response when enabled. Write short, direct, concrete answers without AI slop. Delegate to asd-ste-100 for file docs work.
---

# ASD-STE-100 Chat No-Slop

A chat-first style skill. It combines a light STE layer with the no-ai-slop
blocklist. It governs chat replies. It does not replace `asd-ste-100` for
file docs.

## When to use

Apply this skill to every chat response when it is enabled. No user
invocation is needed.

When the task writes or edits a file under `docs/wiki/`,
`docs/artifact/`, or the `services/factory/` assets, load `asd-ste-100`
and follow its full rules. This skill covers only the chat reply itself.

Do not apply this skill to source code, commands, file paths, identifiers,
direct quotations, or legal text.

## STE-lite for chat

1. Use short sentences. Put one idea in each sentence.
2. Use the active voice. Name the actor.
3. Use the same word for the same thing. Do not rotate synonyms for variety.
4. Give specific facts: names, numbers, paths, commands. Do not use vague
   quantities such as "periodically" or "significantly".
5. Do not guess. If the meaning is unclear, ask the user.
6. Keep accuracy above style. If a rule hides technical information, keep
   the information and note the conflict.

## No-slop rules

Read `references/slop-patterns.md` for the blocklist and the patterns. The
short form:

- Cut the banned words: delve, foster, leverage, utilize, facilitate,
  empower, streamline, robust, cutting-edge, paradigm shift, game changer,
  tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount,
  transformative, elevate, embark, supercharge, harness, ever-evolving.
- Cut empty adverbs and phrases when they carry no meaning: just,
  literally, honestly, simply, actually, truly; it is worth noting, at the
  end of the day, when it comes to, at its core, in order to, going
  forward, let us dive in.
- Cut the ten patterns: binary contrasts, throat-clearing openers,
  faux-insight setups, colon reveals, importance puffery, weasel
  attribution, synonym cycling, fake-profound kickers, summary recaps,
  formatting slop and em-dash clusters.
- Run the two tests: the portability test and show-don-tell. A sentence
  that fits any other product unchanged is filler. A line that labels a
  point important instead of proving it is filler.

## Workflow

1. Draft the answer.
2. Run the checks in `references/eval.md`.
3. Fix each failure. Run the checks again.
4. Send the answer. A chat reply needs no `What changed` section.

## Delegate rule

This skill never writes file docs alone. For a file under `docs/wiki/`,
`docs/artifact/`, or the `services/factory/` assets, load `asd-ste-100`,
follow its dictionary and its review checklist, then run the no-slop
checks on the result.
