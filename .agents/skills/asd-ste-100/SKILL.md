---
name: asd-ste-100
description: Write and edit technical documentation in ASD-STE-100 Simplified Technical English. Use for README files, wiki pages, procedures, work instructions, safety warnings, API and CLI reference text, release notes, and error messages, or when the user asks for STE, Simplified Technical English, controlled language, plain technical English, or asks to simplify, rewrite, or review documentation for clarity.
---

# ASD-STE-100 Simplified Technical English

ASD-STE-100 is a controlled language specification for technical documentation.
It has two parts:

1. **Writing rules** — 53 rules about grammar, style, and structure.
2. **Dictionary** — approved words, each with one approved meaning and one
   approved part of speech.

The goal is documentation that a reader with limited English can understand
correctly on the first read.

## When to apply this skill

Apply the rules to technical content: procedures, descriptions, safety
instructions, reference documentation, README files, commit message bodies,
error messages, and user interface text.

Do not apply the rules to these items:

- Source code, identifiers, and code comments that describe algorithms.
- Direct quotations from other documents.
- Legal text, licenses, and marketing copy.
- Conversation with the user, unless the user asks for it.

## The core rules

Follow these ten rules first. They give most of the benefit.

1. **Use approved words only.** Each word has one meaning and one part of
   speech. Read `references/dictionary.md` for the approved words and for
   replacements for frequent not-approved words.
2. **Use short sentences.** Maximum 20 words in a procedural sentence.
   Maximum 25 words in a descriptive sentence.
3. **Write one instruction per sentence.** If a step has more than one action,
   make a vertical list.
4. **Use the active voice.** The passive voice is not permitted in procedures.
5. **Use the imperative for instructions.** Start with the verb: "Remove the
   cover."
6. **Use simple tenses only.** Simple present, simple past, and simple future.
   Do not use perfect or progressive tenses.
7. **Do not make noun clusters of more than three nouns.**
8. **Keep articles.** Do not delete "a", "an", or "the" to make text shorter.
9. **Use the same word for the same thing every time.** Do not use synonyms
   for variety.
10. **Put the safety instruction before the step that it applies to.**

## Reference files

Read the reference file that matches the task. Do not read all of them.

| File | Read it when |
| --- | --- |
| `references/writing-rules.md` | You need the full rule set, or you need the exact rule number for a review comment. |
| `references/dictionary.md` | You need approved words, approved parts of speech, or a replacement for a not-approved word. |
| `references/examples.md` | You need before-and-after rewrites of common problems. |
| `references/review-checklist.md` | You review or audit an existing document. |

## Workflow: write new content

1. Decide the content type: procedure, description, or safety instruction.
   The rules are different for each.
2. Write the content with the core rules above.
3. Check every word against `references/dictionary.md`. Replace each
   not-approved word, or keep it if it is a technical name or a technical verb
   that the project already uses.
4. Run the checks in `references/review-checklist.md`.

## Workflow: rewrite existing content

1. Read the source content. Record the technical names and the technical verbs
   that it uses. Keep them.
2. Split each long sentence into sentences of one topic.
3. Change each passive sentence to the active voice.
4. Replace each not-approved word.
5. Show the user the changed text. If the meaning of a sentence is not clear,
   tell the user. Do not guess the meaning.

## Important constraints

- **Do not remove technical information to satisfy a rule.** If a rule and the
  accuracy of the content are in conflict, keep the accuracy. Then tell the
  user about the conflict.
- **Keep technical names and technical verbs.** A technical name is an official
  name for a part, a tool, or a concept, such as `kubelet` or "pull request".
  The dictionary does not list them, but they are permitted.
- **Do not change code, commands, file paths, or identifiers** to satisfy a
  language rule. They are data, not prose.
