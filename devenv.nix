{ pkgs, lib, ... }:
{
  # Git hooks. prek installs the shims when you enter the devenv shell. devenv generates
  # .pre-commit-config.yaml and copies it into the repository, so a developer without devenv can
  # run the same hooks with prek. The convco hook runs at the commit-msg stage and
  # rejects a commit message that does not follow Conventional Commits.
  git-hooks = {
    package = pkgs.prek;
    hooks.convco = {
      enable = true;
      # Portable entry: uses convco from PATH instead of a Nix store path, so the committed
      # .pre-commit-config.yaml also works on a machine without Nix.
      entry = "sh -c 'convco check --from-stdin < \"$1\"' convco-hook";
    };
    # The markdownlint hook runs at the pre-commit stage and checks the staged markdown files
    # against .markdownlint.yaml. It skips the templates in docs/, the CLAUDE.md include stub,
    # and the agent harness files that the factory generates.
    hooks.markdownlint = {
      enable = true;
      # Portable entry: uses markdownlint from PATH and the committed .markdownlint.yaml, so the
      # committed .pre-commit-config.yaml also works on a machine without Nix.
      entry = "markdownlint --config .markdownlint.yaml";
      excludes = [
        "^docs/.*/templates/"
        "^CLAUDE\\.md$"
        "^\\.(agents|claude|codex|opencode)/"
      ];
    };
    # The ripsecrets hook runs at the pre-commit stage and scans the staged text files for
    # secrets: API keys, access tokens, and private keys. It rejects the commit when it finds one.
    # A false positive can be allowed with a `# pragma: allowlist secret` comment on the line, or
    # with a path in a .secretsignore file.
    hooks.ripsecrets = {
      enable = true;
      # Portable entry: uses ripsecrets from PATH instead of a Nix store path, so the committed
      # .pre-commit-config.yaml also works on a machine without Nix.
      entry = "ripsecrets --strict-ignore";
    };
    # The gitleaks hook runs at the pre-commit stage and scans the staged diff with the gitleaks
    # rule set: about 150 provider rules (AWS, Anthropic, OpenAI, Azure, DigitalOcean, ...) plus
    # entropy checks. It fills the gaps of ripsecrets, which has no AWS rule. The output redacts
    # the secret value. A false positive can be allowed with a `gitleaks:allow` comment on the
    # line, or with a fingerprint in a .gitleaksignore file.
    hooks.gitleaks = {
      enable = true;
      name = "gitleaks";
      description = "Scan the staged diff for secrets with gitleaks";
      package = pkgs.gitleaks;
      # Portable entry: uses gitleaks from PATH instead of a Nix store path, so the committed
      # .pre-commit-config.yaml also works on a machine without Nix.
      entry = "gitleaks git --pre-commit --staged --redact --no-banner --verbose";
      # gitleaks reads the staged diff from git itself, so it does not take the file list.
      pass_filenames = false;
    };
  };

  files.".pre-commit-config.yaml".copyMode = lib.mkForce "copy";

  # markdownlint rules. devenv generates .markdownlint.yaml from this attribute set and copies it
  # into the repository, so the hook reads the same rules with or without devenv.
  files.".markdownlint.yaml" = {
    copyMode = "copy";
    yaml = {
      default = true;
      # The documents wrap at 100 columns. Code blocks and tables can be wider.
      MD013 = {
        line_length = 100;
        code_blocks = false;
        tables = false;
      };
      # The templates use <angle brackets> for placeholders, and a seeded document keeps them
      # until it is filled in.
      MD033 = false;
    };
  };

  factory = {
    composition.artifact-driven.docs-site = {
      enable = true;
      url = "https://tetrix-uit.github.io";
      base-url = "/tetrix/";
    };
    domain = {
      documentation.use = "artifact-driven";
      repo-arch.use = "multiple";
      design.use = "ddd";
      agent = {
        harness.uses = [
          "claude"
          "opencode"
          "codex"
        ];
        # Implementation experts of this repository. One expert per component; the body of
        # each role is utils/agent/role/<name>/ROLE.md, kept apart from the component code.
        role.builder = {
          tetrix-expert = {
            description = "Implements the Tetrix game in apps/tetrix: the game core with its rules, the game loop, the input, the rendering, and the on-device storage. The game has no backend. Owns phase 4 of the artifact-driven documentation model for that component. Use for a task that changes apps/tetrix, or when the solution expert needs the specifications or the tasks of the game.";
            instruction = builtins.readFile ./utils/agent/role/tetrix-expert/ROLE.md;
            harness.opencode.mode = "subagent";
          };
          lib-expert = {
            description = "Implements the shared libraries in libs/: the shared kernels, the published languages, and the technical libraries, with their consumers. Owns phase 4 of the artifact-driven documentation model for those components. Use for a task that changes libs/, or when the solution expert needs the specifications or the tasks of a library.";
            instruction = builtins.readFile ./utils/agent/role/lib-expert/ROLE.md;
            harness.opencode.mode = "subagent";
          };
          e2e-expert = {
            description = "Implements the shared end-to-end tests in e2e/: one test per workflow that uses more than one application or service. Owns phase 4 of the artifact-driven documentation model for that component. Use for a task that changes e2e/, or when the solution expert needs the specifications or the tasks of the end-to-end tests.";
            instruction = builtins.readFile ./utils/agent/role/e2e-expert/ROLE.md;
            harness.opencode.mode = "subagent";
          };
        };
        skill.builtins = {
          asd-ste-100.enable = true;
        };
      };
      ci-cd = {
        provider = {
          use = "github-actions";
          github-actions = { };
        };
      };
      project-management = {
        provider = {
          use = "trello";
          trello = {
          };
        };
      };
    };
  };
}
