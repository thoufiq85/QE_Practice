# SDET Automation Framework

A production-ready test automation framework for interview preparation demonstrating scalable design patterns and CI/CD integration practices.

## 🎯 Overview

This framework showcases best practices for SDET (Software Development Engineer in Test) roles:

- **Pytest** for test execution and detailed HTML reporting
- **Selenium** for robust web UI automation
- **Page Object Model (POM)** for maintainable, reusable test code
- **YAML configuration** for environment and browser management
- **GitHub Actions** for automated CI/CD pipeline
- **Modular architecture** supporting functional, regression, and integration testing

---

## 📁 Project Structure

```
automation-framework/
├── README.md                           # This file
├── QUICKSTART.md                       # Quick reference guide
├── ARCHITECTURE_AND_WORKFLOW.md        # Detailed architecture & diagrams
├── CI_CD_TROUBLESHOOTING.md           # Debugging common issues
├── requirements.txt                    # Python dependencies
├── pytest.ini                          # Pytest configuration
├── .gitignore                          # Git ignore rules
│
├── .github/workflows/
│   └── tests.yml                       # GitHub Actions CI/CD pipeline
│
└── automation_framework/
    ├── __init__.py
    ├── conftest.py                     # Pytest fixtures & setup
    ├── config/
    │   └── config.yaml                 # Environment configuration
    ├── pages/
    │   ├── __init__.py
    │   └── login_page.py               # Page Object Model example
    ├── tests/
    │   ├── __init__.py
    │   └── test_login.py               # Sample test cases
    └── utils/
        ├── __init__.py
        └── test_data.py                # Shared test data
```

---

## 📋 Component Details

### **Root Level Files**

| File | Purpose |
|------|---------|
| `requirements.txt` | Lists all dependencies: pytest, selenium, pyyaml, webdriver-manager, pytest-html |
| `pytest.ini` | Configures pytest behavior: test discovery, markers, output format |
| `.gitignore` | Excludes venv/, __pycache__/, reports/ from version control |
| `.github/workflows/tests.yml` | GitHub Actions CI/CD pipeline - runs on every push |

### **Core Framework Files**

#### `automation_framework/conftest.py`
Pytest configuration with reusable fixtures:
- **`load_config()`** – Reads `config.yaml` settings
- **`config` fixture** – Loads config once per session
- **`browser` fixture** – Creates/destroys WebDriver for each test
- **`base_url` fixture** – Provides application URL to tests

✓ **Benefit:** Centralized setup/teardown keeps tests clean and focused

#### `automation_framework/config/config.yaml`
Environment and browser settings:
```yaml
base_url: https://example.com      # Target application URL
browser: chrome                     # Browser type
implicit_wait: 10                   # Selenium wait time (seconds)
headless: false                     # Show/hide browser UI
report_dir: reports                 # Test report output folder
```

✓ **Benefit:** Change environments without modifying code

#### `automation_framework/pages/login_page.py`
Page Object Model class encapsulating login page interactions:
- Stores element locators (CSS selectors, IDs, XPath)
- Provides user-friendly methods: `open()`, `enter_username()`, `submit()`, etc.
- Hides UI implementation details from tests

✓ **Benefit:** When UI changes, update one file instead of dozens of tests

#### `automation_framework/tests/test_login.py`
Test cases using POM and fixtures:
```python
@pytest.mark.smoke
def test_login_with_invalid_credentials(browser, base_url):
    login_page = LoginPage(browser)
    login_page.open(base_url)
    login_page.enter_username("wrong_user")
    login_page.enter_password("wrong_pass")
    login_page.submit()
    assert "invalid" in login_page.get_error_text()
```

✓ **Benefit:** Tests are readable, maintainable, and focused on assertions

#### `automation_framework/utils/test_data.py`
Shared test data and helper functions:
```python
def get_credentials(kind="valid"):
    data = {
        "valid": ("user@example.com", "Pass123"),
        "invalid": ("wrong@example.com", "Wrong")
    }
    return data.get(kind)
```

✓ **Benefit:** Separates test data from test logic; easy to swap data sources

---

## ✅ Why This Framework Fits the Job Description

| Requirement | How It's Addressed |
|-------------|-------------------|
| **Scalable automation framework** | Modular design with POM, clear separation of concerns |
| **CI/CD integration** | GitHub Actions pipeline automatically runs tests on push |
| **Coding standards & best practices** | Config, fixtures, pages, tests clearly separated |
| **Regression optimization** | Test markers enable selective test execution |
| **All aspects of automation** | Supports plan, script, execute, analyze, report |
| **Multiple testing levels** | UI, functional, regression test support |
| **Testing deliverables** | HTML reports, clear documentation, test management ready |
| **AI-enabled automation** | Extensible for AI-driven test generation and optimization |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Text editor (VS Code recommended)

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/automation-framework.git
cd automation-framework
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Target App
Edit `automation_framework/config/config.yaml`:
```yaml
base_url: https://your-target-app.com
```

### 3. Run Tests Locally
```bash
# All tests
pytest automation_framework/tests -v

# With HTML report
pytest automation_framework/tests -v --html=reports/report.html --self-contained-html

# Specific test
pytest automation_framework/tests/test_login.py::test_login_with_invalid_credentials -v

# Smoke tests only
pytest automation_framework/tests -v -m smoke
```

Open `reports/report.html` in your browser to view detailed results.

---

## 🔄 GitHub & CI/CD Setup

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: SDET automation framework"
git remote add origin https://github.com/yourusername/automation-framework.git
git branch -M main
git push -u origin main
```

### Step 2: Verify CI/CD is Running

1. Go to `https://github.com/yourusername/automation-framework`
2. Click **Actions** tab (top menu)
3. Watch your workflow execute:
   - 🟡 **Yellow** = Running
   - 🟢 **Green** = Passed
   - 🔴 **Red** = Failed
4. Click workflow to see detailed logs and download reports

### Expected CI/CD Flow
```
git push → GitHub detects push → Workflow triggered → 
Tests run on Ubuntu VM → Report generated → Artifacts uploaded
```

---

## 📝 Adding New Tests

### Pattern 1: Create Page Object
```python
# automation_framework/pages/dashboard_page.py
from selenium.webdriver.common.by import By

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.welcome_text = (By.CSS_SELECTOR, ".welcome-message")
    
    def get_welcome_message(self) -> str:
        return self.driver.find_element(*self.welcome_text).text
```

### Pattern 2: Create Test
```python
# automation_framework/tests/test_dashboard.py
import pytest
from automation_framework.pages.dashboard_page import DashboardPage

@pytest.mark.smoke
def test_dashboard_welcome_message(browser, base_url):
    dashboard = DashboardPage(browser)
    dashboard.open(base_url + "/dashboard")
    assert "Welcome" in dashboard.get_welcome_message()
```

### Pattern 3: Commit & Push
```bash
git add automation_framework/pages/dashboard_page.py automation_framework/tests/test_dashboard.py
git commit -m "Add dashboard page and welcome test"
git push origin main
```

Your new test automatically runs in CI/CD! 🎯

---

## 🛠️ Test Execution Commands

```bash
# Run all tests with verbose output
pytest automation_framework/tests -v

# Run with HTML report
pytest automation_framework/tests -v --html=reports/report.html --self-contained-html

# Run only smoke tests
pytest automation_framework/tests -v -m smoke

# Run tests matching a pattern
pytest automation_framework/tests -k "login" -v

# Run specific file
pytest automation_framework/tests/test_login.py -v

# Run specific test
pytest automation_framework/tests/test_login.py::test_login_with_invalid_credentials -v

# Show print statements during test execution
pytest automation_framework/tests -v -s

# Stop on first failure
pytest automation_framework/tests -v -x

# Parallel execution (install pytest-xdist first)
pytest automation_framework/tests -v -n auto
```

---

## 📊 CI/CD Best Practices

- ✅ **Run tests on every push** to catch regressions early
- ✅ **Use test markers** (`@pytest.mark.smoke`, `@pytest.mark.regression`) for selective execution
- ✅ **Generate HTML reports** for detailed failure analysis
- ✅ **Set branch protections** to require CI/CD to pass before merging
- ✅ **Monitor workflow duration** and optimize slow tests
- ✅ **Review logs carefully** when CI/CD fails

---

## 📚 Additional Resources

- **[QUICKSTART.md](QUICKSTART.md)** – Copy-paste commands reference
- **[ARCHITECTURE_AND_WORKFLOW.md](ARCHITECTURE_AND_WORKFLOW.md)** – Detailed architecture with flow diagrams
- **[CI_CD_TROUBLESHOOTING.md](CI_CD_TROUBLESHOOTING.md)** – Common issues and solutions

---

## 🚀 Next Steps for Growth

1. **API Testing** – Add requests library for API automation
2. **JIRA Integration** – Auto-update test status in JIRA
3. **Performance Testing** – Measure page load times with Selenium
4. **Parallel Execution** – Run tests concurrently with pytest-xdist
5. **AI Test Selection** – Use ML to predict relevant regression tests
6. **Docker Integration** – Run tests in containers for consistency

---

## 🤖 AI & ML Integration Ideas

- Generate test cases from user stories using AI
- Analyze test history to recommend regression subsets
- AI-based synthetic test data generation
- Automated test report summarization
- ML-powered flaky test detection and retry optimization
- AI-driven bug prediction and test prioritization

---

## 📞 Support & Troubleshooting

- **Tests fail in CI but pass locally?** → See [CI_CD_TROUBLESHOOTING.md](CI_CD_TROUBLESHOOTING.md)
- **How do I see test results?** → Download pytest-report artifact from Actions tab
- **How often do tests run?** → Automatically on every push to `main` branch
- **Can I run tests on schedule?** → Yes, modify `.github/workflows/tests.yml`

---

## 📌 Interview Highlights

When discussing this framework:

✅ "I designed a scalable test automation framework using Page Object Model for maintainability"  
✅ "I implemented automated CI/CD using GitHub Actions to run tests on every code push"  
✅ "I separated concerns: configuration, fixtures, page objects, and tests for clean architecture"  
✅ "I created comprehensive documentation for team onboarding and knowledge sharing"  
✅ "The framework supports functional, regression, integration, and performance testing"  
✅ "I leveraged pytest markers for organizing and selectively executing test suites"  
✅ "I built extensibility for AI-driven test generation and optimization"

---

**Ready to get started? Check [QUICKSTART.md](QUICKSTART.md) for step-by-step commands!**
