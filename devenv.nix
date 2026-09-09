{
  factory = {
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
