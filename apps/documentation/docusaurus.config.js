// The factory owns this file. Nix renders site.json from the options
// factory.composition.artifact-driven.docs-site; this file reads it.
const site = require('./site.json');

// The feature-folder order is repository data. It travels only through
// site.json; this generic file contains no repository-specific name.
const FEATURE_ORDER = site.featureOrder ?? [];

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

function folderBasename(dirName) {
  if (!dirName) return null;
  const parts = dirName.split('/').filter(Boolean);
  return parts.length ? parts[parts.length - 1] : null;
}

function fileBasename(source) {
  if (!source) return null;
  const base = source.split('/').pop();
  return base.replace(/\.(md|mdx)$/i, '');
}

// Give each folder without a README.md a generated index page, and label each
// folder with a README.md by the title of that page. Capture the source
// identity of every item in a temporary private field, before the sort reads it.
function withIndexes(items, docs) {
  return items.map((item) => {
    if (item.type !== 'category') {
      const doc = docs.find((d) => d.id === item.id);
      return { ...item, source: doc ? fileBasename(doc.source) : null };
    }
    const category = { ...item, items: withIndexes(item.items, docs) };
    if (category.link && category.link.type === 'doc') {
      const doc = docs.find((d) => d.id === category.link.id);
      if (doc) {
        category.label = doc.title;
      }
      category.source = doc ? folderBasename(doc.sourceDirName) : null;
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
      category.source = folderBasename(folder);
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

const PHASE_ORDER = ['requirements', 'specifications', 'decisions', 'tasks'];
const featureOrderIndex = new Map(FEATURE_ORDER.map((name, index) => [name, index]));
const phaseOrderIndex = new Map(PHASE_ORDER.map((name, index) => [name, index]));

function isFeatureFolder(item) {
  return item.type === 'category' && !!item.source && item.source.startsWith('feat-');
}

function featureRank(item) {
  return featureOrderIndex.has(item.source) ? featureOrderIndex.get(item.source) : Infinity;
}

function isIndexDocument(item) {
  if (item.type !== 'doc' || !item.source) return false;
  const name = item.source.toLowerCase();
  return name === 'index' || name === 'readme';
}

function phaseRank(item) {
  if (item.type !== 'category' || !item.source) return Infinity;
  return phaseOrderIndex.has(item.source) ? phaseOrderIndex.get(item.source) : Infinity;
}

function parseVersion(item) {
  if (item.type !== 'category' || !item.source) return null;
  const match = /^(\d+)\.(\d+)\.(\d+)$/.exec(item.source);
  if (!match) return null;
  return {
    major: Number(match[1]),
    minor: Number(match[2]),
    patch: Number(match[3]),
  };
}

// Compare two strings by Unicode code point. Array.from reads complete code
// points, so a non-BMP label compares as one unit. This is locale-independent.
function compareCodePoints(a, b) {
  const charsA = Array.from(a);
  const charsB = Array.from(b);
  const length = Math.min(charsA.length, charsB.length);
  for (let i = 0; i < length; i += 1) {
    const difference = charsA[i].codePointAt(0) - charsB[i].codePointAt(0);
    if (difference !== 0) return difference;
  }
  return charsA.length - charsB.length;
}

// A document label falls back from the item label to the document title to the
// item identifier. A category label is set by withIndexes before the sort.
function displayLabel(item, context) {
  if (item.type === 'doc') {
    return item.label ?? context.docTitleById.get(item.id) ?? item.id;
  }
  return item.label ?? item.id ?? '';
}

function compareFallback(a, b, context) {
  const labelA = displayLabel(a, context);
  const labelB = displayLabel(b, context);
  const lowerDifference = compareCodePoints(labelA.toLowerCase(), labelB.toLowerCase());
  if (lowerDifference !== 0) return lowerDifference;
  const originalDifference = compareCodePoints(labelA, labelB);
  if (originalDifference !== 0) return originalDifference;
  return compareCodePoints(a.source ?? '', b.source ?? '');
}

// Each rule applies only to its item type and parent folder. The fallback runs
// when no special rule separates the two items.
function compareSidebarItems(a, b, parent, context) {
  if (isFeatureFolder(a) && isFeatureFolder(b)) {
    const rankA = featureRank(a);
    const rankB = featureRank(b);
    if (rankA !== rankB) return rankA - rankB;
  }

  const indexA = isIndexDocument(a);
  const indexB = isIndexDocument(b);
  if (indexA !== indexB) return indexA ? -1 : 1;

  const phaseA = phaseRank(a);
  const phaseB = phaseRank(b);
  if (phaseA !== phaseB) return phaseA - phaseB;

  if (parent === 'versions') {
    const versionA = parseVersion(a);
    const versionB = parseVersion(b);
    if (versionA && versionB) {
      if (versionA.major !== versionB.major) return versionB.major - versionA.major;
      if (versionA.minor !== versionB.minor) return versionB.minor - versionA.minor;
      if (versionA.patch !== versionB.patch) return versionB.patch - versionA.patch;
    } else if (versionA) {
      return -1;
    } else if (versionB) {
      return 1;
    }
  }

  if (parent === 'changes') {
    const initialA = a.source === 'change-initial';
    const initialB = b.source === 'change-initial';
    if (initialA !== initialB) return initialA ? -1 : 1;
  }

  return compareFallback(a, b, context);
}

function sortSidebarItems(items, parent, context) {
  items.sort((a, b) => compareSidebarItems(a, b, parent, context));
  for (const item of items) {
    if (item.type === 'category' && item.items) {
      sortSidebarItems(item.items, item.source, context);
    }
  }
  return items;
}

// Remove the temporary private identity field before the items return.
function stripPrivateFields(items) {
  return items.map((item) => {
    const { source, ...rest } = item;
    if (rest.type === 'category' && rest.items) {
      return { ...rest, items: stripPrivateFields(rest.items) };
    }
    return rest;
  });
}

async function sidebarItemsGenerator({ defaultSidebarItemsGenerator, ...args }) {
  const items = await defaultSidebarItemsGenerator(args);
  const indexed = withIndexes(items, args.docs);
  const context = {
    docs: args.docs,
    docTitleById: new Map(args.docs.map((doc) => [doc.id, doc.title])),
  };
  return stripPrivateFields(sortSidebarItems(indexed, null, context));
}

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: site.title,
  url: site.url,
  baseUrl: site.baseUrl,
  trailingSlash: true,
  staticDirectories: site.staticDirectories,
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
