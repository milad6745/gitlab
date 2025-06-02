در CI/CD (به‌ویژه در GitLab CI/CD)، مفهوم **`Environments` (محیط‌ها)** به **مکان‌هایی که نرم‌افزار در آن مستقر (Deploy) می‌شود** اشاره دارد — مثلاً محیط‌های:

* `development` (توسعه)
* `staging` (آزمایشی)
* `production` (نهایی)

---

## 🔹 تعریف ساده:

**Environment** یک لایه منطقی در فرآیند انتشار (Deployment) است که مشخص می‌کند **کد در کجا اجرا می‌شود**.

---

## ✅ چرا از Environments استفاده می‌کنیم؟

1. **جداسازی محیط‌ها** (dev، staging، prod)
2. **کنترل و مشاهده بهتر وضعیت استقرار**
3. **رول‌بک یا حذف Deployment**
4. **مانیتورینگ Deploymentها در GitLab UI**

---

## 📘 مثال ساده از تعریف Environment در `.gitlab-ci.yml`:

```yaml
deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to staging..."
  environment:
    name: staging
    url: https://staging.example.com

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to production..."
  environment:
    name: production
    url: https://example.com
    on_stop: stop_production

stop_production:
  stage: cleanup
  script:
    - echo "Stopping production..."
  when: manual
  environment:
    name: production
    action: stop
```

---

## 🎯 قابلیت‌های مهم Environments در GitLab:

| ویژگی          | توضیح                                                            |
| -------------- | ---------------------------------------------------------------- |
| `name`         | نام محیط (مثلاً `production`, `dev`, ...)                        |
| `url`          | لینک به محیط (برای دکمه‌ی "Visit Environment")                   |
| `on_stop`      | jobی که محیط رو غیرفعال می‌کنه (مثلاً خاموش کردن سرویس)          |
| `action: stop` | مشخص می‌کنه job برای توقف environment هست                        |
| `auto_stop_in` | محیط رو بعد از مدت مشخصی غیرفعال می‌کنه (مثلاً برای review apps) |

---

## 💡 مثال کاربردی با استفاده از محیط:

```yaml
deploy:
  stage: deploy
  script:
    - kubectl apply -f deployment.yaml
  environment:
    name: production
    url: https://app.example.com
```

بعد از اجرای این Job، در بخش **Environments** در GitLab UI می‌تونی Deployment رو ببینی، وارد محیط بشی، یا حتی دستی متوقفش کنی.

---

## 🔄 ارتباط با ArgoCD

در حالت شما که Deploy سمت Argo انجام می‌شه، می‌تونی همچنان از Environments استفاده کنی برای **نشان دادن اینکه کد به کجا رفته**، حتی اگر Argo خودش Deployment رو مدیریت کنه.

مثلاً:

```yaml
deploy:
  stage: deploy
  script:
    - echo "Syncing ArgoCD..."
  environment:
    name: production
    url: https://argocd.example.com/applications/myapp
```

---


برای اینکه pipeline شما دارای **environmentهای مجزا مثل `dev`, `staging`, و `production`** باشد، می‌تونیم مراحل deploy را جدا کرده و برای هر محیط یک `job` تعریف کنیم. هر محیط هم `environment` مخصوص به خودش را دارد که GitLab UI به‌خوبی مدیریت‌شان می‌کند.

---

## ✅ 🎯 هدف:

* **مرحله build ثابت است.**
* **سه مرحله deploy مختلف داریم برای:**

  * `dev` (مثلاً برای برنچ `develop`)
  * `staging` (مثلاً برای برنچ `staging`)
  * `production` (برای برنچ `main`)

---

## 🔧 نسخه بهبود یافته `.gitlab-ci.yml`

```yaml
stages:
  - build
  - deploy

variables:
  IMAGE_TAG: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"

# ----------------- BUILD -----------------
build:
  stage: build
  image: docker:24.0.5
  services:
    - docker:dind
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" $CI_REGISTRY --password-stdin
  script:
    - docker build -t $IMAGE_TAG ./project
    - for i in {1..3}; do docker push $IMAGE_TAG && break || sleep 10; done

# ----------------- DEPLOY TO DEV -----------------
deploy_dev:
  stage: deploy
  image: alpine:3.19
  environment:
    name: dev
    url: https://dev.example.com
  script:
    - ./scripts/deploy.sh "$IMAGE_TAG" dev
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

# ----------------- DEPLOY TO STAGING -----------------
deploy_staging:
  stage: deploy
  image: alpine:3.19
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./scripts/deploy.sh "$IMAGE_TAG" staging
  rules:
    - if: '$CI_COMMIT_BRANCH == "staging"'

# ----------------- DEPLOY TO PRODUCTION -----------------
deploy_production:
  stage: deploy
  image: alpine:3.19
  environment:
    name: production
    url: https://example.com
  script:
    - ./scripts/deploy.sh "$IMAGE_TAG" prod
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

---

## 🧠 اسکریپت مشترک برای Deploy (داخل `scripts/deploy.sh`)

برای جلوگیری از تکرار، محتوا رو داخل یه اسکریپت بنویس:

```bash
#!/bin/sh

IMAGE_TAG=$1
ENV=$2

# دانلود yq
wget -qO /tmp/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
chmod +x /tmp/yq

# جایگزینی image در فایل deployment مربوط به آن محیط
/tmp/yq eval ".spec.template.spec.containers[] |= select(.name == \"myapp-container\").image = \"$IMAGE_TAG\"" -i "k8s/$ENV/deployment.yaml"

# commit تغییرات
git config --global user.name "gitlab-ci"
git config --global user.email "ci@example.com"
git add "k8s/$ENV/deployment.yaml"
git commit -m "[$ENV] Update image to $IMAGE_TAG [skip ci]" || echo "No changes"
git remote set-url origin https://oauth2:${GITLAB_TOKEN}@gitlab.com/$CI_PROJECT_PATH.git
git push origin HEAD:$CI_COMMIT_BRANCH || echo "Push failed"
```

---

## ✅ مزایای این روش:

* مشاهده Deploy هر محیط از UI → GitLab → Environments
* رول‌بک و مشاهده تاریخچه هر Environment
* اجرای مستقل هر Deploy بر اساس Branch

---

اگه می‌خوای از ArgoCD برای sync هم استفاده کنی، می‌تونیم داخل `deploy.sh` دستور `argocd app sync ...` هم بذاریم یا webhook بزنیم. بگو برات اضافه کنم.


