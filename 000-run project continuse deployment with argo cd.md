## run project continuse deployment with argo cd

---

## 🚀 مسیر یادگیری Argo CD — مرحله به مرحله:

---

### ✅ ۱. پیش‌نیازها

قبل از نصب Argo CD، بهتره موارد زیر رو بلد باشی یا نصب داشته باشی:

* Kubernetes (Minikube, kind, یا کلاستر واقعی)
* `kubectl`
* `git` و مفاهیم CI/CD ساده
* Helm (در صورت استفاده)

> اگه خواستی، می‌تونم همه اینا رو هم قدم‌به‌قدم برات توضیح بدم.

---

### ✅ ۲. نصب Argo CD (روی Minikube یا هر کلاستر دیگه)

```bash
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

بررسی نصب:

```bash
kubectl get pods -n argocd
```

---

### ✅ ۳. دسترسی به UI Argo CD

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

بعد برو به: `https://localhost:8080`

ورود:

```bash
# نام کاربری:
admin

# رمز عبور:
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

---

### ✅ ۴. تعریف اولین اپلیکیشن

یک مخزن Git داشته باش که شامل یک Kustomize یا Helm chart باشه. مثلاً این:

```
https://github.com/argoproj/argocd-example-apps
```

ساخت اپلیکیشن با CLI:

```bash
 argocd app create myapp
--repo https://gitlab.com/milad6745/kuber.git \
--path . \
--dest-server https://kubernetes.default.svc \
--dest-namespace default \
--directory-recurse \
--sync-policy automated
```

سینک کردن (deploy):

```bash
argocd app sync guestbook
```

---

### ✅ ۵. مفاهیم اصلی که باید یاد بگیری

| مفهوم         | توضیح                                     |
| ------------- | ----------------------------------------- |
| Application   | تعریف هر سرویس یا اپ که باید Deploy شه    |
| Sync          | همگام‌سازی وضعیت واقعی با Git             |
| Rollback      | بازگرداندن به نسخه قبلی                   |
| Health Status | بررسی سالم بودن منابع                     |
| Hooks         | اجرای اسکریپت‌های قبل یا بعد از Sync      |
| Multi-tenancy | پشتیبانی از چند کاربر و پروژه در یک سیستم |

---

### ✅ ۶. تمرین‌های پیشنهادی

1. یک اپ ساده (مثلاً Nginx) با Kustomize بساز و Deploy کن
2. یک اپ Helm-based رو Deploy کن
3. حالت Auto-Sync رو فعال کن و تغییری توی Git بده
4. RBAC و دسترسی‌ها رو برای کاربران مختلف تنظیم کن

---



وو در نهایت پس از نصب آرگو میبایست فایل gitlab ci را نیز تغییر دهیم .

```
stages:
  - build
  - deploy

variables:
  IMAGE_TAG: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"

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

deploy:
  stage: deploy
  image: alpine:3.19
  script:
    # دانلود yq داخل /tmp و دادن دسترسی اجرا
    - wget -qO /tmp/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    - chmod +x /tmp/yq

    # جایگزینی image در deployment.yaml با استفاده از yq در /tmp
    - /tmp/yq eval '.spec.template.spec.containers[] |= select(.name == "myapp-container").image = env(IMAGE_TAG)' -i deployment.yaml

    # تنظیم git و commit تغییرات
    - git config --global user.name "gitlab-ci"
    - git config --global user.email "ci@example.com"
    - git add deployment.yaml
    - git commit -m "Update image to $CI_COMMIT_SHORT_SHA [skip ci]" || echo "No changes to commit"

    # push تغییرات با token
    - git remote set-url origin https://oauth2:${GITLAB_TOKEN}@gitlab.com/$CI_PROJECT_PATH.git
    - git push origin HEAD:main || echo "Push failed"

  only:
    - main
```

خیلی عالی! فایل `.gitlab-ci.yml` که نوشتی، یک **pipeline دو مرحله‌ای (build و deploy)** هست که با Argo CD هم **ادغام غیرمستقیم (GitOps-style)** شده. یعنی خود Argo CD کاری با GitLab CI/CD نداره، فقط تغییرات توی گیت رو مانیتور می‌کنه و خودش دیپلوی می‌کنه.

بذار مرحله به مرحله برات توضیح بدم:

---

## 🔧 ساختار کلی

```yaml
stages:
  - build
  - deploy
```

دو مرحله تعریف کردی: `build` و `deploy`

---

## 🧱 متغیرها

```yaml
variables:
  IMAGE_TAG: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
```

اینجا `IMAGE_TAG` برای تگ کردن ایمیج داکر استفاده می‌شه. شامل:

* `CI_REGISTRY_IMAGE`: آدرس رجیستری پروژه در GitLab
* `CI_COMMIT_SHORT_SHA`: هش کوتاه کامیت فعلی

---

## 🛠 مرحله Build

```yaml
build:
  stage: build
  image: docker:24.0.5
  services:
    - docker:dind
```

### خلاصه کاری که این مرحله انجام می‌ده:

1. لاگین به GitLab Container Registry
2. Build ایمیج داکر از مسیر `./project`
3. Push به registry (با retry تا ۳ بار اگه شکست خورد)

```yaml
before_script:
  - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" $CI_REGISTRY --password-stdin
script:
  - docker build -t $IMAGE_TAG ./project
  - for i in {1..3}; do docker push $IMAGE_TAG && break || sleep 10; done
```

✅ همه‌چی خوب، امن و استاندارده.

---

## 🚀 مرحله Deploy (GitOps)

```yaml
deploy:
  stage: deploy
  image: alpine:3.19
```

### کارهایی که این مرحله انجام می‌ده:

#### 1. دانلود ابزار `yq` برای ویرایش YAML:

```bash
wget -qO /tmp/yq ... && chmod +x /tmp/yq
```

#### 2. به‌روزرسانی فایل `deployment.yaml`:

```bash
/tmp/yq eval '.spec.template.spec.containers[] |= select(.name == "myapp-container").image = env(IMAGE_TAG)' -i deployment.yaml
```

➡️ یعنی ایمیج `myapp-container` رو در `deployment.yaml` با مقدار جدید `IMAGE_TAG` جایگزین می‌کنه.

#### 3. کامیت تغییر:

```bash
git config --global ...
git add deployment.yaml
git commit -m "Update image to $CI_COMMIT_SHORT_SHA [skip ci]"
```

📝 `skip ci` باعث می‌شه این commit باعث اجرای دوباره pipeline نشه.

#### 4. Push به Git (با Token):

```bash
git remote set-url ...
git push origin HEAD:main || echo "Push failed"
```

---

## 🎯 نکته مهم: **ارتباط با Argo CD**

تو از GitOps استفاده می‌کنی به این شکل که:

* فقط فایل `deployment.yaml` رو به‌روز می‌کنی و push می‌زنی به main
* Argo CD که روی اون ریپو واچ گذاشته، به‌صورت اتوماتیک این تغییر رو sync و deploy می‌کنه
* بنابراین GitLab هیچ ارتباط مستقیمی با کلاستر نداره — این یه الگوی **Pull-based GitOps** هست (خالص و اصولی ✅)

---

## 📌 خلاصه نقاط قوت فایل تو:

| بخش                                           | وضعیت                                             |
| --------------------------------------------- | ------------------------------------------------- |
| Separation of concerns                        | ✅ عالی؛ CI فقط build می‌کنه و Git رو آپدیت می‌کنه |
| GitOps pattern                                | ✅ خالص؛ بدون دخالت مستقیم در کلاستر               |
| امنیت Push با Token                           | ✅ رعایت شده                                       |
| YQ برای تغییر فایل YAML                       | ✅ ابزار سبُک و مؤثر                               |
| کنترل خطاها (push failure, commit بدون تغییر) | ✅ حساب‌شده                                        |

---

اگه خواستی، می‌تونم:

* فایل `deployment.yaml` پیشنهادی بر اساس best practice بسازم
* یا CI رو توسعه بدم برای multi-env یا Canary Deployment

دوست داری کدوم سمت بری؟

