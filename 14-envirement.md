## gitlab envirements

این مورد برای این استفاده میشود که ما میتوانیم محیط های متفاوت برای تست های خود داشته باشیم
مثلا من اول بیایم و تست کنم در محیط تست و سپس به محیط production بروم

open project > operate > envirement


از این مسیر env های خود را ایجاد میکنیم.

![image](https://github.com/user-attachments/assets/a6a8c0c5-6542-4a34-997e-29aacfef2044)

یکی تست و دیگری محیط production ساختیم.




در pipeline زیر ما مرحله ای که قرار است در production اجرا شود را دستی قرار دادیم که بعد از اینکه همه چیز اکی بود در production هم انجام دهد
```
test:
  stage: test
  environment:
    name: Test
  script:
    - docker-compose up -d  
    - sleep 5  
    - docker-compose ps  
    - docker-compose logs app  
    - docker-compose down 
  only:
    - main  # اجرا در برنچ main

Production:
  stage: test
  environment:
    name: Producation
  when: manual
  script:
    - docker-compose up -d  
    - sleep 5  
    - docker-compose ps 
    - docker-compose logs app 
    - docker-compose down
  only:
    - main  # اجرا در برنچ main

```

![image](https://github.com/user-attachments/assets/b9a2590e-081f-45be-b060-ac3da8d3e1ff)
