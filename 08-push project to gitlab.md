
**push a project to gitlab**

```
git init
git add .
git commit -m "Push existing project to GitLab"
git remote add origin https://gitlab.com/cameronmcnz/example-website.git
git push -u origin master
```

سپس باید یک runner برای این پروژه که پوش کردیم ایجاد کنیم .



نکته :
ما میتوانیم چندین تا origin داشته باشیم پس از ادد کردن origin های متفاوت میتوانیم با کامند زیر ببینیم به جه origin هایی متصل هست .
```
git remote -v
origin	https://gitlab.com/test7522003/dj.git (fetch)
origin	https://gitlab.com/test7522003/dj.git (push)
```
