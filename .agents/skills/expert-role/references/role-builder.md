# Role Declaration

A role is one body and one declaration. The body is the file `utils/agent/role/<name>/ROLE.md`.
The declaration is one entry of the option `factory.domain.agent.role.builder.<name>` in
`devenv.local.nix`. The shell reads the declaration when it starts. It renders one role file for
each harness in use.

### Fields

The fields of `factory.domain.agent.role.builder.<name>`:

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `enable` | bool | `true` | Whether to generate this role. |
| `name` | str | The attribute name | The file name of the role in each harness. |
| `description` | str | Required | Tells the harness when to use the role. |
| `instruction` | str | Required | The markdown body of the role file. |
| `harness.claude` | attrs | `{ }` | Extra frontmatter fields of `.claude/agents/<name>.md`. |
| `harness.codex` | attrs | `{ }` | Extra keys of `.codex/agents/<name>.toml`. |
| `harness.opencode` | attrs | `{ }` | Extra frontmatter fields of `.opencode/agents/<name>.md`. |

### Rendered files

The harness list is `factory.domain.agent.harness.uses`. It is a list with values from
`claude`, `codex`, and `opencode`. A harness that is not in the list renders no file. Each
rendered file has the copy mode `copy`: the shell overwrites it on each entry.

| Harness | Rendered file | Content |
| --- | --- | --- |
| `claude` | `.claude/agents/<name>.md` | YAML frontmatter with `name` and `description` plus `harness.claude`, then the body. |
| `opencode` | `.opencode/agents/<name>.md` | YAML frontmatter with `description` plus `harness.opencode`, then the body. |
| `codex` | `.codex/agents/<name>.toml` | The keys `name`, `description`, and `developer_instructions` (the body) plus `harness.codex`. |
| `codex` | `.codex/config.toml` | One entry `agents.<name>` with `description` and `config_file = "agents/<name>.toml"`. |

### Declaration

One complete declaration for `devenv.local.nix`:

```nix
{
  factory.domain.agent.role.builder.<name> = {
    description = "<What the expert does. Use for ...>";
    instruction = builtins.readFile ./utils/agent/role/<name>/ROLE.md;
    harness.opencode.mode = "subagent";
  };
}
```

- `harness.opencode.mode = "subagent"` is the convention of each shipped role.
- Copy the declaration. Change only `<name>`, the description, and the body. After the next
  shell entry, each harness in use has a rendered role file.
