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
  { key: "home", label: "Overview", icon: "⌂" },
  { key: "analysis", label: "News research", icon: "◫" },
  { key: "market", label: "Market data", icon: "↗" },
  { key: "support", label: "Support", icon: "?" },
];

function App({ args }: ComponentProps) {
  const activePage = (args.active_page as PageKey | undefined) ?? "home";

  useEffect(() => {
    Streamlit.setFrameHeight(82);
  }, []);

  return (
    <header className="shell" aria-label="Application navigation">
      <div className="brand">
        <span className="brand-mark">F</span>
        <span>Financial News Analyzer</span>
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
      <div className="live-status"><span /> Live provider data</div>
    </header>
  );
}

const ConnectedApp = withStreamlitConnection(App);
createRoot(document.getElementById("root")!).render(<ConnectedApp />);
