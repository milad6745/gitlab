بله، من می‌تونم برات یه اسکریپت ساده پایتون بنویسم و با استفاده از pytest برای تست در GitLab آماده کنم. اینجا یک مثال ساده دارم که می‌تونی ازش استفاده کنی.

### 1. **ایجاد اسکریپت پایتون:**

اول یه فایل پایتون می‌سازیم، مثلاً به اسم `calculator.py` که یه تابع ساده به نام `add` رو داخلش می‌نویسیم.

```python
# calculator.py

def add(a, b):
    return a + b
```

### 2. **ایجاد تست با pytest:**

حالا باید یه فایل تست بنویسیم که با pytest این تابع رو تست کنه.

```python
# test_calculator.py

from calculator import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### 3. **پیکربندی GitLab CI:**

برای اینکه تست‌ها توی GitLab اجرا بشه، باید یه فایل به اسم `.gitlab-ci.yml` بسازی که تنظیمات مربوط به اجرای pytest رو انجام بده.

```yaml
# .gitlab-ci.yml

stages:
  - test

test:
  image: python:3.9
  stage: test
  script:
    - pip install pytest
    - pytest --maxfail=1 --disable-warnings -q
```

### 4. **چطور کار می‌کنه؟**

1. **اسکریپت پایتون** (`calculator.py`) تابع `add` رو تعریف می‌کنه.
2. **فایل تست** (`test_calculator.py`) تست‌هایی رو برای این تابع می‌نویسه که اگر خروجی تابع درست نباشه، خطا بده.
3. **GitLab CI** با استفاده از فایل `.gitlab-ci.yml` محیطی رو برای اجرای pytest فراهم می‌کنه و تست‌ها رو اجرا می‌کنه.

### 5. **مراحل اجرا در GitLab:**

1. فایل‌های پایتون و تست رو به رپازیتوری GitLab خودت اضافه کن.
2. فایل `.gitlab-ci.yml` رو هم توی رپازیتوری بذار.
3. بعد از commit کردن تغییرات، GitLab به طور خودکار مراحل CI رو اجرا می‌کنه و نتایج تست‌ها رو نشون می‌ده.

اینطور می‌تونی با استفاده از pytest توی GitLab تست‌های پایتون رو اجرا کنی.
