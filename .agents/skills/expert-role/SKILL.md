---
name: expert-role
description: Set up an implementation expert role for one component of the project. The expert owns phase 4 of the artifact-driven documentation model for that component. Use for "add an expert", "set up an implementation expert", or "no expert covers this component".
---

# Expert Role

An implementation expert is an agent role that knows one component of the project. The expert
owns phase 4 of the artifact-driven documentation model for that component. This skill tells
you how to write the body of the role and how to declare the role. It tells you how to check
the rendered role file of each harness in use.

## When to use

A project has one implementation expert for each component. When `docs/domain/` exists, the
project uses domain-driven design and has one implementation expert for each bounded context.
This is the same rule: one bounded context is one component.

Do not add a second expert for a component that has one. To find the experts, read
`role.builder` in `devenv.local.nix` and the folders in `utils/agent/role/`.

## Procedure

1. Find the component. Read the page in `docs/wiki/repo-arch/`. When `docs/domain/` exists,
   read the `**Component:**` line of `docs/domain/context-<name>/README.md`. Make sure that no
   expert covers the component.
2. Write the body at `utils/agent/role/<name>/ROLE.md` from `references/role-template.md`.
   Write the body only. Do not write a frontmatter or a header. The shell adds the header.
3. Declare the role in `devenv.local.nix` as `references/role-builder.md` shows.
4. Enter the shell again. The shell renders the files when it starts. Check the rendered role
   file of each harness in `factory.domain.agent.harness.uses`:
   - `.claude/agents/<name>.md` for `claude`.
   - `.opencode/agents/<name>.md` for `opencode`.
   - `.codex/agents/<name>.toml` and one `agents.<name>` entry in `.codex/config.toml` for
     `codex`.

   Each rendered file has the header that the shell adds and the body. A harness that is not
   in the list has no rendered file. A rendered file is not a source. To change it, change the
   body or the declaration, then enter the shell again.
5. Report the files that you wrote and the result of the check.

## Rules

- The expert owns phase 4 for its component.
- The expert gives `spec-<name>.md` and `task-<name>.md` to the solution expert in phases 2
  and 3. The expert does not write `specifications/README.md` or `tasks/README.md`.
- The expert does not write requirements.
- The description of the role says what the expert does and ends with a sentence that starts
  with `Use for`.
- Write in ASD-STE-100 Simplified Technical English. Use the `asd-ste-100` skill.
- Do not repeat the rules of `AGENTS.md` in the body.
- Do not put a status field or a phase-tracking field in any file.

## References

- [Role body template](references/role-template.md): the seven parts of the body and one
  filled example.
- [Role declaration](references/role-builder.md): the fields of the declaration and the
  rendered file of each harness.
