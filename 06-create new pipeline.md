# create a new pipe line
بعد از ساخت gitlab runner میخواهیم یک basic pipeline ایجاد کنیم.

داخل repository امان میشویم یک فایل جدید ایجاد میکنیم و اسمش را gitlat-ci.yml. مگذاریم اسم دیگری قرار بدهیم کار نمیکند

سپس شروع به نوشتن پایپ لاینمان میکنیم.
```
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

سپس commit میکنیم .

MENU > build > pipeline 
میبینیم که یک ارور داده .

![Capture](https://github.com/user-attachments/assets/5b21b738-a897-4551-8c2a-75d63efb0a1b)

برای حل این مورد بر روی سرور gitlab runner را اجرا میکنیم و فایل زیر را پاک میکنیم .

cd /home/gitlab-runner/
rm -f .bash_logout

سپس مجدد ران میکنیم و مشکل برطرف میشود .

![image](https://github.com/user-attachments/assets/5c4f21b5-0dfb-49f0-8a90-93a8f20c6851)

![image](https://github.com/user-attachments/assets/c7b4a308-1aeb-4f6e-aae2-1e0eeceadbe6)






