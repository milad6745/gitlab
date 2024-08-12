در اینجا یک پروژه ساده برای شما ایجاد می‌کنیم که شامل یک Dockerfile، فایل Docker Compose و پیکربندی GitLab CI برای ساخت و انتشار ایمیج Docker در GitLab Container Registry است.

### ساختار پروژه:
```
simple-docker-project/
├── Dockerfile
├── docker-compose.yml
├── app/
│   └── main.py
└── .gitlab-ci.yml
```

### 1. ساخت Dockerfile

ابتدا یک `Dockerfile` ایجاد می‌کنیم که یک اپلیکیشن ساده پایتونی را در یک کانتینر اجرا می‌کند.

```dockerfile
# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy source code to the container
COPY app/ /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
```

### 2. ساخت فایل docker-compose.yml

سپس یک فایل `docker-compose.yml` ایجاد می‌کنیم که Docker Compose را برای اجرای سرویس اپلیکیشن ما تنظیم می‌کند.

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
    ports:
      - "8080:8080"
```

### 3. ایجاد کد اپلیکیشن

در پوشه `app` یک فایل به نام `main.py` ایجاد کنید و کد زیر را در آن قرار دهید:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

همچنین یک فایل `requirements.txt` برای نصب وابستگی‌های لازم ایجاد کنید:

```txt
Flask==2.0.3
```

### 4. نوشتن GitLab CI Pipeline

فایل `.gitlab-ci.yml` را در دایرکتوری ریشه پروژه ایجاد کنید. این فایل یک pipeline ساده ایجاد می‌کند که ایمیج Docker را می‌سازد و آن را در GitLab Container Registry منتشر می‌کند.

```yaml
stages:
  - test
  - build
  - push

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG

before_script:
  - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

test:
  stage: test
  script:
    - docker-compose up -d  # اپلیکیشن Flask را اجرا می‌کند
    - sleep 5  # چند ثانیه صبر می‌کنیم تا سرور بالا بیاید
    - docker-compose ps  # وضعیت کانتینرها را چک می‌کند
    - docker-compose logs app  # لاگ‌های اپلیکیشن را بررسی می‌کند
    - docker-compose down  # بعد از تست، کانتینرها را متوقف می‌کند
  only:
    - main  # اجرا در برنچ main

build_image:
  stage: build
  script:
    - docker build -t $IMAGE_TAG .
  only:
    - main  # اجرا در برنچ main

push_image:
  stage: push
  script:
    - docker push $IMAGE_TAG
  only:
    - main  # اجرا در برنچ main
```

### 5. تنظیمات GitLab برای Docker Registry

1. پروژه‌ی خود را در GitLab بسازید.
2. به تنظیمات پروژه بروید و دسترسی به Container Registry را فعال کنید.
3. به مسیر `Settings > CI / CD > Variables` بروید و متغیرهای زیر را اضافه کنید:
   - `CI_REGISTRY_USER` (مقدار: نام کاربری GitLab)
   - `CI_REGISTRY_PASSWORD` (مقدار: رمز عبور GitLab یا Token)
  
### 6. اجرای Pipeline

پس از انجام مراحل بالا و کامیت کردن کدها به ریپازیتوری، Pipeline به طور خودکار اجرا می‌شود و ایمیج Docker در GitLab Container Registry منتشر می‌شود.

با اجرای این مراحل شما یک پروژه ساده ایجاد کرده‌اید که با استفاده از Dockerfile و Docker Compose اجرا می‌شود و با GitLab CI/CD ایمیج آن ساخته و در GitLab Container Registry منتشر می‌گردد.
