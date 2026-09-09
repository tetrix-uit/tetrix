# ASD-STE-100 Writing Rules

The specification has nine sections of rules. This file gives the rules and a
short example for each. Use the rule numbers when you comment on a document.

## Section 1: Words

**1.1 Use approved words only.** Use a word only if the dictionary approves it,
or if it is a technical name or a technical verb.

**1.2 Use the approved part of speech.** A word that the dictionary approves as
a verb must not be used as a noun.

- Not approved: "Do a test of the pump."
- Approved: "Test the pump."

**1.3 Keep to the approved meaning.** "Follow" means "come after", not "obey".

- Not approved: "Follow the safety instructions."
- Approved: "Obey the safety instructions."

**1.4 Technical names are permitted.** A technical name identifies a part, a
tool, a material, a place, or a document. Examples: "database", "load
balancer", "Dockerfile".

**1.5 Use one technical name for one thing.** Do not change between "container"
and "pod" for the same object.

**1.6 Use one technical verb for one action.** Do not change between "deploy"
and "roll out" for the same action.

**1.7 Do not use a technical name as a verb.** Write "Send a request with the
HTTP client", not "HTTP the endpoint".

**1.8 Use approved words to make new technical verbs only when no approved verb
exists.** Record the new verb in the project glossary.

**1.9 Do not use slang, jargon, or idioms.** "The build is broken" is clear.
"The build went sideways" is not.

**1.10 Do not use a word that has more than one meaning in the context.**

**1.11 Use short and familiar words.** Write "use", not "utilize". Write
"start", not "initiate".

**1.12 Do not use abbreviations that the document does not define.** Give the
full term at first use, then the abbreviation in parentheses.

**1.13 Do not use a contraction.** Write "do not", not "don't".

## Section 2: Noun phrases

**2.1 Do not make a noun cluster of more than three nouns.**

- Not approved: "runtime configuration validation error message"
- Approved: "error message for a validation error in the runtime
  configuration"

**2.2 Give the definition of a permitted cluster of three nouns at first use,
if the meaning is not clear.**

**2.3 Use an article or a demonstrative before a noun.** Write "the
configuration file", not "configuration file".

**2.4 Use a hyphen in a compound modifier.** Write "read-only file system".

## Section 3: Verbs

**3.1 Use only an approved form of a verb.** The approved forms are the
infinitive, the imperative, the simple past, the past participle used as an
adjective, and the -ing form used in a technical name.

**3.2 Use these tenses only:** the simple present, the simple past, and the
simple future.

**3.3 Do not use a complex tense.**

- Not approved: "The service has been restarting since 10:00."
- Approved: "The service started again at 10:00. It is not stable."

**3.4 Use the active voice in a description as much as possible.**

**3.5 Do not use the passive voice in a procedure.**

- Not approved: "The container must be stopped."
- Approved: "Stop the container."

**3.6 Do not change a verb into a noun.**

- Not approved: "Perform a validation of the schema."
- Approved: "Validate the schema."

**3.7 Use the -ing form only in a technical name.** "Load balancing" as a name
is permitted. "The server is processing the queue" is not.

## Section 4: Sentences

**4.1 Keep to the standard word order:** subject, verb, object.

**4.2 Be as specific as possible.**

- Not approved: "Wait for a short time."
- Approved: "Wait for 30 seconds."

**4.3 Do not delete a word to make a sentence shorter.** Keep articles,
relative pronouns, and the word "that".

**4.4 Use a connecting word to show the relation between two sentences.**
Examples: "then", "but", "because", "if".

**4.5 Give one item of information in one sentence.**

**4.6 Keep to one topic in one sentence.**

## Section 5: Procedures

**5.1 Write an instruction as a command.** Start with the verb.

**5.2 Write one instruction in one sentence.**

**5.3 Use a vertical list when a step has more than one action.**

**5.4 Use a horizontal list only for a short set of items.**

**5.5 Give the condition before the instruction.**

- Approved: "If the test fails, examine the log file."

**5.6 Use the maximum of 20 words in a procedural sentence.**

**5.7 Use the maximum of 6 sentences in a procedural paragraph.**

## Section 6: Descriptive writing

**6.1 Use the maximum of 25 words in a descriptive sentence.**

**6.2 Use the maximum of 6 sentences in a descriptive paragraph.**

**6.3 Keep to one topic in one paragraph.** Start the paragraph with the topic
sentence.

**6.4 Vary the length of the sentences and the paragraphs, so that the text is
easy to read.**

## Section 7: Safety instructions

**7.1 Put a warning or a caution before the step that it applies to.** A reader
who reads the step first can be injured before the warning is read.

**7.2 Start a safety instruction with a command, or with the condition.**

- Approved: "Do not run this command on a production database."
- Approved: "If the disk is full, the service stops. Delete old log files
  first."

**7.3 Write the condition first, then the instruction, if a condition applies.**

**7.4 Give the reason only if the reason helps the reader to obey the
instruction.**

## Section 8: Punctuation and numbers

**8.1 Use punctuation to make the structure of a sentence clear.**

**8.2 Use a hyphen to connect the parts of a compound modifier.**

**8.3 Do not use a slash to mean "and" or "or".** Write "start or stop", not
"start/stop".

**8.4 Do not use a parenthesis to add information to a sentence.** Write a new
sentence.

**8.5 Write a number as a numeral if the number is a measurement, a quantity,
or a step number.**

**8.6 Use a decimal point, not a comma, in a decimal number.**

**8.7 Use the international system of units, and give the other unit in
parentheses if the reader needs it.**

**8.8 Do not start a sentence with a numeral.** Rewrite the sentence.

## Section 9: Writing practices

**9.1 Use a note to give information, not an instruction.**

**9.2 Do not put a warning, a caution, or an instruction in a note.**

**9.3 Use a key word at the start of a paragraph to help the reader find the
information.**

**9.4 Keep the same layout and the same terminology in the full document.**
