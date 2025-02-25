
# artifact

در GitLab، artifact به فایل‌هایی اطلاق می‌شود که در طول فرایند CI/CD (Continuous Integration / Continuous Delivery) تولید می‌شوند و به عنوان نتایج یک job ذخیره می‌شوند. این فایل‌ها می‌توانند شامل مواردی مثل فایل‌های خروجی، لاگ‌ها، یا هر چیزی باشند که به عنوان نتیجه‌ی یک task تولید می‌شود و ممکن است در مراحل بعدی مورد نیاز باشد.

به طور معمول، از artifacts برای ذخیره‌سازی فایل‌هایی مانند:

فایل‌های ساخته شده در طول فرایند build
گزارش‌های تست‌ها
بسته‌های نرم‌افزاری تولید شده

gitlab-ci.yml
```
lint:
  stage: lint
  image: python:3.8
  script:
    - pip install flake8
    - flake8 main.py --output-file=flake8-report.txt
  artifacts:
    paths:
      - flake8-report.txt
    expire_in: 1 week
```

main.py
```
def say_hello():

    print("Hello, World!")


say_hello()

```

- در یک stage میتوانند از Artifact ]ای جاب های دیگه استفاده کنند
- نمیشود Artifact ها را در بین پروژه های مختلف شیر کرد
- عمرشون 30 روزه
- آخرین آرتیفکت latest منقضی نمیشوند
- 
- 
