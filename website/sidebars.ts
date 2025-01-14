import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'doc',
      id: 'getting-started/intro',
      label: 'Introduction',
    },
    {
      type: 'doc',
      id: 'getting-started/getting-started',
      label: 'Setup Guide',
    },
    {
      type: 'category',
      label: 'Core Concepts',
      items: [
        'core-concepts/architecture',
      ],
    },
    {
      type: 'doc',
      id: 'reference/api',
      label: 'API Reference',
    },
  ],
};

export default sidebars;
