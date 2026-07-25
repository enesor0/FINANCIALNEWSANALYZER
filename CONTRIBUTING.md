# Contributing to Financial News Analyzer

First off, thank you for considering contributing to Financial News Analyzer! 🎉

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide system information and screenshots

### 💡 Feature Requests
- Suggest new features through GitHub Issues
- Explain the use case and expected behavior
- Consider implementation complexity

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Follow coding standards
- Add comprehensive tests
- Update documentation
- Submit a pull request

### ✉️ Contact & Support
- Use the built-in Contact Us page
- Professional support interface
- Priority-based issue handling
- FAQ section available

## 📋 Development Guidelines

### 🏗️ Architecture Principles
- Keep domain rules independent from Streamlit, pandas, and external providers
- Put orchestration in application use cases and define their provider contracts as ports
- Keep Yahoo Finance and other external integrations in infrastructure adapters
- Let Streamlit pages call use cases instead of infrastructure services directly
- Add modules only when they have a live caller or test
- Avoid simulated market/news data in production workflows

### 🎨 Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Write descriptive variable names
- Add docstrings for functions and classes

### 🧪 Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use the built-in `unittest` suite

### 📚 Documentation
- Update README for new features
- Add inline comments for complex logic
- Document API changes
- Include usage examples
- Update Contact Us information for new features

## 🚀 Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/FINANCIALNEWSANALYZER.git
   cd FINANCIALNEWSANALYZER/financial_news_analyzer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests** (when available)
   ```bash
   pytest tests/
   ```

5. **Start Development Server**
   ```bash
   streamlit run Start.py
   ```

## 📝 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Changes**
   - Implement your feature
   - Add tests
   - Update documentation

3. **Test Your Changes** (when available)
   ```bash
   pytest tests/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push and Submit PR**
   ```bash
   git push origin feature/amazing-feature
   ```

## 🎯 Commit Message Convention

Use conventional commits for clear history:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

## 🔍 Code Review Process

1. All PRs require at least one review
2. Automated tests must pass
3. Code coverage should not decrease
4. Documentation must be updated
5. Breaking changes require discussion

## 🏷️ Issue Labels

- `bug` - Bug reports
- `enhancement` - Feature requests
- `documentation` - Documentation improvements
- `good first issue` - Beginner-friendly issues
- `help wanted` - Issues needing assistance
- `contact-system` - Contact form and support related
- `ui-improvement` - User interface enhancements

## 📞 Getting Help

- ✉️ **Contact Form**: Use the built-in Contact Us page in the application
- 📧 **Email**: Direct contact via enesor8@gmail.com
- 📖 **Documentation**: Check the comprehensive README
- 🔍 **Search Issues**: Look through existing GitHub issues
- 💬 **Professional Support**: Available through the application interface

## 🙏 Recognition

All contributors will be:
- Added to the contributors list
- Mentioned in release notes
- Recognized in the README

Thank you for making Financial News Analyzer better! 🚀
