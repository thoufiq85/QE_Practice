# CI/CD Troubleshooting & FAQ

## ❓ FAQ

### Q: I pushed code but the CI/CD pipeline didn't run
**A:** Check:
1. Did you push to `main` or `develop` branch? (The workflow only triggers on these)
2. Is the `.github/workflows/tests.yml` file committed and on GitHub?
3. Go to your repo's **Actions** tab – do you see any workflow runs listed?
4. If nothing appears after 5 seconds, refresh the page

---

### Q: My workflow shows a red X (failed), how do I debug?
**A:** 
1. Click on the failed workflow
2. Click on the **test** job
3. Look for which step failed (e.g., "Run tests")
4. Read the error message – it tells you exactly what went wrong
5. Common issues:
   - **Dependency missing**: Add to `requirements.txt` and re-push
   - **Test failed**: Check the test logic, run it locally first
   - **Invalid YAML syntax**: Check `.github/workflows/tests.yml` for indentation errors

---

### Q: My tests pass locally but fail in CI/CD
**A:** Likely causes:
1. **Different environment**: CI uses Linux, you use Windows/Mac. Some Selenium drivers behave differently.
2. **Missing test data**: Test data file not committed to GitHub
3. **URL issue**: `base_url` in `config.yaml` is hardcoded but invalid in CI
   - **Solution**: Use environment variables in GitHub Actions
4. **Timing issues**: Increase implicit waits in `config.yaml`

---

### Q: How do I see the test report in CI/CD?
**A:**
1. Go to your GitHub repo → **Actions** tab
2. Click on the workflow run
3. Scroll down to **Artifacts** section
4. Download **pytest-report** (ZIP file)
5. Extract and open `report.html` in your browser

---

### Q: Can I run tests on multiple Python versions?
**A:** Yes! Modify `.github/workflows/tests.yml`:

```yaml
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11, 3.12]

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

This runs your tests on 4 different Python versions automatically.

---

## 🔧 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'selenium'"
**Cause:** Dependencies not installed in CI  
**Solution:** Ensure `selenium` is in `requirements.txt` and commit it

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

---

### Issue 2: "WebDriver not found" or "chromedriver not found"
**Cause:** CI doesn't have Chrome browser or webdriver installed  
**Solution:** Modify `tests.yml` to install dependencies:

```yaml
- name: Install Chrome
  run: |
    sudo apt-get update
    sudo apt-get install -y chromium-browser
```

Or use headless mode in `config.yaml`:
```yaml
headless: true
```

---

### Issue 3: Test hangs or times out in CI
**Cause:** Implicit waits too long or test waiting for user interaction  
**Solution:**
1. Add timeout to the workflow step:
```yaml
- name: Run tests
  timeout-minutes: 10
  run: pytest automation_framework/tests -v
```

2. Or reduce waits in `config.yaml`:
```yaml
implicit_wait: 5  # Lower from 10
```

---

### Issue 4: YAML indentation error in workflow file
**Error:** `Error: Invalid YAML`  
**Solution:** 
- YAML requires **spaces, not tabs**
- Each indentation level = 2 spaces
- Use an online YAML validator: https://www.yamllint.com/
- Paste your `.github/workflows/tests.yml` to validate

---

## 📊 Monitoring & Optimization

### Set up email notifications
1. Go to your GitHub repo → **Settings**
2. Click **Notifications** → configure email alerts for workflow failures

### Add a workflow status badge to README
Add this to the top of your `README.md`:

```markdown
[![Tests](https://github.com/yourusername/automation-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/automation-framework/actions)
```

Your README will show a live status badge (green = passing, red = failing)

### View workflow run history
- Go to **Actions** tab
- Click **Run Automation Tests** workflow
- See all runs with timestamps and status

---

## 🚀 Advanced: Conditional Execution

### Run tests only on certain conditions

**Run only on pull requests (not pushes):**
```yaml
on:
  pull_request:
    branches: [ main ]
```

**Run on schedule (e.g., every night at 2 AM):**
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
```

**Run only when specific files change:**
```yaml
on:
  push:
    paths:
      - 'automation_framework/**'
      - 'requirements.txt'
```

---

## 📝 Best Practices

1. **Commit `requirements.txt`** – Always keep dependencies tracked
2. **Use `.gitignore`** – Don't commit `venv/`, `__pycache__/`, or `reports/`
3. **Test locally first** – Before pushing to GitHub
4. **Review logs** – When CI fails, read the logs carefully
5. **Keep workflows simple** – Start basic, add complexity later
6. **Document your setup** – Help team members get running quickly

---

## 🆘 Need More Help?

- **GitHub Actions docs**: https://docs.github.com/en/actions
- **pytest docs**: https://docs.pytest.org/
- **Selenium docs**: https://selenium.dev/documentation/
- **YAML syntax**: https://yaml.org/
