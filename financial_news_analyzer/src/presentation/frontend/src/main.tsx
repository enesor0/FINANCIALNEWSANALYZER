import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import "./styles.css";

type PageKey = "home" | "analysis" | "market" | "support";

interface NavItem {
  key: PageKey;
  label: string;
  icon: string;
}

const NAVIGATION: NavItem[] = [
  { key: "home", label: "Overview", icon: "◌" },
  { key: "analysis", label: "Research", icon: "✦" },
  { key: "market", label: "Markets", icon: "↗" },
  { key: "support", label: "Support", icon: "?" },
];

function App({ args }: ComponentProps) {
  const activePage = (args.active_page as PageKey | undefined) ?? "home";
  const [hovered, setHovered] = useState<PageKey | null>(null);

  useEffect(() => {
    Streamlit.setFrameHeight(86);
  }, []);

  const activeIndex = useMemo(
    () => Math.max(0, NAVIGATION.findIndex((item) => item.key === activePage)),
    [activePage],
  );

  return (
    <header className="shell" aria-label="Financial News Analyzer navigation">
      <div className="shell-glow" aria-hidden="true" />

      <a className="brand-cluster" href="#" onClick={(e) => e.preventDefault()}>
        <span className="brand-mark" aria-hidden="true">
          <i /><i /><i />
        </span>
        <div className="brand-copy">
          <span className="brand-name">Financial News</span>
          <span className="brand-subtitle">Intelligence desk</span>
        </div>
      </a>

      <nav className="navigation" aria-label="Workspaces">
        <span
          className="nav-indicator"
          aria-hidden="true"
          style={{
            transform: `translateX(${activeIndex * 100}%)`,
            opacity: hovered ? 0 : 1,
          }}
        />
        {NAVIGATION.map((item) => {
          const isActive = item.key === activePage;
          return (
            <button
              type="button"
              key={item.key}
              className={isActive ? "nav-item active" : "nav-item"}
              aria-current={isActive ? "page" : undefined}
              onMouseEnter={() => setHovered(item.key)}
              onMouseLeave={() => setHovered(null)}
              onClick={() => Streamlit.setComponentValue(item.key)}
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
              {isActive && <span className="nav-dot" aria-hidden="true" />}
            </button>
          );
        })}
      </nav>

      <div className="live-status" aria-label="Live provider data available">
        <span className="status-pulse" aria-hidden="true">
          <span className="status-pulse-ring" />
        </span>
        <div className="live-status-copy">
          <strong>Provider live</strong>
          <small>Research workspace</small>
        </div>
      </div>
    </header>
  );
}

const ConnectedApp = withStreamlitConnection(App);
createRoot(document.getElementById("root")!).render(<ConnectedApp />);
