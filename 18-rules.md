## rules
میخواهیم یک رول بنویسیم و بگوییم اگر برنامه در برنچ تست بود فقط اجرا شود .

```
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."
  rules:
    - if: '$CI_COMMIT_BRANCH == "test"'

test_job:
  stage: test
  script:
    - echo "Running tests..."
  rules:
    - if: '$CI_COMMIT_BRANCH == "test"
```

که مشاهده میشود وقتی برنامه در مین است کار نمیکن د و فقط وقتی به برنچ تست میرود به درستی کار میکند .

![image](https://github.com/user-attachments/assets/3ed9c762-f0b7-4490-8dd0-7ce4a259a0aa)


### Example

در اینجا یک مثال دیگر از استفاده از `rules` در GitLab آورده شده است. در این مثال، می‌خواهیم یک job فقط تحت شرایط خاصی اجرا شود:

### سناریو:
- **build_job** فقط در برنچ `develop` اجرا می‌شود.
- **test_job** فقط زمانی اجرا می‌شود که یک merge request ایجاد شود.
- **deploy_job** فقط وقتی اجرا می‌شود که یک tag جدید با الگوی `vX.X.X` (مثل `v1.0.0`) ایجاد شود.

### نمونه فایل `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'  # فقط در برنچ develop اجرا می‌شود

test_job:
  stage: test
  script:
    - echo "Running tests..."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'  # فقط وقتی merge request باز شده باشد

deploy_job:
  stage: deploy
  script:
    - echo "Deploying the project..."
  rules:
    - if: '$CI_COMMIT_TAG =~ /^v[0-9]+(\.[0-9]+)*$/'  # فقط وقتی یک tag با الگوی vX.X.X ایجاد شده باشد
```
![image](https://github.com/user-attachments/assets/ebc7e66d-1223-49cc-a2d0-4a4efdc75bd3)

همچنین میتوانیم از Only هم استفاده کنیم ولی استفاده از rule خیلی حرفه ای تر است .

```
stages:
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."
  only:
    - Prob  # فقط در برنچ 'Prob' اجرا می‌شود
```
