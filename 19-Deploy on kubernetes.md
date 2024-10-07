
### 1. **استقرار (Deployment) چیست؟**
Deployment به معنی انتشار نسخه‌ی جدید پروژه در سرور یا محیطی است که کاربران نهایی بتوانند به آن دسترسی داشته باشند. شما می‌توانید پروژه خود را به یک سرور، Kubernetes cluster، یا هر محیط دیگری استقرار دهید.

### 2. **پیکربندی مرحله‌ی استقرار در `.gitlab-ci.yml`:**
فرض می‌کنیم که می‌خواهید پروژه را روی یک سرور یا یک سرویس ابری مانند Kubernetes استقرار دهید.

#### مثال: استقرار روی یک سرور با استفاده از SSH
در این مثال، از طریق SSH به یک سرور متصل می‌شویم و دستوراتی را برای استقرار پروژه اجرا می‌کنیم.

فایل `.gitlab-ci.yml` را به‌روز کنید:

```yaml
stages:
  - build
  - test
  - deploy

build-job:
  stage: build
  script:
    - docker build -t my-image:latest .
    - docker tag my-image:latest registry.gitlab.com/username/my-cicd-project:latest
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
    - docker push registry.gitlab.com/username/my-cicd-project:latest

test-job:
  stage: test
  script:
    - echo "Running tests"

deploy-job:
  stage: deploy
  script:
    - echo "Deploying application"
    - ssh user@your-server.com "docker pull registry.gitlab.com/username/my-cicd-project:latest && docker stop my-container && docker rm my-container && docker run -d --name my-container registry.gitlab.com/username/my-cicd-project:latest"
  only:
    - main
```

#### توضیحات:
- **ssh user@your-server.com**: این دستور از طریق SSH به سرور مقصد متصل می‌شود.
- **docker pull**: تصویر Docker جدیدی که ساخته و push شده است را از registry می‌کشد.
- **docker stop و docker rm**: کانتینر قبلی را متوقف و حذف می‌کند.
- **docker run**: یک کانتینر جدید با استفاده از تصویر جدید اجرا می‌کند.
- **only: main**: این دستور به GitLab می‌گوید که استقرار تنها وقتی انجام شود که تغییرات در شاخه‌ی `main` اعمال شده باشد.

### 3. **تنظیم متغیرهای CI/CD برای SSH:**

برای برقراری اتصال SSH، شما باید کلیدهای SSH را در تنظیمات CI/CD پروژه خود پیکربندی کنید.

1. به تنظیمات پروژه خود در GitLab بروید.
2. روی "Settings" کلیک کنید و سپس به بخش "CI/CD" بروید.
3. در بخش "Variables"، کلید خصوصی SSH (private SSH key) را به عنوان یک متغیر با نام **SSH_PRIVATE_KEY** اضافه کنید.

در فایل `.gitlab-ci.yml`، دستور زیر را برای استفاده از این کلید اضافه کنید:

```yaml
before_script:
  - 'which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )'
  - eval $(ssh-agent -s)
  - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
  - mkdir -p ~/.ssh
  - chmod 700 ~/.ssh
  - ssh-keyscan your-server.com >> ~/.ssh/known_hosts
```

### 4. **استقرار روی Kubernetes (اختیاری)**:

اگر از Kubernetes برای استقرار استفاده می‌کنید، به جای استفاده از SSH، می‌توانید از `kubectl` برای استقرار پروژه در یک Kubernetes cluster استفاده کنید.

#### مثال برای Kubernetes:

```yaml
deploy-job:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -f deployment.yaml
  only:
    - main
```

### 5. **مشاهده اجرای مرحله‌ی استقرار:**

پس از اضافه کردن مرحله‌ی استقرار، آن را commit و push کنید. سپس به صفحه CI/CD در GitLab بروید و بررسی کنید که مراحل استقرار به درستی اجرا می‌شوند. در صورتی که همه چیز درست تنظیم شده باشد، پروژه شما به صورت خودکار روی سرور یا Kubernetes استقرار می‌یابد.

---

### مرحله بعدی:
اگر پروژه شما آماده استقرار است، می‌توانیم نحوه‌ی **پیکربندی سرور برای اجرای Docker** یا **استفاده از Kubernetes** را بررسی کنیم. کدام گزینه برای شما مناسب‌تر است یا نیاز به راهنمایی بیشتر در کدام بخش دارید؟
