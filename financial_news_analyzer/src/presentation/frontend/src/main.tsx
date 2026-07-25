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
  shortLabel: string;
}

const NAVIGATION: NavItem[] = [
  { key: "home", label: "Overview", shortLabel: "01" },
  { key: "analysis", label: "News research", shortLabel: "02" },
  { key: "market", label: "Markets", shortLabel: "03" },
  { key: "support", label: "Support", shortLabel: "04" },
];

function App({ args }: ComponentProps) {
  const activePage = (args.active_page as PageKey | undefined) ?? "home";

  useEffect(() => {
    Streamlit.setFrameHeight(76);
  }, []);

  return (
    <header className="shell" aria-label="Financial News Analyzer navigation">
      <button
        type="button"
        className="brand-cluster"
        aria-label="Go to overview"
        onClick={() => Streamlit.setComponentValue("home")}
      >
        <span className="brand-mark" aria-hidden="true">
          <span className="brand-bar brand-bar-one" />
          <span className="brand-bar brand-bar-two" />
          <span className="brand-bar brand-bar-three" />
        </span>
        <span className="brand-copy">
          <span className="brand-name">Financial News</span>
          <span className="brand-product">Analyzer</span>
        </span>
      </button>

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
              <span className="nav-index" aria-hidden="true">{item.shortLabel}</span>
              <span className="nav-label">{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="live-status" aria-label="Live provider data available">
        <span className="status-pulse" aria-hidden="true" />
        <span>Provider connected</span>
      </div>
    </header>
  );
}

const ConnectedApp = withStreamlitConnection(App);
createRoot(document.getElementById("root")!).render(<ConnectedApp />);
