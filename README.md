# 🏦 Financial News Analyzer

<div align="center">

![Financial News Analyzer](https://img.shields.io/badge/Financial-News%20Analyzer-2c3e50?style=for-the-badge&logo=chart-line)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Professional Financial Analysis & Market Intelligence Platform with Modern Contact System**

🌐 **Live Demo:** [financialnewsanalyzer.streamlit.app](https://financialnewsanalyzer.streamlit.app/)

*Provider-linked financial news analysis and latest-available daily market-data visualization*

[🚀 Demo](#demo) • [📖 Documentation](#documentation) • [⚡ Quick Start](#quick-start) • [🔧 Features](#features)

</div>

---

## 🌟 Overview

Financial News Analyzer is a research-oriented Streamlit application combining linked financial-news retrieval, explainable keyword-based sentiment scoring, and interactive market-data visualizations.

## ⚠️ Current data status

- The **Market Data** page retrieves the latest available daily OHLCV data from Yahoo Finance through `yfinance`, cached for five minutes.
- The **Financial Analysis** page retrieves linked provider news from the same integration and applies a transparent keyword-based sentiment baseline.
- Dashboard summary cards describe configuration; they do not present market values.
- This project is for research and education, not investment advice. `yfinance` is unaffiliated with Yahoo and its data access is intended for personal use; obtain an appropriately licensed provider before commercial or production use.

### 🎯 Key Highlights

- **🔎 Explainable Sentiment**: Keyword-based scoring with visible source links
- **📊 Latest Daily Data**: Provider-backed OHLCV charts with five-minute caching
- **🌍 Market Schedules**: Weekday schedule display across global timezones
- **📱 Responsive Design**: Modern UI with professional animations and dark theme
- **🧩 Focused codebase**: Only the modules used by the Streamlit workspaces are retained
- **⚡ Cached Retrieval**: Short-lived provider response caching to reduce rate limiting
- **✉️ Contact Page**: Direct email contact details and FAQs

## 🔧 Features

### 📰 Financial News Analysis
- **Sentiment Analysis**: Explainable keyword scoring of provider-returned headline and summary text
- **Company-specific Insights**: Targeted news retrieval for selected companies
- **News Aggregation**: Provider-linked news articles with their available URLs
- **Historical Trends**: Sentiment timeline of the retrieved articles

### 📈 Market Data Visualization
- **Interactive Charts**: Candlestick, line, and area charts with zoom functionality
- **Technical Indicators**: Price and volume visualizations from daily OHLCV history
- **Market Overview**: Latest available provider prices for the supported symbol universe
- **Category Performance**: Compare live provider returns across the supported categories

### 🌍 Global Market Coverage
- **Multi-timezone Support**: Weekday schedules across different exchange time zones
- **Regional Analysis**: Schedule coverage for major financial regions

### ✉️ Professional Contact System
- **Modern Interface**: Sophisticated contact form with responsive design
- **Primary Channel**: Direct email contact
- **FAQ Support**: Comprehensive frequently asked questions section
- **Professional Support**: Technical assistance and customer service

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/enecpp/FINANCIALNEWSANALYZER.git
   cd FINANCIALNEWSANALYZER/financial_news_analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**
   ```bash
   streamlit run Start.py
   ```

5. **Access the platform**
   - Open your browser and navigate to `http://localhost:8501`
   - Enjoy the comprehensive financial analysis experience!

The application uses a native Streamlit interface with a custom React
navigation component. Open `http://localhost:8501` after starting the app.

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
pytz>=2023.3
yfinance>=0.2.54,<1.0
```

## �️ Security & Best Practices

**Security Features:**

- 🔒 **Data Protection**: All user data is handled with industry-standard security practices
- 🌐 **Deployment Security**: HTTPS must be configured by the deployment platform
- 🧹 **Rendered Provider Text**: External article title/source fields are escaped before HTML rendering
- 🔗 **External Provider**: Yahoo Finance data is retrieved via `yfinance`; see its terms before use

**Best Practices:**

- ⚡ **Performance**: Five-minute provider caching for the live data pages
- 📱 **Responsive**: Mobile-first design approach
- ♿ **Accessibility**: WCAG compliance for inclusive user experience
- 🎨 **Modern UI**: Contemporary design patterns and animations

## 🏗️ Architecture

The application follows Onion Architecture: dependencies point inward, while the
composition root wires the outer adapters together.

```
financial_news_analyzer/
├── 📁 src/
│   ├── 📁 domain/               # Sentiment scoring and market schedule value objects
│   ├── 📁 application/          # Use cases and provider/repository port contracts
│   ├── 📁 infrastructure/       # Yahoo Finance and static-schedule adapters
│   ├── 📁 presentation/         # Shared design, navigation, and market-clock UI
│   └── bootstrap.py             # Composition root
├── 📁 pages/                    # Streamlit pages
│   ├── 1_Financial_Analysis.py  # News sentiment analysis
│   ├── 2_Market_Data.py         # Market data visualization
│   └── 3_Contact_Us.py          # Professional contact interface
├── 📁 tests/                    # Unit and integration tests
├── Start.py                     # Main application entry point
└── requirements.txt             # Python dependencies
```

### 🎨 Design Principles

- Keep domain models and rules free from Streamlit, pandas, yfinance, and provider details.
- Depend on application-owned ports; implement those ports only in infrastructure adapters.
- Let Streamlit pages call use cases and adapt their results for charts and tables.
- Prefer live provider data; do not fall back to simulated news or market prices.
- Keep the keyword sentiment baseline inspectable and easy to change.

## 🎮 Usage

Run the Streamlit app, open **Financial Analysis** to select companies and retrieve linked articles, or open **Market Data** to view the supported live symbol universe and its daily OHLCV history. The app does not currently expose a public Python `analyzer` API, portfolio management, trading signals, or investment recommendations.

## 🌟 Screenshots

### Main Dashboard
![Main Dashboard](https://via.placeholder.com/800x400/2c3e50/ffffff?text=Financial+News+Analyzer+Dashboard)

### Financial Analysis Page
![Financial Analysis](https://via.placeholder.com/800x400/34495e/ffffff?text=AI-Powered+Sentiment+Analysis)

### Market Data Visualization
![Market Data](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Latest+Available+Market+Data)

### Contact Us Page
![Contact Us](https://via.placeholder.com/800x400/FF6B6B/ffffff?text=Professional+Contact+Interface)

## 🔮 Roadmap

### 🎯 Upcoming Features

- [ ] **Machine Learning Models**: Advanced predictive models for price forecasting
- [ ] **API Integration**: Real-time data feeds from Bloomberg, Reuters, Alpha Vantage
- [ ] **Mobile App**: React Native mobile application
- [ ] **Alerts System**: Email and SMS notifications for market events
- [ ] **Portfolio Management**: Advanced portfolio tracking and optimization
- [ ] **Social Sentiment**: Twitter and Reddit sentiment integration
- [ ] **Backtesting Engine**: Strategy backtesting with historical data
- [ ] **Multi-language Support**: International language support
- [ ] **Advanced Contact Features**: Live chat integration and ticket system
- [ ] **AI Chatbot**: Intelligent customer support assistant

### 🚀 Performance Enhancements

- [ ] **Redis Caching**: Advanced caching for improved performance
- [ ] **Database Integration**: PostgreSQL for data persistence
- [ ] **Microservices**: Dockerized microservices architecture
- [ ] **Load Balancing**: Horizontal scaling capabilities

## 🤝 Contributing

We welcome contributions from the financial technology community! Here's how you can contribute:

### 🛠️ Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### 📝 Contribution Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure all tests pass before submitting
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

<div align="center">

**Built with ❤️ by Financial Technology Enthusiasts**

[![GitHub](https://img.shields.io/badge/GitHub-enesor0-181717?style=flat-square&logo=github)](https://github.com/enecpp)

</div>

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing web app framework
- **Plotly Team** for powerful visualization capabilities
- **Financial Data Providers** for market data access
- **Open Source Community** for continuous inspiration

## 📞 Support

Need help? We're here for you!

- 📧 **Email**: enesor8@gmail.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/enesor0/FINANCIALNEWSANALYZER/issues)
- ✉️ **Contact Form**: Use the built-in Contact Us page for inquiries
- 💬 **Live Support**: Available through the application interface
- 🔐 **Security**: All communications are secure and confidential

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=enecpp.mleng-financial_news_analyzer)

</div>
