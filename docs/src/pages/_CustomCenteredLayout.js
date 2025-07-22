import React, { useEffect } from 'react';

export default function CustomCenteredLayout({ children }) {
  useEffect(() => {
    // Hide the left sidebar
    const sidebar = document.querySelector('.theme-doc-sidebar-container');
    if (sidebar) sidebar.style.display = 'none';
    // Hide the sidebar toggle button if present
    const sidebarToggle = document.querySelector('.theme-doc-sidebar-toggle');
    if (sidebarToggle) sidebarToggle.style.display = 'none';
    // Expand main content to full width
    const main = document.querySelector('.main-wrapper');
    if (main) main.style.marginLeft = '0';
    return () => {
      if (sidebar) sidebar.style.display = '';
      if (sidebarToggle) sidebarToggle.style.display = '';
      if (main) main.style.marginLeft = '';
    };
  }, []);
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'var(--ifm-background-color)' }}>
      <div style={{ width: '100%', maxWidth: 900, margin: '0 auto', padding: '6rem' }}>
        {children}
      </div>
    </div>
  );
}
