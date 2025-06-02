در GitLab CI/CD، مفهومی به نام **workflow** وجود داره که به شما این امکان رو می‌ده کنترل بیشتری روی اینکه **کِی و چطور یک pipeline اجرا بشه** داشته باشید.

---

## ✅ تعریف Workflow در GitLab CI/CD

در `.gitlab-ci.yml`، بخش `workflow:` در بالای فایل قرار می‌گیره و تعیین می‌کنه:

* **آیا pipeline باید اجرا بشه یا نه**
* **بر اساس شرایط خاصی مثل نام برنچ، مقدار یک متغیر، یا merge request بودن**

```yaml
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
    - when: never
```

---

## 🧠 تفاوت Workflow با Rules در Jobها چیه؟

| ویژگی    | `workflow.rules`                     | `job.rules`                      |
| -------- | ------------------------------------ | -------------------------------- |
| محل اجرا | در سطح کل pipeline                   | در سطح job خاص                   |
| هدف      | اجرا/اجرا نشدن کل pipeline           | اجرا/اجرا نشدن یک job            |
| کاربرد   | کنترل اولیه روی trigger شدن pipeline | کنترل دقیق‌تر روی مراحل pipeline |

---

## ✅ مثال‌های کاربردی

### 🎯 اجرای Pipeline فقط روی `main` و `develop`

```yaml
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "develop"'
      when: always
    - when: never
```

---

### 🚀 اجرا فقط روی Merge Request

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
    - when: never
```

---

### ☁️ شرط بر اساس متغیر محیطی

```yaml
workflow:
  rules:
    - if: '$DEPLOY_ENV == "staging"'
      when: always
    - when: never
```

---

## 💡 بدون Workflow چطور عمل می‌کنه؟

اگه `workflow` ننویسی، GitLab همه‌ی pipelineها رو به صورت پیش‌فرض **اجرا می‌کنه** و کنترل فقط از طریق `rules` یا `only/except` تو jobها انجام می‌شه. اما با `workflow.rules` می‌تونی زودتر جلوی اجرا شدن کل pipeline رو بگیری (که به‌صرفه‌تره).

---

## ✳ جمع‌بندی

* `workflow.rules` برای کنترل **اجرای کل pipeline** استفاده می‌شه
* در بالای `.gitlab-ci.yml` قرار می‌گیره
* جلوی اجرا شدن‌های غیرضروری (مثلاً در برنچ‌های خاص یا در merge requestها) رو می‌گیره

---

اگر خواستی چند مثال بر اساس پروژه‌ی خودت (مثلاً فقط اجرا برای `develop`, `staging`, `main`) برات تنظیم کنم، بگو تا دقیق بنویسمش.


## مثال
حتماً! در ادامه یک کانفیگ کامل `.gitlab-ci.yml` برات می‌نویسم که شامل:

* ✅ اجرای Pipeline فقط برای برنچ‌های `develop`, `staging`, `main`
* ✅ دپلوی مجزا برای هر محیط
* ✅ استفاده از `workflow.rules`
* ✅ تغییر داینامیک فایل YAML با `yq`

---

## 🔧 فایل کامل `.gitlab-ci.yml`

```yaml
stages:
  - build
  - deploy

# ✅ اجرای pipeline فقط برای برنچ‌های خاص
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
      when: always
    - if: '$CI_COMMIT_BRANCH == "staging"'
      when: always
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
    - when: never

variables:
  IMAGE_TAG: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
  K8S_DIR: "k8s/$CI_COMMIT_BRANCH"

# ✅ مرحله build: ساختن image و push
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

# ✅ مرحله deploy: بروزرسانی فایل deployment.yaml مخصوص هر محیط
deploy:
  stage: deploy
  image: alpine:3.19
  script:
    - apk add --no-cache curl git
    - curl -sLo /tmp/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    - chmod +x /tmp/yq

    # جایگزینی ایمیج در فایل محیط مربوطه
    - /tmp/yq eval '.spec.template.spec.containers[] |= select(.name == "myapp-container").image = env(IMAGE_TAG)' -i "$K8S_DIR/deployment.yaml"

    # تنظیم git
    - git config --global user.name "gitlab-ci"
    - git config --global user.email "ci@example.com"
    - git add "$K8S_DIR/deployment.yaml"
    - git commit -m "Update image to $CI_COMMIT_SHORT_SHA for $CI_COMMIT_BRANCH [skip ci]" || echo "No changes"
    - git remote set-url origin https://oauth2:${GITLAB_TOKEN}@gitlab.com/$CI_PROJECT_PATH.git
    - git push origin HEAD:$CI_COMMIT_BRANCH || echo "Push failed"

  only:
    - develop
    - staging
    - main
```

---

## 📁 ساختار فایل‌ها باید این باشه:

```
.
├── .gitlab-ci.yml
├── project/
├── k8s/
│   ├── develop/
│   │   └── deployment.yaml
│   ├── staging/
│   │   └── deployment.yaml
│   └── main/
│       └── deployment.yaml
```

> در این ساختار، بسته به برنچی که push می‌کنی، فقط همون مسیر `k8s/<branch>/deployment.yaml` آپدیت می‌شه و ArgoCD اون رو sync می‌کنه.

---


