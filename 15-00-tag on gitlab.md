## Tag on gitlab
در گیت لب میتوانیم برای gitlab runner هایمان تگ قرار دهیم .
به این صورت که وارد پروژه میشود

oprn project > Setting > CICD > runner > Expand

سپس یک رانر جدید با تگ درست میکنیم .

![image](https://github.com/user-attachments/assets/3171f625-b6cd-43f5-83d1-cef2e9eec0cc)

با کامند زیر رد سرور gitlab runner خود را ایجاد میکنیم
```
gitlab-runner register

  --url https://gitlab.com

  --token glrt-5xMVKzLDfyQEoqoy5Yuc
```

سپس در کانفیگ gitlab runner سرور مان مشاهده میکنیم که یه رانر ایجاد شده است .
```
nano /etc/gitlab-runner/config.toml

[[runners]]
  name = "dev"
  url = "https://gitlab.com"
  id = 40563843
  token = "glrt-5xMVKzLDfyQEoqoy5Yuc"
  token_obtained_at = 2024-08-13T07:53:45Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "shell"
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
```
## create 2 runner
![image](https://github.com/user-attachments/assets/65ee99bd-02ff-4906-803e-3e1c9b7a97ac)

ما در اینجا دو رانر ساختیم که محیط تست را با رانر تست و دیگری را در محیط عملیاتی اجرا کنیم.

```
test:
  stage: test
  environment:
    name: Test
  tags:
    - Dev
  script:
    - docker-compose up -d  
بعد از تست، کانتینرها را متوقف می‌کند
  only:
    - main  # اجرا در برنچ main

Production:
  stage: test
  environment:
    name: Producation
  when: manual
  tags: 
    - pro
  script:
    - docker-compose up -d  
بعد از تست، کانتینرها را متوقف می‌کند
```

بعد از اجرای پایپ لاین هر قسمت با یک رانر اجرا میشود .

![image](https://github.com/user-attachments/assets/01b56c3a-09c1-480b-80f6-78a31f033464)
![image](https://github.com/user-attachments/assets/704be1da-b4de-44ff-b359-05934606e099)

