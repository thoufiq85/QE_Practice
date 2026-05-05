# Local Testing Troubleshooting

If pytest fails locally, try these steps:

1. **Check Chrome Installation**
   - Ensure Google Chrome is installed on your system
   - Chrome version should be compatible with ChromeDriver

2. **Run Basic Chrome Test**
   ```bash
   python -c "
   from selenium import webdriver
   from selenium.webdriver.chrome.options import Options
   options = Options()
   options.add_argument('--headless')
   driver = webdriver.Chrome(options=options)
   driver.get('https://www.google.com')
   print('Chrome works!')
   driver.quit()
   "
   ```

3. **Check Environment Variables**
   - Ensure `CI` environment variable is not set locally
   - Run: `echo $CI` (should be empty)

4. **Update ChromeDriver**
   ```bash
   pip install --upgrade webdriver-manager
   ```

5. **Run with Debug Info**
   ```bash
   pytest automation_framework/tests -v -s --tb=long
   ```

6. **Check Python Path**
   - Ensure you're running from the project root directory
   - Check that all imports work: `python -c "import automation_framework.conftest"`

7. **Alternative: Run the debug script**
   ```bash
   python test_local_setup.py
   ```</content>
<parameter name="filePath">c:\Users\Mohammed Thoufiq\Desktop\Resume\RBC\QE\P\QE_Practice\LOCAL_DEBUG.md