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
