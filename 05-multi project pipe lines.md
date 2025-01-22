در GitLab، **Multi-Project Pipeline** یا خط لوله چند پروژه‌ای، زمانی استفاده می‌شود که می‌خواهید خط لوله یک پروژه به اجرای خط لوله پروژه دیگری وابسته باشد یا آنها با هم تعامل داشته باشند. این معمولاً در پروژه‌هایی که وابستگی‌هایی بین ماژول‌ها، میکروسرویس‌ها یا مخازن وجود دارد، بسیار مفید است.

### مثال ساده از Multi-Project Pipeline

فرض کنید:
1. **پروژه A**: حاوی کد اصلی یک اپلیکیشن.
2. **پروژه B**: مسئول ساخت و انتشار Docker Image برای اپلیکیشن.

حالا می‌خواهیم خط لوله پروژه A، خط لوله پروژه B را پس از موفقیت خود فراخوانی کند.

---

### تنظیم فایل `.gitlab-ci.yml` در پروژه A

```yaml
stages:
  - build
  - trigger_b

build_project_a:
  stage: build
  script:
    - echo "Building Project A..."
    - sleep 2

trigger_project_b_pipeline:
  stage: trigger_b
  trigger:
    project: "namespace/project-b"  # مسیر پروژه B
    branch: main                   # برنچی که باید در پروژه B اجرا شود
    strategy: depend               # اجرای وابسته به موفقیت مراحل قبلی
```

---

### تنظیم فایل `.gitlab-ci.yml` در پروژه B

```yaml
stages:
  - build
  - deploy

build_project_b:
  stage: build
  script:
    - echo "Building Project B..."
    - sleep 2

deploy_project_b:
  stage: deploy
  script:
    - echo "Deploying Project B..."
    - sleep 2
```

---

### توضیحات:
1. در **پروژه A**، مرحله `trigger_project_b_pipeline` خط لوله پروژه B را با استفاده از دستور `trigger` فراخوانی می‌کند.
2. کلید `strategy: depend` مشخص می‌کند که خط لوله پروژه B تنها در صورت موفقیت‌آمیز بودن مراحل پروژه A اجرا می‌شود.
3. در **پروژه B**، خط لوله شامل مراحل استاندارد Build و Deploy است.

---

### کاربردهای متداول:
- اجرای خط لوله یک پروژه وابسته به دیگری (مانند Build در یک پروژه و Deploy در پروژه دیگر).
- مدیریت وابستگی‌ها بین میکروسرویس‌ها.
- هماهنگ‌سازی خطوط لوله در پروژه‌های بزرگ.

### نکات:
- اطمینان حاصل کنید که **پروژه A** دسترسی کافی (مانند Access Token) برای اجرای خط لوله پروژه B دارد.
- برای امنیت بیشتر، از **Trigger Tokens** برای کنترل اجرای خطوط لوله استفاده کنید.
