## pipeline problem

مایک pipe line نوشتیم و در آن یک داکر فایل اجرا میشود و سپس run میوشد .
حال اگر برای مرتبه دوم بخاهد اجرا شود میگوید کانتینر وجود دارد برای رفع آن میبایستقبل از اینکه در pipeline کانتینرمان را اجرا کنیم کانتینر های قبلی را پاک کنیم

حال برای اینکه موقعی که هر دفعه Pipeline را اجرا میکنیم بهمون نگوید که همچین container ای در حال اجرا است باید در pipe line تغییراتی بدهیم.

```
stages:
  - build_stage
  - deploy_stage

build:
  stage: build_stage
  script:
    - docker --version
    - docker build -t pyapp .

deploy:
  stage: deploy_stage
  script:
    - docker stop pyappcontainer && docker rm -f pyappcontainer
    - docker run --name pyappcontainer -p 9090:9090 pyapp
```
