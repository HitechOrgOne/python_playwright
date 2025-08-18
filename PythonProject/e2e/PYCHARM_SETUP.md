# PyCharm Setup Guide for E2E Testing Framework

## Quick Fix for Import Errors

### Method 1: Mark Directory as Sources Root (Recommended)

1. **Right-click on the `e2e` folder** in PyCharm project explorer
2. **Select "Mark Directory as" → "Sources Root"**
3. **Restart PyCharm** for changes to take effect

### Method 2: Manual Project Structure Configuration

1. Go to **File → Settings** (or **PyCharm → Preferences** on Mac)
2. Navigate to **Project → Project Structure**
3. Select the **`e2e` folder**
4. Click **"Sources"** button to mark it as source root
5. Click **Apply** and **OK**
6. **Restart PyCharm**

### Method 3: Add Content Root

1. Go to **File → Settings → Project → Project Structure**
2. Click **"+ Add Content Root"**
3. Select your **`e2e` directory**
4. **Apply** and **OK**

## Verify Setup

After setup, check that imports work:

```python
# These should work without errors:
from pages.login_page import LoginPage
from utils.file_utils import FileUtils
```

## Running Tests from PyCharm

1. Right-click on `test_login.py`
2. Select **"Run 'pytest in test_login.py'"**
3. Or use the green arrow buttons next to test methods

## Running Tests from Terminal

```bash
cd e2e
pytest tests/ -v
```
