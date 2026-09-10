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
    ".github/workflows/docs-site.yml".text = lib.mkForce ''
      name: Documentation site

      on:
        push:
          paths:
            - docs/**
            - apps/documentation/**
            - devenv.nix
            - .github/workflows/docs-site.yml
        workflow_dispatch:

      permissions:
        contents: read

      concurrency:
        group: docs-site
        cancel-in-progress: false

      jobs:
        build:
          if: github.ref_name == github.event.repository.default_branch
          runs-on: ubuntu-latest
          defaults:
            run:
              working-directory: apps/documentation
          steps:
            - name: Check out the repository
              uses: actions/checkout@v4
            - name: Build the final report
              uses: xu-cheng/latex-action@v3
              with:
                root_file: docs/reports/final-project-report.vi.tex
                latexmk_use_xelatex: true
            - name: Copy the final report
              working-directory: .
              run: |
                mkdir -p apps/documentation/static
                cp docs/reports/final-project-report.vi.pdf apps/documentation/static/final-project-report.vi.pdf
            - name: Set up Node.js
              uses: actions/setup-node@v4
              with:
                node-version: 22
                cache: npm
                cache-dependency-path: apps/documentation/package-lock.json
            - name: Install the dependencies
              run: npm ci
            - name: Build the website
              run: npm run build
            - name: Upload the website
              uses: actions/upload-pages-artifact@v3
              with:
                path: apps/documentation/build

        deploy:
          needs: build
          runs-on: ubuntu-latest
          permissions:
            pages: write
            id-token: write
            contents: read
          environment:
            name: github-pages
            url: ''${{ steps.deployment.outputs.page_url }}
          steps:
            - name: Deploy to GitHub Pages
              id: deployment
              uses: actions/deploy-pages@v4
            - name: Check out the notification code
              uses: actions/checkout@v4
              with:
                persist-credentials: false
            - name: Notify the team about the deployment
              run: python3 .github/docs-site/notify.py
              env:
                DOCS_SITE_NOTIFICATION_USES: '["slack"]'
                DOCS_SITE_NOTIFICATION_SLACK_WEBHOOK: ''${{ secrets.DOCS_SITE_NOTIFICATION_WEBHOOK }}
                DOCS_SITE_DEPLOYMENT_URL: ''${{ steps.deployment.outputs.page_url }}
                DOCS_SITE_REPOSITORY: ''${{ github.repository }}
                DOCS_SITE_REF_NAME: ''${{ github.ref_name }}
                DOCS_SITE_COMMIT_SHA: ''${{ github.sha }}
                DOCS_SITE_RUN_URL: ''${{ github.server_url }}/''${{ github.repository }}/actions/runs/''${{ github.run_id }}
    '';
    "apps/documentation/docusaurus.config.js".source = lib.mkForce (
      pkgs.writeText "docusaurus.config.js" ''
        // The factory owns this file. Nix renders site.json from the options
        // factory.composition.artifact-driven.docs-site; this file reads it.
        const site = require('./site.json');

        // Title Case each word so the sidebar casing stays consistent:
        // "decisions" becomes "Decisions" and "repo-arch" becomes "Repo Arch".
        function humanizeFolder(name) {
          return name
            .split('/')
            .pop()
            .replace(/[-_]+/g, ' ')
            .split(' ')
            .filter(Boolean)
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
        }

        // Give each folder without a README.md a generated index page, and label each
        // folder with a README.md by the title of that page.
        function withIndexes(items, docs) {
          return items.map((item) => {
            if (item.type !== 'category') {
              return item;
            }
            const category = { ...item, items: withIndexes(item.items, docs) };
            if (category.link && category.link.type === 'doc') {
              const doc = docs.find((d) => d.id === category.link.id);
              if (doc) {
                category.label = doc.title;
              }
            } else {
              const folder = folderOf(category, docs);
              const label = humanizeFolder(folder || category.label);
              category.label = label;
              if (!category.link) {
                if (folder) {
                  category.link = { type: 'generated-index', title: label, slug: '/' + folder };
                }
              } else if (category.link.type === 'generated-index' && !category.link.title) {
                category.link = { ...category.link, title: label };
              }
            }
            return category;
          });
        }

        // The folder of a category is the sourceDirName of a direct doc child. When the
        // category has no direct doc child, it is the parent folder of its first child
        // category.
        function folderOf(category, docs) {
          for (const child of category.items) {
            if (child.type === 'doc') {
              const doc = docs.find((d) => d.id === child.id);
              if (doc) {
                return doc.sourceDirName;
              }
            }
          }
          for (const child of category.items) {
            if (child.type === 'category') {
              const childFolder = folderOf(child, docs);
              if (childFolder) {
                return childFolder.split('/').slice(0, -1).join('/');
              }
            }
          }
          return null;
        }

        async function sidebarItemsGenerator({ defaultSidebarItemsGenerator, ...args }) {
          const items = await defaultSidebarItemsGenerator(args);
          return withIndexes(items, args.docs);
        }

        /** @type {import('@docusaurus/types').Config} */
        const config = {
          title: site.title,
          url: site.url,
          baseUrl: site.baseUrl,
          trailingSlash: true,
          staticDirectories: ['static'],
          onBrokenLinks: 'warn',
          markdown: {
            format: 'detect',
            hooks: {
              onBrokenMarkdownLinks: 'warn',
            },
          },
          presets: [
            [
              'classic',
              {
                blog: false,
                docs: {
                  path: '../../docs',
                  routeBasePath: '/',
                  sidebarPath: './sidebars.js',
                  numberPrefixParser: false,
                  exclude: [
                    '**/_*.{js,jsx,ts,tsx,md,mdx}',
                    '**/_*/**',
                    '**/*.test.{js,jsx,ts,tsx}',
                    '**/__tests__/**',
                    '**/templates/**',
                  ],
                  sidebarItemsGenerator,
                },
                theme: {
                  customCss: './src/css/custom.css',
                },
              },
            ],
          ],
          themeConfig: {
            navbar: {
              title: site.title,
            },
          },
        };

        module.exports = config;
      ''
    );
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
