## pipe line

در GitLab CI/CD، سه مفهوم اصلی وجود دارد که فرآیند ساخت، تست، و استقرار نرم‌افزار را تعریف می‌کنند: **Pipeline**، **Stage** و **Job**. هر کدام از این مفاهیم نقش مهمی در ساختاردهی و اجرای فرآیند CI/CD دارند. در ادامه به توضیحات هر یک از این مفاهیم می‌پردازیم:

### 1. Pipeline


مجموعه‌ای از مراحل (stages) است که به ترتیب اجرا می‌شوند تا فرآیند ساخت، تست و استقرار نرم‌افزار را تکمیل کنند. هر pipeline معمولاً با هر تغییر یا push به مخزن کد، اجرا می‌شود. pipeline می‌تواند شامل چندین stage باشد و هر stage می‌تواند شامل چندین job باشد.

**مثال:**
فرض کنید یک pipeline ساده به صورت زیر است:
- **Build**: ساختن کد.
- **Test**: اجرای تست‌ها.
- **Deploy**: استقرار نرم‌افزار.

### 2. Stage


یک مرحله خاص در pipeline است که مجموعه‌ای از jobها را شامل می‌شود. تمامی jobهای موجود در یک stage به طور موازی اجرا می‌شوند. pipeline به ترتیب مراحل مختلف را اجرا می‌کند، یعنی تا زمانی که همه jobهای یک stage به پایان نرسند، مرحله بعدی شروع نمی‌شود.

**مثال:**
- **build**: شامل jobهای کامپایل و ساخت کد.
- **test**: شامل jobهای اجرای تست‌های واحد و تست‌های یکپارچه‌سازی.
- **deploy**: شامل jobهای استقرار در محیط‌های مختلف.

### 3. Job

 یک کار واحد است که در یک stage خاص اجرا می‌شود. هر job می‌تواند شامل دستوراتی باشد که باید در محیط runner اجرا شود. jobها وظایف مشخصی مانند ساخت، تست یا استقرار کد را انجام می‌دهند. یک stage می‌تواند شامل چندین job باشد که به صورت موازی اجرا می‌شوند.
 

**مثال:**
- **compile_code**: jobی در stage build که کد را کامپایل می‌کند.
- **run_unit_tests**: jobی در stage test که تست‌های واحد را اجرا می‌کند.
- **deploy_to_staging**: jobی در stage deploy که کد را در محیط staging مستقر می‌کند.

### نحوه تعریف Pipeline، Stage و Job در GitLab CI/CD
این مفاهیم در فایل `.gitlab-ci.yml` تعریف می‌شوند. در زیر یک مثال ساده آورده شده است:

```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."
    - make build

unit_test_job:
  stage: test
  script:
    - echo "Running unit tests..."
    - make test

integration_test_job:
  stage: test
  script:
    - echo "Running integration tests..."
    - make integration_test

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - make deploy
```
- **deploy_job**:
-
-   jobی در stage deploy که دستورات استقرار را اجرا می‌کند.

با استفاده از این ساختار، GitLab CI/CD می‌تواند فرآیندهای ساخت، تست و استقرار نرم‌افزار شما را به صورت اتوماتیک و قابل تکرار اجرا کند.


## Type of pipeline


در GitLab CI/CD، انواع مختلفی از pipelines وجود دارند که هر کدام برای اهداف و سناریوهای خاصی طراحی شده‌اند. این انواع شامل موارد زیر هستند:

### 1. **Basic Pipeline**
این نوع pipeline ساده‌ترین نوع است و شامل مراحل (stages) و jobهایی است که به ترتیب مشخص شده اجرا می‌شوند. این نوع برای فرآیندهای ساده ساخت، تست و استقرار استفاده می‌شود.

### 2. **Multi-project Pipeline**
این نوع pipeline به شما امکان می‌دهد که یک pipeline را به پروژه‌های دیگر در GitLab متصل کنید و jobهای مربوط به چندین پروژه را به صورت هماهنگ اجرا کنید. این نوع pipeline برای سازمان‌های بزرگ که پروژه‌های مرتبط متعددی دارند، مفید است.

### 3. **Child Pipeline**
این نوع pipeline به شما امکان می‌دهد که یک pipeline را از درون یک pipeline دیگر فراخوانی کنید. این روش به مدیریت بهتر و سازمان‌دهی بهتر jobها کمک می‌کند و می‌تواند به تقسیم یک pipeline پیچیده به چندین pipeline کوچک‌تر و قابل مدیریت‌تر کمک کند.

### 4. **Trigger Pipeline**
این نوع pipeline به شما اجازه می‌دهد که یک pipeline را به صورت دستی یا به وسیله یک webhook یا API trigger کنید. این قابلیت به شما امکان می‌دهد که pipelineها را در شرایط خاص یا بر اساس رویدادهای خاص اجرا کنید.

### 5. **Scheduled Pipeline**
این نوع pipeline به شما امکان می‌دهد که pipelineها را بر اساس یک زمانبندی مشخص اجرا کنید. می‌توانید یک job را به صورت روزانه، هفتگی یا در هر بازه زمانی دلخواه اجرا کنید. این نوع pipeline برای کارهایی که نیاز به اجرای دوره‌ای دارند، مناسب است.

### 6. **Merge Request Pipeline**
این نوع pipeline به صورت خودکار برای هر merge request جدید اجرا می‌شود. این pipeline به شما کمک می‌کند تا قبل از ادغام تغییرات در شاخه اصلی (main branch)، مطمئن شوید که کد به درستی کار می‌کند و تمامی تست‌ها پاس شده‌اند.

### 7. **Branch Pipeline**
این نوع pipeline برای هر شاخه (branch) خاص اجرا می‌شود. می‌توانید pipelineهای مختلفی را برای شاخه‌های مختلف پروژه تنظیم کنید، مثلاً یک pipeline برای شاخه توسعه (development) و یک pipeline دیگر برای شاخه تولید (production).

### 8. **Pipeline with Environments**
این نوع pipeline به شما امکان می‌دهد که jobهای مختلف را در محیط‌های مختلف (مانند staging، production، و غیره) اجرا کنید. این قابلیت به مدیریت بهتر فرآیند استقرار و تست کمک می‌کند.


### نحوه تعریف انواع مختلف pipeline در GitLab

#### Basic Pipeline
```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."

test_job:
  stage: test
  script:
    - echo "Running tests..."

deploy_job:
  stage: deploy
  script:
    - echo "Deploying the project..."
```
