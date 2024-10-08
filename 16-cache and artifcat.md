
گذاشتن موقت پکیج ها و اپلیکیشن هایی که دانلود میکنیم . برای اینکه هر سری میخواهیم اجرا کنیم نره و دانلود کنه
آرتیفکت هم یک سری خروجی هاست که میتوانیم آنها را در گیت لب ذخیره کنم
مثلا فایل میسازم و آنها را نگهداری میکنم و در پایپ هاین های بعدی میتوانم ازش استفاده میکنم مثلا pdf , video , image, ..

### cache
تعریف Cache برای هر job: شما می‌توانید با استفاده از کلمه‌کلیدی cache برای هر job به صورت جداگانه، Cache را تعریف کنید. اگر این کار را نکنید، Cache به‌صورت پیش‌فرض غیرفعال است.

استفاده مجدد در pipeline‌های بعدی: اگر Cache در pipeline قبلی ایجاد شده باشد، pipeline‌های بعدی می‌توانند از همان Cache استفاده کنند.

استفاده در job‌های مشابه در یک pipeline: اگر وابستگی‌های job‌ها یکسان باشند، job‌های بعدی در همان pipeline می‌توانند از Cache استفاده کنند.

عدم اشتراک‌گذاری بین پروژه‌ها: Cache‌ها بین پروژه‌های مختلف به اشتراک گذاشته نمی‌شوند.

جداسازی Cache بین شاخه‌های محافظت‌شده و محافظت‌نشده: به‌صورت پیش‌فرض، شاخه‌های محافظت‌شده و محافظت‌نشده Cache‌های جداگانه دارند. اما شما می‌توانید این رفتار را تغییر دهید.


### artifact

تعریف Artifacts برای هر job: مانند Cache، شما باید Artifacts را برای هر job به صورت جداگانه تعریف کنید.

استفاده در مراحل بعدی: job‌های مراحل بعدی در همان pipeline می‌توانند از Artifacts استفاده کنند.

عدم اشتراک‌گذاری بین پروژه‌ها: مانند Cache، Artifacts نیز بین پروژه‌های مختلف به اشتراک گذاشته نمی‌شوند.

تاریخ انقضاء: به‌صورت پیش‌فرض، Artifacts پس از ۳۰ روز منقضی می‌شوند، اما شما می‌توانید زمان انقضاء را به‌صورت سفارشی تنظیم کنید.

عدم انقضاء آخرین Artifacts: اگر گزینه "keep latest artifacts" فعال باشد، آخرین Artifacts منقضی نمی‌شوند.

کنترل دسترسی به Artifacts: شما می‌توانید با استفاده از کلمه‌کلیدی dependencies کنترل کنید که کدام job‌ها بتوانند به Artifacts دسترسی داشته باشند.




این متن درباره **روش‌های بهینه برای استفاده از Cache** در GitLab CI/CD صحبت می‌کند. هدف از این روش‌ها این است که اطمینان حاصل شود Cache همیشه در دسترس است و به طور مؤثر استفاده می‌شود.

### **روش‌های بهینه برای استفاده از Cache:**

1. **برچسب‌گذاری (Tagging) Runners:**
   - **برچسب‌گذاری Runners** و استفاده از این برچسب‌ها در jobهایی که از یک Cache مشترک استفاده می‌کنند، به دسترسی آسان‌تر به Cache کمک می‌کند.

2. **استفاده از Runners اختصاصی برای پروژه خاص:**
   - اگر Runners را فقط به یک پروژه خاص اختصاص دهید، می‌توانید Cache را به‌صورت مؤثرتری مدیریت کنید و از مشکلاتی مانند تداخل Cache‌ها بین پروژه‌های مختلف جلوگیری کنید.

3. **استفاده از کلید مناسب برای Cache:**
   - انتخاب کلیدی که مناسب با جریان کاری (workflow) شما باشد اهمیت زیادی دارد. به عنوان مثال، می‌توانید یک Cache جداگانه برای هر شاخه (branch) ایجاد کنید.

### **کار با Runners و Cache:**

برای اینکه Runners بتوانند به‌طور مؤثر با Cache کار کنند، باید یکی از این کارها را انجام دهید:

1. **استفاده از یک Runner واحد برای تمام jobها:**
   - این کار تضمین می‌کند که Cache همیشه در دسترس است و مشکلاتی مانند تفاوت در نسخه یا معماری Runner‌ها به وجود نمی‌آید.

2. **استفاده از چندین Runner با Cache توزیع‌شده:**
   - این روش شامل ذخیره Cache در S3 buckets است که GitLab.com نیز از همین روش استفاده می‌کند. این Runners می‌توانند به صورت خودکار مقیاس‌بندی شوند (autoscale mode) ولی لزومی به این کار نیست. همچنین می‌توانید قوانین مربوط به چرخه عمر (lifecycle rules) را برای مدیریت حذف Cache‌های قدیمی تنظیم کنید.

3. **استفاده از چندین Runner با معماری یکسان و دایرکتوری شبکه مشترک:**
   - این Runners باید از معماری یکسانی برخوردار باشند و Cache را در یک دایرکتوری شبکه مشترک (مانند NFS) ذخیره کنند. همچنین باید قابلیت مقیاس‌بندی خودکار (autoscale mode) داشته باشند.

### **نتیجه‌گیری:**
این روش‌ها به شما کمک می‌کنند تا Cache در GitLab CI/CD به‌صورت بهینه و مؤثر مدیریت شود، که نتیجه آن بهبود کارایی و کاهش زمان اجرای pipeline‌ها است.

### Example 
در اینجا یک مثال ساده‌تر از استفاده از **Cache** و **Artifacts** در GitLab CI/CD برای مدیریت پکیج‌های پایتون آورده شده است:

```yaml
stages:
  - install
  - test

# تعریف Cache برای پکیج‌های pip
cache:
  paths:
    - .cache/pip  # دایرکتوری که پکیج‌های pip کش می‌شوند

install_dependencies:
  stage: install
  script:
    - pip install -r requirements.txt  # نصب پکیج‌ها از فایل requirements.txt
  artifacts:
    paths:
      - .venv  # ذخیره محیط مجازی پایتون به عنوان artifact

run_tests:
  stage: test
  script:
    - source .venv/bin/activate  # فعال‌سازی محیط مجازی
    - pytest  # اجرای تست‌ها
  dependencies:
    - install_dependencies  # استفاده از artifact نصب شده در job قبلی
```

### توضیح مثال:

1. **Cache:**
   - `paths: .cache/pip`: دایرکتوری `.cache/pip` جایی است که پکیج‌های pip کش می‌شوند. این باعث می‌شود که اگر پکیجی قبلاً نصب شده باشد، نیازی به دانلود دوباره نداشته باشید.

2. **Artifacts:**
   - `artifacts` در job `install_dependencies`: بعد از نصب پکیج‌ها، محیط مجازی پایتون (`.venv`) به‌عنوان artifact ذخیره می‌شود تا در job بعدی مورد استفاده قرار گیرد.
   - `dependencies` در job `run_tests`: این job از artifact ساخته شده در job `install_dependencies` استفاده می‌کند تا محیط مجازی آماده را برای اجرای تست‌ها به کار بگیرد.

این مثال ساده نشان می‌دهد که چگونه می‌توانید با استفاده از Cache و Artifacts، زمان نصب و اجرای پکیج‌ها و تست‌ها را کاهش دهید.
