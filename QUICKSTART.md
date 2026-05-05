# Quick Start Guide for SDET Automation Framework

## 1. Initial Setup (One-time)

### Clone the Repository
```bash
git clone https://github.com/yourusername/automation-framework.git
cd automation-framework
```

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Your Target App
Edit `automation_framework/config/config.yaml` and update `base_url`:
```yaml
base_url: https://your-application-url.com
```

---

## 2. Running Tests Locally

### Run all tests
```bash
pytest automation_framework/tests -v
```

### Run with HTML report
```bash
pytest automation_framework/tests -v --html=reports/report.html --self-contained-html
```

### Run only smoke tests
```bash
pytest automation_framework/tests -v -m smoke
```

### Run a specific test file
```bash
pytest automation_framework/tests/test_login.py -v
```

### Run a specific test
```bash
pytest automation_framework/tests/test_login.py::test_login_with_invalid_credentials -v
```

---

## 3. Pushing to GitHub & Watching CI/CD

### Commit and Push
```bash
git add .
git commit -m "My changes"
git push origin main
```

### Watch CI/CD Execute
1. Go to your GitHub repo: `https://github.com/yourusername/automation-framework`
2. Click **Actions** tab
3. You should see your workflow running
   - **Yellow icon** = Running
   - **Green checkmark** = Passed
   - **Red X** = Failed
4. Click the workflow to see detailed logs
5. Scroll to "Artifacts" to download the HTML test report

---

## 4. Common Commands

### Activate/Deactivate Virtual Environment
```bash
# Windows
venv\Scripts\activate  # Activate
deactivate             # Deactivate

# macOS/Linux
source venv/bin/activate  # Activate
deactivate                # Deactivate
```

### Update Dependencies
```bash
pip freeze > requirements.txt
```

### See All Available pytest Markers
```bash
pytest --markers
```

### Run tests in verbose debug mode
```bash
pytest automation_framework/tests -vv -s
```

---

## 5. Understanding Test Results

After running tests, check `reports/report.html` for:
- **Test name and status** (passed/failed)
- **Execution time** per test
- **Error stack trace** (if test failed)
- **Screenshots** (if captured on failure)

---

## 6. What Happens in CI/CD

When you `git push`:
1. GitHub detects the push to `main` branch
2. GitHub Actions workflow (`tests.yml`) is triggered
3. A virtual machine spins up (Ubuntu)
4. Python and dependencies are installed
5. All tests run automatically
6. HTML report is generated and uploaded as an artifact
7. You can download and review the report

---

## 7. Next Steps

- Add more page objects to `automation_framework/pages/`
- Add more tests to `automation_framework/tests/`
- Create markers (`@pytest.mark.regression`, etc.) for organizing tests
- Add test data to `automation_framework/utils/`
- Integrate with JIRA/qTest for automated reporting

Follow the existing pattern and your tests will automatically run in CI/CD! 🎯
