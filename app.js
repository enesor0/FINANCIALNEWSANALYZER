const state = {
  quotes: [],
  selectedSymbol: null,
  selectedProfile: null,
  selectedHistory: [],
  marketDays: 90,
  chartMode: "line",
  newsArticles: [],
  newsAnalysis: null,
  selectionRequest: 0,
  searchController: null,
  searchTimer: null,
  loaded: { overview: false, news: false, markets: false, sessions: false },
  cache: {
    news: new Map(),
    search: new Map(),
    profiles: new Map(),
    history: new Map(),
  },
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const escapeHtml = (value = "") =>
  String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
  }[character]));

const safeUrl = (value) => {
  try {
    const url = new URL(value);
    return ["http:", "https:"].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
};

const formatCurrency = (value, currency = "USD", digits = 2) => {
  if (value == null || Number.isNaN(Number(value))) return "—";
  try {
    return Number(value).toLocaleString("en-US", {
      style: "currency",
      currency: currency || "USD",
      maximumFractionDigits: digits,
    });
  } catch {
    return `${Number(value).toLocaleString("en-US", { maximumFractionDigits: digits })} ${currency || ""}`.trim();
  }
};

const formatCompact = (value) =>
  value == null ? "—" : Intl.NumberFormat("en", { notation: "compact", maximumFractionDigits: 2 }).format(value);

const formatNumber = (value, digits = 2) =>
  value == null ? "—" : Number(value).toLocaleString("en-US", { maximumFractionDigits: digits });

const formatPercent = (value, digits = 2) =>
  value == null ? "—" : `${Number(value) >= 0 ? "+" : ""}${Number(value).toFixed(digits)}%`;

const formatDate = (value) => {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "Unknown date"
    : date.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
};

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || "The data provider is temporarily unavailable.");
  return payload;
}

async function cachedFetch(cache, key, url) {
  if (cache.has(key)) return cache.get(key);
  const data = await fetchJson(url);
  cache.set(key, data);
  return data;
}

function showView(id) {
  $$(".view").forEach((view) => view.classList.toggle("active", view.id === id));
  $$(".nav-link").forEach((link) => link.classList.toggle("active", link.dataset.view === id));
  history.replaceState(null, "", `#${id}`);
  window.scrollTo({ top: 0, behavior: "smooth" });
  if (id === "markets" && !state.loaded.markets) loadMarket();
  if (id === "sessions" && !state.loaded.sessions) loadSessions();
  if (id === "news" && !state.loaded.news) loadNews();
}

async function loadPulse() {
  const container = $("#pulse-list");
  try {
    const data = await fetchJson("/api/market?symbols=AAPL,MSFT,NVDA");
    container.innerHTML = data.quotes.map((quote) => `
      <div class="pulse-row">
        <b>${escapeHtml(quote.symbol)}</b>
        <b>${formatCurrency(quote.price)}</b>
        <small>${escapeHtml(quote.name)}</small>
        <small class="${quote.changePercent >= 0 ? "up" : "down"}">${formatPercent(quote.changePercent)}</small>
      </div>`).join("");
    state.loaded.overview = true;
  } catch (error) {
    container.innerHTML = `<div class="empty-state error-state">${escapeHtml(error.message)}</div>`;
  }
}

function signalLabel(score) {
  if (score > .2) return "Positive coverage bias";
  if (score < -.2) return "Negative coverage bias";
  return "Mixed / neutral coverage";
}

function renderBreakdown(title, counts, total) {
  const rows = Object.entries(counts || {}).sort((a, b) => b[1] - a[1]);
  return `
    <section class="insight-panel">
      <h3>${escapeHtml(title)}</h3>
      ${rows.length ? rows.map(([label, count]) => `
        <div class="breakdown-row">
          <span>${escapeHtml(label.replaceAll("_", " "))}</span>
          <div class="breakdown-track"><div class="breakdown-fill" style="width:${Math.max(3, count / Math.max(total, 1) * 100)}%"></div></div>
          <b>${count}</b>
        </div>`).join("") : `<p class="panel-copy">No breakdown is available.</p>`}
    </section>`;
}

function renderNewsDashboard(data) {
  const analysis = data.analysis;
  const sources = new Set(data.articles.map((item) => item.source)).size;
  const signal = signalLabel(analysis.averageScore);
  $("#news-summary").innerHTML = `
    <div class="metric"><small>Source-linked articles</small><strong>${analysis.totalArticles}</strong><em>${data.queryTerms.length} search terms</em></div>
    <div class="metric"><small>Coverage signal</small><strong>${analysis.averageScore >= 0 ? "+" : ""}${analysis.averageScore.toFixed(2)}</strong><em>${escapeHtml(signal)}</em></div>
    <div class="metric"><small>Average confidence</small><strong>${Math.round(analysis.averageConfidence * 100)}%</strong><em>Keyword evidence consistency</em></div>
    <div class="metric"><small>Distinct sources</small><strong>${sources}</strong><em>Provider-returned publishers</em></div>`;

  const strongest = [...data.articles].sort((a, b) => Math.abs(b.score) - Math.abs(a.score))[0];
  $("#news-insights").innerHTML = `
    ${renderBreakdown("Sentiment distribution", analysis.sentimentCounts, analysis.totalArticles)}
    <section class="insight-panel analysis-callout">
      <small class="eyebrow">Research readout</small>
      <strong>${escapeHtml(signal)}</strong>
      <p>${strongest
        ? `Highest-impact headline: “${escapeHtml(strongest.title)}” with a ${formatNumber(strongest.score)} score. Review the linked source and keyword evidence before drawing conclusions.`
        : "No provider-linked article was available for this query."}</p>
    </section>
    ${renderBreakdown("Coverage by category", analysis.categoryCounts, analysis.totalArticles)}
    ${renderBreakdown("Coverage by search term", analysis.companyCounts, analysis.totalArticles)}`;
}

function populateNewsFilters(articles) {
  const sentiments = [...new Set(articles.map((item) => item.sentiment))].sort();
  const categories = [...new Set(articles.map((item) => item.category))].sort();
  $("#sentiment-filter").innerHTML = `<option value="all">All signals</option>${sentiments.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value.replaceAll("_", " "))}</option>`).join("")}`;
  $("#category-filter").innerHTML = `<option value="all">All categories</option>${categories.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join("")}`;
  $("#news-toolbar").classList.remove("hidden");
}

function renderNewsArticles() {
  const query = $("#article-search").value.trim().toLowerCase();
  const sentiment = $("#sentiment-filter").value;
  const category = $("#category-filter").value;
  const sort = $("#news-sort").value;
  const articles = state.newsArticles.filter((item) => {
    const searchable = `${item.title} ${item.summary} ${item.source} ${item.company} ${item.category}`.toLowerCase();
    return (!query || searchable.includes(query))
      && (sentiment === "all" || item.sentiment === sentiment)
      && (category === "all" || item.category === category);
  });

  articles.sort((a, b) => {
    if (sort === "impact") return Math.abs(b.score) - Math.abs(a.score);
    if (sort === "confidence") return b.confidence - a.confidence;
    return new Date(b.publishedAt) - new Date(a.publishedAt);
  });

  $("#news-result-count").textContent = `${articles.length} of ${state.newsArticles.length}`;
  $("#news-results").innerHTML = articles.length ? articles.map((item) => {
    const link = safeUrl(item.url);
    const evidence = [
      ...(item.evidence?.positive || []).map((word) => ({ word, kind: "positive" })),
      ...(item.evidence?.negative || []).map((word) => ({ word, kind: "negative" })),
      ...(item.evidence?.neutral || []).map((word) => ({ word, kind: "neutral" })),
    ].slice(0, 8);
    return `
      <article class="article-card">
        <div class="article-meta">
          <span>${escapeHtml(item.company)}</span><span>·</span>
          <span>${escapeHtml(item.category)}</span><span>·</span>
          <span>${escapeHtml(formatDate(item.publishedAt))}</span>
        </div>
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.summary)}</p>
        <div class="article-evidence">
          ${evidence.length
            ? evidence.map(({ word, kind }) => `<span class="evidence-chip ${kind}">${escapeHtml(word)}</span>`).join("")
            : `<span class="evidence-chip">No matched sentiment keywords</span>`}
        </div>
        <div class="article-footer">
          ${link ? `<a href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.source)} →</a>` : `<span>${escapeHtml(item.source)}</span>`}
          <span class="article-score">score ${formatNumber(item.score)} · confidence ${Math.round(item.confidence * 100)}%</span>
          <span class="sentiment ${escapeHtml(item.sentiment)}">${escapeHtml(item.sentiment.replaceAll("_", " "))}</span>
        </div>
      </article>`;
  }).join("") : `<div class="empty-state">No articles match the current filters.</div>`;
}

async function loadNews(event) {
  if (event) event.preventDefault();
  const results = $("#news-results");
  const companies = $("#company-input").value.trim();
  const limit = $("#news-limit").value;
  if (!companies) {
    results.innerHTML = `<div class="empty-state error-state">Enter at least one company, ticker, sector, or topic.</div>`;
    return;
  }
  results.innerHTML = `<div class="empty-state">Retrieving and analyzing provider coverage…</div>`;
  $("#news-summary").innerHTML = "";
  $("#news-insights").innerHTML = "";
  $("#news-toolbar").classList.add("hidden");
  try {
    const key = `${companies.toLowerCase()}|${limit}`;
    const data = await cachedFetch(
      state.cache.news,
      key,
      `/api/news?companies=${encodeURIComponent(companies)}&limit=${limit}`,
    );
    state.newsArticles = data.articles;
    state.newsAnalysis = data.analysis;
    renderNewsDashboard(data);
    populateNewsFilters(data.articles);
    renderNewsArticles();
    state.loaded.news = true;
  } catch (error) {
    results.innerHTML = `<div class="empty-state error-state">${escapeHtml(error.message)}</div>`;
  }
}

function renderWatchlist() {
  const watchlist = $("#watchlist");
  watchlist.innerHTML = state.quotes.length ? state.quotes.map((quote) => `
    <button class="watch-row ${quote.symbol === state.selectedSymbol ? "active" : ""}" data-symbol="${escapeHtml(quote.symbol)}">
      <b>${escapeHtml(quote.symbol)}</b>
      <b>${formatCurrency(quote.price, quote.currency)}</b>
      <small>${escapeHtml(quote.name)}</small>
      <small class="${quote.changePercent >= 0 ? "up" : "down"}">${formatPercent(quote.changePercent)}</small>
    </button>`).join("") : `<div class="empty-state">No market rows are available.</div>`;
  $$(".watch-row").forEach((row) => row.addEventListener("click", () => selectSymbol(row.dataset.symbol)));
}

async function loadMarket(force = false) {
  const watchlist = $("#watchlist");
  if (force) {
    watchlist.innerHTML = `<div class="skeleton"></div><div class="skeleton"></div>`;
    state.cache.profiles.clear();
    state.cache.history.clear();
  }
  try {
    const data = await fetchJson("/api/market");
    const discovered = state.quotes.filter((item) => !data.quotes.some((quote) => quote.symbol === item.symbol));
    state.quotes = [...discovered, ...data.quotes];
    renderWatchlist();
    state.loaded.markets = true;
    await selectSymbol(state.selectedSymbol || data.quotes[0]?.symbol);
  } catch (error) {
    watchlist.innerHTML = `<div class="empty-state error-state">${escapeHtml(error.message)}</div>`;
  }
}

function renderSearchResults(data) {
  const container = $("#market-search-results");
  if (!data.results.length) {
    container.innerHTML = `<div class="empty-state">No matching instrument was returned. Try an exact ticker or a broader company name.</div>`;
    container.classList.remove("hidden");
    return;
  }
  container.innerHTML = data.results.map((item, index) => `
    <button class="search-result" data-search-index="${index}">
      <b>${escapeHtml(item.symbol)}</b>
      <span>${escapeHtml(item.name)}</span>
      <small>${escapeHtml([item.quoteType, item.exchange, item.sector].filter(Boolean).join(" · "))}</small>
    </button>`).join("");
  container.classList.remove("hidden");
  $$(".search-result").forEach((button) => button.addEventListener("click", () => {
    const item = data.results[Number(button.dataset.searchIndex)];
    container.classList.add("hidden");
    $("#market-search-input").value = `${item.symbol} · ${item.name}`;
    selectSymbol(item.symbol, item);
  }));
}

async function searchMarket(event, suppliedQuery = null) {
  if (event) event.preventDefault();
  const rawValue = suppliedQuery ?? $("#market-search-input").value;
  const query = rawValue.split(" · ")[0].trim();
  const container = $("#market-search-results");
  if (!query) {
    container.classList.add("hidden");
    return;
  }
  container.innerHTML = `<div class="empty-state">Searching global instruments…</div>`;
  container.classList.remove("hidden");
  if (state.searchController) state.searchController.abort();
  state.searchController = new AbortController();
  try {
    const key = query.toLowerCase();
    let data = state.cache.search.get(key);
    if (!data) {
      data = await fetchJson(`/api/search?q=${encodeURIComponent(query)}&limit=15`, {
        signal: state.searchController.signal,
      });
      state.cache.search.set(key, data);
    }
    renderSearchResults(data);
  } catch (error) {
    if (error.name === "AbortError") return;
    container.innerHTML = `<div class="empty-state error-state">${escapeHtml(error.message)}</div>`;
  }
}

function updateQuoteFromProfile(profile) {
  const quote = {
    symbol: profile.symbol,
    name: profile.name,
    category: profile.sector || profile.quoteType,
    price: profile.price,
    previousClose: profile.previousClose,
    change: profile.change,
    changePercent: profile.changePercent,
    volume: profile.volume,
    dayHigh: profile.dayHigh,
    dayLow: profile.dayLow,
    currency: profile.currency,
  };
  state.quotes = [quote, ...state.quotes.filter((item) => item.symbol !== profile.symbol)].slice(0, 18);
  renderWatchlist();
}

function renderProfile(profile) {
  const link = safeUrl(profile.website);
  $("#instrument-profile").innerHTML = `
    <p class="eyebrow">Instrument profile</p>
    <h2>${escapeHtml(profile.name)}</h2>
    <div class="profile-tags">
      ${[profile.symbol, profile.quoteType, profile.exchange, profile.sector, profile.industry]
        .filter(Boolean).map((value) => `<span>${escapeHtml(value)}</span>`).join("")}
    </div>
    <p class="panel-copy">${escapeHtml(profile.description || "The provider did not return a business or asset description.")}</p>
    ${link ? `<a class="profile-link" href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer">Official website →</a>` : ""}`;

  const currency = profile.currency || "USD";
  $("#instrument-metrics").innerHTML = [
    ["Market cap", formatCompact(profile.marketCap), currency],
    ["Trailing P/E", formatNumber(profile.trailingPE), "reported"],
    ["Forward P/E", formatNumber(profile.forwardPE), "estimate"],
    ["52-week range", `${formatCurrency(profile.fiftyTwoWeekLow, currency)} – ${formatCurrency(profile.fiftyTwoWeekHigh, currency)}`, "provider range"],
    ["Average volume", formatCompact(profile.averageVolume), "daily"],
    ["Beta", formatNumber(profile.beta), "market sensitivity"],
  ].map(([label, value, note]) => `<div class="metric"><small>${label}</small><strong>${value}</strong><em>${note}</em></div>`).join("");
}

function renderInstrumentNews(data, profile) {
  const list = $("#instrument-news");
  const articles = data?.articles || [];
  $("#instrument-news-title").textContent = `${profile?.symbol || state.selectedSymbol} coverage`;
  list.innerHTML = articles.length ? articles.slice(0, 5).map((item) => {
    const link = safeUrl(item.url);
    const content = `<small>${escapeHtml(item.source)} · ${escapeHtml(formatDate(item.publishedAt))}</small><strong>${escapeHtml(item.title)}</strong>`;
    return link
      ? `<a class="compact-news-item" href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer">${content}</a>`
      : `<div class="compact-news-item">${content}</div>`;
  }).join("") : `<div class="empty-state">No related provider coverage was returned.</div>`;
}

async function loadHistoryForSelected() {
  const symbol = state.selectedSymbol;
  if (!symbol) return;
  $("#price-chart").innerHTML = `<div class="empty-state">Loading ${escapeHtml(symbol)} history…</div>`;
  const key = `${symbol}|${state.marketDays}`;
  try {
    const data = await cachedFetch(
      state.cache.history,
      key,
      `/api/history/${encodeURIComponent(symbol)}?days=${state.marketDays}`,
    );
    if (symbol !== state.selectedSymbol) return;
    state.selectedHistory = data.bars;
    renderChart(data.bars);
  } catch (error) {
    if (symbol !== state.selectedSymbol) return;
    $("#price-chart").innerHTML = `<div class="empty-state error-state">${escapeHtml(error.message)}</div>`;
  }
}

async function selectSymbol(symbol, discovery = null) {
  if (!symbol) return;
  const normalized = symbol.trim().toUpperCase();
  state.selectedSymbol = normalized;
  state.selectedProfile = null;
  state.selectedHistory = [];
  const requestId = ++state.selectionRequest;
  renderWatchlist();

  const existing = state.quotes.find((item) => item.symbol === normalized);
  $("#chart-name").textContent = discovery?.name || existing?.name || normalized;
  $("#chart-price").textContent = existing?.price != null
    ? formatCurrency(existing.price, existing.currency)
    : "Loading…";
  $("#chart-meta").textContent = [discovery?.quoteType, discovery?.exchange, discovery?.sector].filter(Boolean).join(" · ") || normalized;
  const change = $("#chart-change");
  change.className = `change-pill ${existing?.changePercent > 0 ? "up" : existing?.changePercent < 0 ? "down" : "neutral"}`;
  change.textContent = formatPercent(existing?.changePercent);
  $("#instrument-metrics").innerHTML = `<div class="empty-state">Loading detailed metrics…</div>`;
  $("#instrument-profile").innerHTML = `<p class="eyebrow">Instrument profile</p><h2>${escapeHtml(discovery?.name || normalized)}</h2><p class="panel-copy">Loading provider metadata…</p>`;
  $("#instrument-news").innerHTML = `<div class="empty-state">Loading related coverage…</div>`;
  $("#research-selected-news").disabled = true;

  const profilePromise = cachedFetch(
    state.cache.profiles,
    normalized,
    `/api/profile/${encodeURIComponent(normalized)}`,
  );
  const historyPromise = loadHistoryForSelected();
  const newsPromise = profilePromise.then((profile) => {
    const newsQuery = profile.shortName || normalized;
    return cachedFetch(
      state.cache.news,
      `market|${newsQuery.toLowerCase()}|5`,
      `/api/news?companies=${encodeURIComponent(newsQuery)}&limit=5`,
    );
  });
  const [profileResult, , newsResult] = await Promise.allSettled([
    profilePromise,
    historyPromise,
    newsPromise,
  ]);
  if (requestId !== state.selectionRequest) return;

  if (profileResult.status === "fulfilled") {
    const profile = profileResult.value;
    state.selectedProfile = profile;
    updateQuoteFromProfile(profile);
    renderProfile(profile);
    renderChart(state.selectedHistory);
    $("#chart-name").textContent = `${profile.name} · ${profile.symbol}`;
    $("#chart-price").textContent = formatCurrency(profile.price, profile.currency);
    $("#chart-meta").textContent = [profile.exchange, profile.quoteType, profile.currency, profile.sector].filter(Boolean).join(" · ");
    change.className = `change-pill ${profile.changePercent > 0 ? "up" : profile.changePercent < 0 ? "down" : "neutral"}`;
    change.textContent = formatPercent(profile.changePercent);
  } else {
    $("#instrument-profile").innerHTML = `<p class="eyebrow">Instrument profile</p><h2>${escapeHtml(normalized)}</h2><p class="panel-copy error-state">${escapeHtml(profileResult.reason.message)}</p>`;
    $("#instrument-metrics").innerHTML = "";
  }

  if (newsResult.status === "fulfilled") {
    renderInstrumentNews(newsResult.value, state.selectedProfile);
  } else {
    $("#instrument-news").innerHTML = `<div class="empty-state error-state">${escapeHtml(newsResult.reason.message)}</div>`;
  }
  $("#research-selected-news").disabled = false;
}

function renderChart(bars) {
  const chart = $("#price-chart");
  if (!bars.length) {
    chart.innerHTML = `<div class="empty-state">No price history is available.</div>`;
    $("#chart-stats").innerHTML = "";
    return;
  }

  const sampled = bars.length > 180
    ? bars.filter((_, index) => index % Math.ceil(bars.length / 180) === 0 || index === bars.length - 1)
    : bars;
  const lows = sampled.map((bar) => bar.low);
  const highs = sampled.map((bar) => bar.high);
  const closes = sampled.map((bar) => bar.close);
  const min = Math.min(...lows);
  const max = Math.max(...highs);
  const width = 800;
  const height = 330;
  const padX = 30;
  const padTop = 24;
  const padBottom = 30;
  const range = max - min || 1;
  const xAt = (index) => padX + index / Math.max(1, sampled.length - 1) * (width - padX * 2);
  const yAt = (value) => padTop + (max - value) / range * (height - padTop - padBottom);

  const labels = [0, .5, 1].map((ratio) => {
    const y = padTop + ratio * (height - padTop - padBottom);
    const value = max - ratio * range;
    return `<line class="grid-line" x1="${padX}" x2="${width - padX}" y1="${y}" y2="${y}" /><text class="chart-label" x="${width - padX}" y="${y - 6}" text-anchor="end">${formatCurrency(value, state.selectedProfile?.currency)}</text>`;
  }).join("");
  const dateLabels = `
    <text class="chart-label" x="${padX}" y="${height - 5}">${escapeHtml(formatDate(sampled[0].date))}</text>
    <text class="chart-label" x="${width - padX}" y="${height - 5}" text-anchor="end">${escapeHtml(formatDate(sampled.at(-1).date))}</text>`;

  let drawing;
  if (state.chartMode === "candles") {
    const candleWidth = Math.max(1.5, Math.min(7, (width - padX * 2) / sampled.length * .65));
    drawing = sampled.map((bar, index) => {
      const x = xAt(index);
      const openY = yAt(bar.open);
      const closeY = yAt(bar.close);
      const highY = yAt(bar.high);
      const lowY = yAt(bar.low);
      const bodyY = Math.min(openY, closeY);
      const bodyHeight = Math.max(1.5, Math.abs(closeY - openY));
      const kind = bar.close >= bar.open ? "candle-up" : "candle-down";
      return `<line class="candle-wick" x1="${x}" x2="${x}" y1="${highY}" y2="${lowY}" /><rect class="${kind}" x="${x - candleWidth / 2}" y="${bodyY}" width="${candleWidth}" height="${bodyHeight}" rx="1" />`;
    }).join("");
  } else {
    const points = closes.map((value, index) => [xAt(index), yAt(value)]);
    const line = points.map((point) => point.join(",")).join(" ");
    const area = `${padX},${height - padBottom} ${line} ${width - padX},${height - padBottom}`;
    drawing = `<polygon class="chart-area" points="${area}" /><polyline class="chart-line" points="${line}" />`;
  }

  chart.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${state.chartMode === "candles" ? "Daily candlestick" : "Daily closing price"} history">
      <defs><linearGradient id="chart-gradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#93b1a6" stop-opacity=".28"/><stop offset="1" stop-color="#93b1a6" stop-opacity="0"/></linearGradient></defs>
      ${labels}${drawing}${dateLabels}
    </svg>`;

  const first = bars[0];
  const latest = bars.at(-1);
  const periodReturn = first.close ? (latest.close - first.close) / first.close * 100 : null;
  const averageVolume = bars.reduce((sum, bar) => sum + (bar.volume || 0), 0) / bars.length;
  $("#chart-stats").innerHTML = [
    ["Period return", formatPercent(periodReturn)],
    ["Period high", formatCurrency(Math.max(...bars.map((bar) => bar.high)), state.selectedProfile?.currency)],
    ["Period low", formatCurrency(Math.min(...bars.map((bar) => bar.low)), state.selectedProfile?.currency)],
    ["Average volume", formatCompact(averageVolume)],
  ].map(([label, value]) => `<div class="chart-stat"><small>${label}</small><b>${value}</b></div>`).join("");
}

async function loadSessions() {
  const grid = $("#session-grid");
  try {
    const markets = await fetchJson("/api/schedules");
    grid.innerHTML = markets.map((market) => {
      const localDate = new Date(market.localTime);
      const time = localDate.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
      return `
        <article class="session-card">
          <div class="session-top">
            <span class="session-code">${escapeHtml(market.flag)} ${escapeHtml(market.code)}</span>
            <span class="session-status ${market.status}"><i></i>${escapeHtml(market.status)}</span>
          </div>
          <h3>${escapeHtml(market.name)}</h3>
          <p>${escapeHtml(market.timezone)} · ${escapeHtml(market.currency || "—")}</p>
          <div class="session-time"><strong>${escapeHtml(time)}</strong><small>${escapeHtml(market.openTime)}–${escapeHtml(market.closeTime)}</small></div>
        </article>`;
    }).join("");
    state.loaded.sessions = true;
  } catch (error) {
    grid.innerHTML = `<div class="empty-state error-state">${escapeHtml(error.message)}</div>`;
  }
}

$$(".nav-link").forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
$$("[data-open-view]").forEach((button) => button.addEventListener("click", () => showView(button.dataset.openView)));
$$("[data-news-query]").forEach((button) => button.addEventListener("click", () => {
  $("#company-input").value = button.dataset.newsQuery;
  loadNews();
}));
$$("[data-market-query]").forEach((button) => button.addEventListener("click", () => {
  $("#market-search-input").value = button.dataset.marketQuery;
  searchMarket(null, button.dataset.marketQuery);
}));

$("#news-form").addEventListener("submit", loadNews);
$("#article-search").addEventListener("input", renderNewsArticles);
$("#sentiment-filter").addEventListener("change", renderNewsArticles);
$("#category-filter").addEventListener("change", renderNewsArticles);
$("#news-sort").addEventListener("change", renderNewsArticles);
$("#refresh-market").addEventListener("click", () => loadMarket(true));
$("#market-search-form").addEventListener("submit", searchMarket);
$("#market-search-input").addEventListener("input", () => {
  clearTimeout(state.searchTimer);
  const query = $("#market-search-input").value.trim();
  if (query.length < 2) {
    $("#market-search-results").classList.add("hidden");
    return;
  }
  state.searchTimer = setTimeout(() => searchMarket(null, query), 350);
});

$$("[data-days]").forEach((button) => button.addEventListener("click", () => {
  state.marketDays = Number(button.dataset.days);
  $$("[data-days]").forEach((item) => item.classList.toggle("active", item === button));
  loadHistoryForSelected();
}));
$$("[data-chart-mode]").forEach((button) => button.addEventListener("click", () => {
  state.chartMode = button.dataset.chartMode;
  $$("[data-chart-mode]").forEach((item) => item.classList.toggle("active", item === button));
  renderChart(state.selectedHistory);
}));

$("#research-selected-news").addEventListener("click", () => {
  const query = state.selectedProfile?.name || state.selectedSymbol;
  if (!query) return;
  $("#company-input").value = query;
  showView("news");
  loadNews();
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".market-search-shell")) {
    $("#market-search-results").classList.add("hidden");
  }
});

const initialView = location.hash.slice(1);
showView(["overview", "news", "markets", "sessions"].includes(initialView) ? initialView : "overview");
loadPulse();
