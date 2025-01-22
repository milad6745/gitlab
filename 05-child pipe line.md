**Child Pipeline** در GitLab به شما امکان می‌دهد تا خط لوله‌های پیچیده و قابل مدیریت‌تری ایجاد کنید. با استفاده از **Child Pipeline**، می‌توانید یک خط لوله را به بخش‌های کوچکتر تقسیم کنید که هر بخش در فایل `.gitlab-ci.yml` جداگانه تعریف می‌شود.

---

### سناریو: تقسیم خط لوله به والد و فرزند
فرض کنید:
- یک پروژه داریم که دو مرحله دارد: **Build** و **Test**.
- مرحله Build در خط لوله اصلی (Parent Pipeline) تعریف شده است.
- مرحله Test در یک خط لوله فرزند (Child Pipeline) اجرا می‌شود.

---

### فایل `.gitlab-ci.yml` در خط لوله والد (Parent Pipeline)

```yaml
stages:
  - build
  - trigger_child

build:
  stage: build
  script:
    - echo "Building the application..."
    - sleep 2

trigger_child_pipeline:
  stage: trigger_child
  trigger:
    include:
      - local: 'child-pipeline.yml'  # اشاره به فایل خط لوله فرزند
    strategy: depend  # اجرای خط لوله فرزند وابسته به موفقیت خط لوله والد است
```

---

### فایل `child-pipeline.yml` در خط لوله فرزند

```yaml
stages:
  - test

test:
  stage: test
  script:
    - echo "Running tests..."
    - sleep 2
    - echo "Tests completed successfully!"
```

---

### توضیحات:
1. **Parent Pipeline**:
   - مرحله `trigger_child_pipeline` از کلید `trigger` و `include` استفاده می‌کند تا فایل `child-pipeline.yml` را به عنوان خط لوله فرزند فراخوانی کند.
   - کلید `strategy: depend` تضمین می‌کند که اگر خط لوله والد شکست بخورد، خط لوله فرزند اجرا نمی‌شود.

2. **Child Pipeline**:
   - فایل `child-pipeline.yml` شامل مرحله `test` است که تست‌ها را اجرا می‌کند.

---

### مزایا:
- خط لوله‌های قابل مدیریت‌تر: تقسیم خط لوله به والد و فرزند، نگهداری و توسعه را آسان‌تر می‌کند.
- انعطاف‌پذیری: می‌توانید خطوط لوله فرزند را بر اساس نیازهای خاص پروژه تغییر دهید.
- وابستگی منطقی: خط لوله فرزند فقط در صورت موفقیت خط لوله والد اجرا می‌شود.

---

### نکات:
- فایل فرزند (`child-pipeline.yml`) باید در مخزن موجود باشد.
- مطمئن شوید که ساختار فایل‌ها و مسیرها درست است.
- از ابزارهای GitLab مانند **Pipeline Editor** برای تست و بررسی خط لوله استفاده کنید.
