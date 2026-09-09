# ASD-STE-100 Dictionary Guidance

The full dictionary of ASD-STE-100 has approximately 900 approved words. ASD
holds the copyright, and the official dictionary is at
`https://asd-ste100.org`. This file gives the principles and the frequent
replacements. Use the official dictionary when a word is not in this file.

## The three principles

**1. One word, one meaning.** Each approved word has one approved meaning.
"Close" means "to shut". It does not mean "near".

**2. One word, one part of speech.** If the dictionary approves "test" as a
verb, do not write "a test". Write "a check" or rewrite the sentence.

**3. A not-approved word has an approved alternative.** The dictionary gives
the alternative. If no alternative exists, the word is a technical name and it
is permitted.

## Words that are always permitted

The dictionary does not list these words, but you can use them:

- **Technical names.** Names of parts, tools, materials, systems, standards,
  and documents. Examples: "Kubernetes", "pull request", "TLS certificate".
- **Technical verbs.** Verbs for an action in the technical domain, when no
  approved verb has the same meaning. Examples: "to solder", "to compile".
- **Numbers, units, and identifiers.**
- **Official names of organizations, people, and places.**
- **Words in code, in a command, in a file path, and in a quoted error
  message.**

Record each new technical name and technical verb in the project glossary.
Then use it consistently.

## Frequent replacements

### Verbs

| Not approved | Approved |
| --- | --- |
| accomplish, execute, perform | do |
| utilize, employ | use |
| initiate, commence | start |
| terminate, cease | stop |
| ascertain, determine | find, calculate |
| require | need |
| assist | help |
| attempt | try |
| obtain, acquire | get |
| modify, alter | change |
| verify, validate (as prose) | check, make sure |
| indicate | show |
| permit | let |
| retain | keep |
| eliminate, discard | remove, delete |
| prohibit | do not let |
| comprise, constitute | have, include |
| facilitate | help, make easy |
| implement | do, make, install |
| leverage | use |
| ensure | make sure |

### Nouns

| Not approved | Approved |
| --- | --- |
| utilization | use |
| commencement | start |
| termination | end |
| assistance | help |
| requirement | what you need |
| capability | ability, function |
| functionality | function |
| methodology | method |
| approximately | about |
| prior to | before |
| subsequent to | after |

### Adjectives and adverbs

| Not approved | Approved |
| --- | --- |
| adequate, sufficient | enough |
| additional | more |
| initial | first |
| final | last |
| numerous, multiple | many |
| optimal | best |
| rapid, expeditious | fast, quick |
| approximately | about |
| currently, presently | now |
| immediately | now, at once |
| frequently | often |
| typically, generally | usually |

### Connecting words and phrases

| Not approved | Approved |
| --- | --- |
| in order to | to |
| due to the fact that | because |
| in the event that | if |
| with regard to, in respect of | about |
| in accordance with | as given in, as specified in |
| in the vicinity of | near |
| at this point in time | now |
| for the purpose of | to, for |
| notwithstanding | but, although |

## Words with a restricted meaning

These words are approved, but only in one meaning. Take care.

| Word | Approved meaning | Do not use for |
| --- | --- | --- |
| follow | to come after | to obey |
| clear | to remove an obstruction | easy to understand |
| close | to shut | near |
| free | to release | at no cost |
| right | the opposite of left | correct |
| fit | to install a part | the correct size |
| light | not heavy | a lamp, or a color |
| like | the same as | to want |
| may | permission | possibility (use "can" or "it is possible") |
| should | a recommendation | probability |

## Approved auxiliary verbs

Use these verbs only in these meanings:

- **can** — is able to, or is possible.
- **must** — an obligation. Use it for a rule that the reader must obey.
- **must not** — a prohibition.
- **do not** — a prohibition in an instruction.
- **will** — the simple future.
- **may** — has permission to.
- **should** — a recommendation, not an obligation.

## How to handle a word that is not in the dictionary

Answer the questions in this order:

1. Is it a technical name or a technical verb in this project? If yes, keep it
   and record it in the glossary.
2. Does an approved word have the same meaning? If yes, use the approved word.
3. Can you rewrite the sentence and remove the word? If yes, rewrite it.
4. Is the word necessary for the accuracy of the content? If yes, keep the word
   and tell the user.
