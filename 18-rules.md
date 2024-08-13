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
