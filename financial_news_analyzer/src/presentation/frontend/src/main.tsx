import React, { useEffect } from "react";
import { createRoot } from "react-dom/client";
import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import "./styles.css";

type PageKey = "home" | "analysis" | "market" | "support";

const navigation: Array<{ key: PageKey; label: string; icon: string }> = [
  { key: "home", label: "Overview", icon: "◌" },
  { key: "analysis", label: "Research", icon: "✦" },
  { key: "market", label: "Markets", icon: "↗" },
  { key: "support", label: "Support", icon: "?" },
];

function App({ args }: ComponentProps) {
  const activePage = (args.active_page as PageKey | undefined) ?? "home";

  useEffect(() => {
    Streamlit.setFrameHeight(82);
  }, []);

  return (
    <header className="shell" aria-label="Financial News Analyzer navigation">
      <div className="brand-cluster">
        <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
        <div className="brand-copy">
          <span className="brand-name">Financial News</span>
          <span className="brand-subtitle">Intelligence desk</span>
        </div>
      </div>
      <nav className="navigation" aria-label="Workspaces">
        {navigation.map((item) => (
          <button
            type="button"
            key={item.key}
            className={item.key === activePage ? "nav-item active" : "nav-item"}
            aria-current={item.key === activePage ? "page" : undefined}
            onClick={() => Streamlit.setComponentValue(item.key)}
          >
            <span aria-hidden="true">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>
      <div className="live-status" aria-label="Live provider data available">
        <span className="status-pulse" aria-hidden="true" />
        <div>
          <strong>Provider live</strong>
          <small>Research workspace</small>
        </div>
      </div>
    </header>
  );
}

const ConnectedApp = withStreamlitConnection(App);
createRoot(document.getElementById("root")!).render(<ConnectedApp />);
