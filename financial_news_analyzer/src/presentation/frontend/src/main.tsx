import React, { useEffect } from "react";
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
  { key: "home", label: "Genel Bakış", icon: "◌" },
  { key: "analysis", label: "Haberler", icon: "✦" },
  { key: "market", label: "Piyasalar", icon: "↗" },
  { key: "support", label: "Destek", icon: "?" },
];

function App({ args }: ComponentProps) {
  const activePage = (args.active_page as PageKey | undefined) ?? "home";

  useEffect(() => {
    Streamlit.setFrameHeight(72);
  }, []);

  return (
    <header className="shell" aria-label="Financial News Analyzer navigation">
      <a className="brand-cluster" href="#" onClick={(e) => e.preventDefault()}>
        <span className="brand-mark" aria-hidden="true">F</span>
        <span className="brand-name">Financial News Analyzer</span>
      </a>

      <nav className="navigation" aria-label="Workspaces">
        {NAVIGATION.map((item) => {
          const isActive = item.key === activePage;
          return (
            <button
              type="button"
              key={item.key}
              className={isActive ? "nav-item active" : "nav-item"}
              aria-current={isActive ? "page" : undefined}
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
        <span className="status-pulse" aria-hidden="true" />
        <span>Canlı veri</span>
      </div>
    </header>
  );
}

const ConnectedApp = withStreamlitConnection(App);
createRoot(document.getElementById("root")!).render(<ConnectedApp />);
