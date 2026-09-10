{ pkgs, lib, ... }:
{
  packages = [
    pkgs.texliveFull
  ];

  git-hooks = {
    package = pkgs.prek;
    hooks.convco = {
      enable = true;
      entry = "sh -c 'convco check --from-stdin < \"$1\"' convco-hook";
    };
    hooks.markdownlint = {
      enable = true;
      entry = "markdownlint --config .markdownlint.yaml";
      excludes = [
        "^docs/.*/templates/"
        "^CLAUDE\\.md$"
        "^\\.(agents|claude|codex|opencode)/"
      ];
    };
    hooks.ripsecrets = {
      enable = true;
      entry = "ripsecrets --strict-ignore";
    };
    hooks.gitleaks = {
      enable = true;
      name = "gitleaks";
      description = "Scan the staged diff for secrets with gitleaks";
      package = pkgs.gitleaks;
      entry = "gitleaks git --pre-commit --staged --redact --no-banner --verbose";
      pass_filenames = false;
    };
  };

  files = {
    ".pre-commit-config.yaml".copyMode = lib.mkForce "copy";
    ".markdownlint.yaml" = {
      copyMode = "copy";
      yaml = {
        default = true;
        MD013 = {
          line_length = 100;
          code_blocks = false;
          tables = false;
        };
        MD033 = false;
      };
    };
  };

  factory = {
    composition.artifact-driven = {
      docs-site = {
        enable = true;
        url = "https://tetrix-uit.github.io";
        base-url = "/tetrix/";
        notification = {
          uses = [ "slack" ];
          slack.webhook-secret = "DOCS_SITE_NOTIFICATION_WEBHOOK";
        };
      };
      project-issues = {
        enable = true;
        notification = {
          uses = [ "slack" ];
          slack.webhook-secret = "ARTIFACT_NOTIFICATION_WEBHOOK";
        };
      };
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
            board-id = "CaFqAJ3t";
            implementation-board-id = "41x81yWC";
          };
        };
      };
    };
  };
}
