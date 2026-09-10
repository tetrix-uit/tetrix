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
