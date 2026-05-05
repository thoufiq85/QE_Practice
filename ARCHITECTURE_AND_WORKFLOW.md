# SDET Framework: Complete Workflow & Architecture

## 📋 End-to-End Workflow: From Code Push to CI/CD Execution

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR LOCAL MACHINE                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    1. You write test code
                    2. pytest works locally
                    3. You commit changes
                                  │
                                  ▼
                      git add .
                      git commit -m "..."
                      git push origin main
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      YOUR GITHUB REPOSITORY                          │
│                 (https://github.com/your-username/...)               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                 GitHub detects push to main/develop
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS TRIGGERED                          │
│              (reads .github/workflows/tests.yml)                      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              ┌─────────┐   ┌─────────┐   ┌──────────┐
              │  Python  │   │  Ubuntu │   │  Virtual │
              │  3.12    │   │  Latest │   │ Machine  │
              └─────────┘   └─────────┘   └──────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │  1. Checkout your code from GitHub   │
    │  2. Set up Python 3.12                │
    │  3. Install dependencies (pip install)│
    │  4. Run: pytest automation_framework/ │
    │  5. Generate: reports/report.html     │
    │  6. Upload: pytest-report artifact    │
    └───────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      GITHUB ACTIONS TAB                              │
│              Your workflow shows: ✓ PASSED or ✗ FAILED              │
│              (Artifacts available for download)                      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                    Download report.html
                    View test results in browser
```

---

## 🏗️ Project Structure with Descriptions

```
automation-framework/
│
├── README.md                           ← Main documentation
├── QUICKSTART.md                       ← Quick start guide
├── CI_CD_TROUBLESHOOTING.md           ← Debugging guide
├── requirements.txt                    ← Python dependencies
├── pytest.ini                          ← pytest configuration
├── .gitignore                          ← Files to exclude from git
│
├── .github/
│   └── workflows/
│       └── tests.yml                   ← CI/CD pipeline (GitHub Actions)
│
└── automation_framework/               ← Main framework package
    ├── __init__.py
    │
    ├── config/
    │   └── config.yaml                 ← Environment & browser settings
    │
    ├── conftest.py                     ← pytest fixtures (setup/teardown)
    │
    ├── pages/                          ← Page Object Models (POM)
    │   ├── __init__.py
    │   └── login_page.py               ← Example: Login page actions
    │
    ├── tests/                          ← Test cases
    │   ├── __init__.py
    │   └── test_login.py               ← Example: Login tests
    │
    └── utils/                          ← Helper utilities
        ├── __init__.py
        └── test_data.py                ← Test data (credentials, etc)
```

---

## 🔄 How Each Component Works

### 1. **config.yaml** → Test Configuration
```yaml
base_url: https://example.com          # Target app
browser: chrome                         # Browser type
implicit_wait: 10                       # Wait time (seconds)
headless: false                         # Run with/without UI
report_dir: reports                     # Report output folder
```

**Usage**: Loaded once per test session. Tests read from here instead of hardcoding URLs.

---

### 2. **conftest.py** → Test Setup & Fixtures
```python
@pytest.fixture(scope="function")
def browser(config):
    # Creates a fresh Selenium WebDriver for each test
    # Automatically closes after test completes
    driver = webdriver.Chrome(...)
    yield driver
    driver.quit()  # Cleanup
```

**Usage**: Every test receives a `browser` fixture automatically.

---

### 3. **pages/login_page.py** → Page Object Model
```python
class LoginPage:
    def __init__(self, driver):
        self.username_input = (By.ID, "username")  # Locator stored here
    
    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)
```

**Why POM?** 
- If the login form's HTML changes, update only `login_page.py`
- Tests stay clean and readable
- Locators are defined once, reused everywhere

---

### 4. **tests/test_login.py** → Test Cases
```python
@pytest.mark.smoke
def test_login_with_invalid_credentials(browser, base_url):
    login_page = LoginPage(browser)  # Instantiate POM
    login_page.open(base_url)         # Use fixture
    login_page.enter_username("wrong_user")
    login_page.enter_password("wrong_pass")
    login_page.submit()
    assert "invalid" in login_page.get_error_text()
```

**What's happening?**
- `@pytest.mark.smoke` = Tag for running specific tests
- `browser`, `base_url` = Fixtures injected automatically
- Test focuses on *what to verify*, not *how to find elements*

---

### 5. **utils/test_data.py** → Test Data
```python
def get_credentials(kind="valid"):
    data = {
        "valid": ("user@example.com", "Pass123"),
        "invalid": ("wrong@example.com", "Wrong")
    }
    return data.get(kind)
```

**Why separate?**
- Test data in one place
- Easy to swap sources (hardcoded → JSON → Database)
- Tests don't scatter credentials everywhere

---

### 6. **.github/workflows/tests.yml** → CI/CD Automation
```yaml
on:
  push:
    branches: [ main, develop ]  # Trigger on these branches
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest        # Linux virtual machine
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest automation_framework/tests
      - uses: actions/upload-artifact@v3  # Save report
```

**What happens:**
1. You push code
2. GitHub reads this file
3. Spins up an Ubuntu VM
4. Runs pytest
5. Uploads HTML report as artifact

---

## 🎯 Interaction Diagram: Test Execution

```
User Test (test_login.py)
         │
         ▼
    Create LoginPage object
         │
         ├─ conftest.py provides 'browser' fixture
         │  │
         │  ▼
         │ Selenium WebDriver
         │  │
         │  └─ Opens browser (Chrome)
         │
         ├─ conftest.py provides 'base_url' fixture
         │  │
         │  ▼
         │ config.yaml → https://example.com
         │
         ▼
    LoginPage.open(base_url)
         │
         ├─ Driver navigates to URL
         │
         ▼
    LoginPage.enter_username("user")
         │
         ├─ Finds element by locator in pages/login_page.py
         │  (By.ID, "username")
         │
         ├─ Sends keystrokes
         │
         ▼
    LoginPage.submit()
         │
         ├─ Clicks login button
         │
         ▼
    Assert error message contains "invalid"
         │
         ├─ PASS: Test complete, WebDriver closes
         │ FAIL: Screenshot + error message captured
         │
         ▼
    reports/report.html updated with result
```

---

## 🚀 Adding a New Test

### Step 1: Create a page object (if needed)
```python
# automation_framework/pages/dashboard_page.py
class DashboardPage:
    def __init__(self, driver):
        self.welcome_text = (By.CSS_SELECTOR, ".welcome")
    
    def get_welcome_message(self):
        return self.driver.find_element(*self.welcome_text).text
```

### Step 2: Create a test
```python
# automation_framework/tests/test_dashboard.py
@pytest.mark.smoke
def test_dashboard_shows_welcome(browser, base_url):
    dashboard = DashboardPage(browser)
    dashboard.open(base_url + "/dashboard")
    assert "Welcome" in dashboard.get_welcome_message()
```

### Step 3: Commit and push
```bash
git add automation_framework/pages/dashboard_page.py automation_framework/tests/test_dashboard.py
git commit -m "Add dashboard page and welcome message test"
git push origin main
```

### Step 4: Watch CI/CD
- Go to GitHub → **Actions** tab
- Your new test runs automatically!
- Results appear in the report

---

## 📊 Test Execution Flow (Local vs CI/CD)

### Local Execution
```
pytest automation_framework/tests -v
│
├─ Load config.yaml
├─ Create browser fixture (your Chrome)
├─ Run test_login.py::test_login_with_invalid_credentials
│  ├─ Browser navigates to localhost/example
│  ├─ Enters username/password
│  ├─ Clicks login
│  ├─ Verifies error message
├─ Close browser
├─ Repeat for next test
│
▼
reports/report.html generated
```

### CI/CD Execution
```
GitHub Actions triggered (your push)
│
├─ Checkout code
├─ Install Python 3.12
├─ pip install -r requirements.txt
├─ Load config.yaml
├─ Create browser fixture (Ubuntu's Chrome/Chromium)
├─ Run ALL tests in automation_framework/tests/
│  ├─ test_login.py::test_login_with_invalid_credentials
│  ├─ test_login.py::test_login_success (if added)
│  └─ All other tests...
├─ Close browsers
│
▼
reports/report.html uploaded as artifact
│
▼
You download & review results
```

---

## ✅ Verification Checklist

After pushing code:

- [ ] Go to GitHub repo → **Actions** tab
- [ ] See your workflow in the list
- [ ] Click workflow → see job execution logs
- [ ] Job shows **green checkmark** (all tests passed) or **red X** (failure)
- [ ] Scroll to **Artifacts** → download **pytest-report**
- [ ] Extract ZIP and open `report.html` in browser
- [ ] View detailed results: test names, status, execution time

---

## 🎓 Interview Talking Points

When discussing this framework in an interview:

1. **"I built a scalable test automation framework using Page Object Model"**
   - Show the pages/ and tests/ structure

2. **"I separated concerns: config, fixtures, page objects, and tests"**
   - Explain each component's responsibility

3. **"I implemented CI/CD using GitHub Actions"**
   - Show the .github/workflows/tests.yml
   - Explain how tests run automatically on every push

4. **"I created comprehensive documentation for team onboarding"**
   - Point to README.md, QUICKSTART.md

5. **"The framework is easily extensible"**
   - Show how simple it is to add new tests (just follow the pattern)

6. **"I used pytest markers to organize tests by type (smoke, regression)"**
   - Show @pytest.mark.smoke examples

7. **"I integrated with CI/CD for continuous testing and early bug detection"**
   - Explain the workflow trigger and artifact generation
