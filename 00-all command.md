خیلی عالی توضیح دادی! من هم برای هر کدوم از مواردی که گفتی یه توضیح دقیق‌تر همراه با مثال YAML در فایل `.gitlab-ci.yml` می‌دم تا بهتر جا بیفته:

---

### ✅ `retry`

وقتی بخوایم یه job رو در صورت خطا (مثلاً خطای شبکه‌ای یا timeout) چندبار تکرار کنیم.

**توضیح:**
تعداد دفعاتی که GitLab Runner سعی می‌کنه یک job ناموفق رو دوباره اجرا کنه. مقدار پیش‌فرض `0` هست.

**مثال:**

```yaml
build:
  script: echo "Trying to build..."
  retry: 2
```

یعنی اگه job `build` fail بشه، دو بار دیگه هم تلاش می‌کنه اجراش کنه.

---

### ✅ `parallel`

برای اجرای موازی یک job استفاده میشه، مثلاً وقتی بخوایم یه تست روی چند محیط مختلف به طور همزمان اجرا شه.

**توضیح:**
یک job رو به تعداد مشخصی instance موازی اجرا می‌کنه.

**مثال:**

```yaml
test:
  script: echo "Running test"
  parallel: 3
```

یعنی job `test` سه بار به صورت هم‌زمان اجرا میشه (با index متفاوت: 0، 1، 2).

> ❗ برای اینکه درست کار کنه باید یا چند runner داشته باشی یا runner تکی قابلیت اجرای موازی داشته باشه (`concurrent` بالا در تنظیمات runner).

---

### ✅ `timeout`

برای اینکه job تو یه مدت زمان خاص تموم شه، وگرنه fail بشه.

**توضیح:**
اگه job بیشتر از مدت زمان مشخص‌شده طول بکشه، fail میشه.

**مثال:**

```yaml
long_job:
  script: sleep 120
  timeout: 1m
```

یعنی اگر job بیشتر از 1 دقیقه طول بکشه، fail میشه، حتی اگه هنوز `sleep` ادامه داشته باشه.

> ⚠ باید مطمئن باشی که این مقدار از `runner timeout` کمتر باشه.

---

### ✅ `trigger`

برای اجرای یک pipeline دیگه از داخل این pipeline استفاده میشه.

**توضیح:**
می‌تونی یه pipeline تو یه پروژه دیگه یا همین پروژه رو با `trigger` اجرا کنی.

**مثال برای child pipeline:**

```yaml
trigger_job:
  trigger:
    include: .child-pipeline.yml
    strategy: depend
```

**مثال برای multi-project pipeline:**

```yaml
deploy:
  trigger:
    project: group/another-project
    branch: main
```

---

### ✅ `variables`

برای تعریف متغیرهایی که در job استفاده می‌کنیم.

**توضیح:**
با استفاده از `variables` می‌تونی مقدارهایی مثل نام فایل، ورژن، مسیر و غیره رو تعریف و استفاده کنی.

**مثال:**

```yaml
variables:
  APP_ENV: production

deploy:
  script:
    - echo "Deploying to $APP_ENV"
```

---

### ✅ `when`

کنترل اینکه چه زمانی یک job اجرا بشه.

#### حالت‌های مختلف:

1. **`on_success` (پیش‌فرض):**
   فقط اگه jobهای استیج قبل موفق بودن اجرا میشه.

   ```yaml
   job:
     script: echo "OK"
     when: on_success
   ```

2. **`manual`:**
   فقط وقتی کاربر دستی اجراش کنه.

   ```yaml
   deploy_production:
     script: deploy.sh
     when: manual
   ```

3. **`always`:**
   بدون توجه به موفق یا fail بودن jobهای قبلی اجرا میشه.

   ```yaml
   notify:
     script: notify.sh
     when: always
   ```

4. **`on_failure`:**
   فقط اگه jobهای استیج قبل fail شده باشن.

   ```yaml
   recover:
     script: fix.sh
     when: on_failure
   ```

5. **`delayed`:**
   اجرای job رو با تاخیر انجام میده.

   ```yaml
   delayed_job:
     script: echo "Starting late..."
     when: delayed
     start_in: 10 minutes
   ```

6. **`never`:**
   job هیچ وقت اجرا نمیشه (معمولاً در `workflow: rules` استفاده میشه).

   ```yaml
   job:
     script: echo "Never runs"
     when: never
   ```

---



خیلی عالی و کامل پرسیدی! حالا برات تمام این موارد رو **با توضیح + مثال YAML ساده** می‌نویسم تا راحت تو فایل `.gitlab-ci.yml` بتونی استفاده کنی:

---

## ✅ 1. `workflow`

برای کنترل کلی اینکه یک **pipeline اجرا بشه یا نه** از `workflow:` استفاده می‌کنیم.

### 📌 مثال:

```yaml
workflow:
  rules:
    - if: '$CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/'
      when: always
    - when: never
```

🔍 **توضیح:** اگر تگ به فرمت `v1.2.3` بود pipeline اجرا می‌شه، وگرنه اصلاً pipeline اجرا نمی‌شه.

---

## ✅ 2. `environments` و `deployments`

برای مشخص کردن جایی که کد deploy میشه از `environment` استفاده می‌کنیم.

### 📌 مثال:

```yaml
deploy_to_production:
  stage: deploy
  script:
    - ./deploy.sh
  environment:
    name: production
    url: https://example.com
```

🔍 **توضیح:** این باعث می‌شه تو GitLab UI یک محیط به نام "production" نمایش داده بشه که تاریخچه‌ی دیپلوی‌ها، قابلیت rollback و rollout داره.

---

## ✅ 3. `artifacts`

برای اینکه خروجی یک job (مثل فایل یا پوشه) به job بعدی منتقل بشه.

### 📌 مثال:

```yaml
build:
  script:
    - make build
  artifacts:
    paths:
      - build/

test:
  script:
    - run_tests build/
```

🔍 **توضیح:** دایرکتوری `build/` که توسط job اول تولید شده، به job دوم منتقل میشه.

---

## ✅ 4. `dependencies`

کنترل می‌کنه که **فقط آرتیفکت‌های خاصی** از job‌های قبل بیاد.

### 📌 مثال:

```yaml
job_a:
  script: generate_a
  artifacts:
    paths: [a.txt]

job_b:
  script: generate_b
  artifacts:
    paths: [b.txt]

job_c:
  script: use_files
  dependencies:
    - job_b
```

🔍 **توضیح:** `job_c` فقط آرتیفکت‌های `job_b` رو می‌بینه، نه `job_a`.

---

## ✅ 5. `cache`

برای ذخیره‌ی چیزایی مثل پکیج‌ها یا وابستگی‌ها بین jobها.

### 📌 مثال:

```yaml
install_deps:
  script:
    - npm install
  cache:
    paths:
      - node_modules/
```

🔍 **توضیح:** پوشه `node_modules/` کش میشه، پس دفعات بعدی سریع‌تر اجرا میشه.

---

## ✅ 6. `tags`

برای مشخص کردن job روی کدوم runner اجرا بشه.

### 📌 مثال:

```yaml
build:
  script: make
  tags:
    - docker
    - high-cpu
```

🔍 **توضیح:** فقط روی runnerهایی اجرا میشه که این تگ‌ها رو دارن.

---

## ✅ 7. `only` / `except`

برای کنترل اینکه job در چه شرایطی اجرا بشه.

### 📌 مثال:

```yaml
test:
  script: npm test
  only:
    - main

deploy:
  script: ./deploy.sh
  except:
    - schedules
```

🔍 **توضیح:** `test` فقط روی branch `main` اجرا میشه و `deploy` در اجرای زمان‌بندی‌شده (`schedule`) اجرا نمی‌شه.

---

## ✅ 8. `extends`

برای تمیز نگه داشتن config و استفاده‌ی مجدد از templateها.

### 📌 مثال:

```yaml
.default_job:
  script: echo "Default"
  image: node:18

job1:
  extends: .default_job
  script: echo "Job 1"

job2:
  extends: .default_job
```

---

## ✅ 9. `coverage`

برای مشخص کردن pattern کاورج گزارش‌شده توسط تست‌ها.

### 📌 مثال:

```yaml
test:
  script: npm run test
  coverage: '/All files\s*\|\s*\d+%/'
```

🔍 **توضیح:** GitLab خروجی تست رو می‌خونه و میزان coverage رو نمایش می‌ده.

---

## ✅ 10. `rules`

جایگزین بهتر `only/except` با کنترل بیشتر.

### 📌 مثال:

```yaml
job:
  script: run
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
    - when: never
```

---

## ✅ 11. `release`

برای ساخت release اتوماتیک از پروژه.

### 📌 مثال:

```yaml
release_job:
  script: echo "Release created"
  release:
    tag_name: v1.0.0
    description: 'First release'
```

---

## ✅ 12. `inherit`

برای مدیریت ارث‌بری jobها از config بالا یا default.

### 📌 مثال:

```yaml
job_without_login:
  script: echo "skip login"
  inherit:
    default: false
```

---

## ✅ 13. `interruptible`

برای لغو pipeline قبلی وقتی یه commit جدید میاد.

### 📌 مثال:

```yaml
build:
  script: make build
  interruptible: true
```

---

## ✅ 14. `manual_confirmation`

برای دادن پیام به کاربر در زمان اجرای دستی.

### 📌 مثال:

```yaml
deploy_prod:
  script: ./deploy.sh
  when: manual
  allow_failure: false
  environment:
    name: production
    action: start
  trigger:
    manual_confirmation:
      prompt: "آیا مطمئنی می‌خوای تو پروداکشن دیپلوی کنی؟"
```

---

## ✅ 15. `resource_group`

برای اینکه jobهایی که به منابع یکسانی دسترسی دارند با هم overlap نکنن.

### 📌 مثال:

```yaml
deploy_prod:
  script: ./deploy.sh
  resource_group: production
```

---

## ✅ 16. `identity`

برای احراز هویت با identity providerها، در contextهای خاص مثل access به cloud.

🔸 استفاده‌ی ساده‌ش در GitLab CI زیاد رایج نیست و بیشتر با تنظیمات پیشرفته GitLab SaaS یا Kubernetes سروکار داره.

---

## ✅ 17. `pages`

برای راه‌اندازی سایت استاتیک (مثل بلاگ، مستندات، پروژه شخصی و غیره).

### 📌 مثال:

```yaml
pages:
  stage: deploy
  script:
    - mkdir .public
    - echo "Hello GitLab Pages!" > .public/index.html
    - mv .public public
  artifacts:
    paths:
      - public
```

---
