## test with Flake8

app.py
```
# app.py

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
```

ب

### فایل `.gitlab-ci.yml`:

```yaml
stages:
  - test

lint_test:
  image: python:3.8-slim
  stage: test
  before_script:
    - pip install flake8-html
  script:
    - flake8 --format=html --htmldir=flake_reports/
  artifacts:
    when: always
    paths:
      - flake_reports/
```

### توضیحات:
 **stages:**
   - مرحله `test` تعریف شده است که شامل اجرای linting خواهد بود.

 **lint_test:**

 
   - **image:**
   -
   -   از تصویر سبک `python:3.8-slim` برای اجرای این مرحله استفاده می‌شود.
   - **before_script:**
   -
   - پیش از اجرای اسکریپت، `flake8-html` نصب می‌شود.
   - **script:**
   -
   - دستور `flake8` اجرا می‌شود تا کد را بررسی کند و گزارش را به صورت HTML در دایرکتوری `flake_reports/` ذخیره کند.
     - `--format=html`: فرمت خروجی را به HTML تغییر می‌دهد.
     - `--htmldir=flake_reports/`: مسیر ذخیره گزارش HTML را مشخص می‌کند.
   - **artifacts:** 
     - **when: always:**
     -
     - گزارش HTML همیشه به عنوان artifact ذخیره می‌شود، حتی اگر linting با خطا مواجه شود.
     - **paths:**
     -
     - مسیر دایرکتوری `flake_reports/` که شامل گزارش HTML است، به عنوان artifact ذخیره می‌شود.
