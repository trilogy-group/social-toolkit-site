import React from 'react';
import { useLocation } from '@docusaurus/router';
import DocSidebar from '@theme-original/DocSidebar';
import type { Props } from '@theme/DocSidebar';
import { usePluginData } from '@docusaurus/useGlobalData';

// Get package version from package.json
const version = '2.1.2'; // Hardcoded for now, can be imported from package.json if needed

export default function DocSidebarWrapper(props: Props): JSX.Element {
  return (
    <>
      <DocSidebar {...props} />
      <div className="sidebar-version">Version: v{version}</div>
    </>
  );
} 