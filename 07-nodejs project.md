## nodejs project

برای ایجاد یک وب سرویس ساده با استفاده از Node.js و فریمورک Express که پیام "Hello World" را در پاسخ به درخواست‌ها نشان دهد، می‌توانید به شکل زیر عمل کنید:

1. ابتدا باید Node.js و npm (مدیر بسته Node.js) را نصب کرده باشید.


```
apt update -y
apt install nodejs
apt install npm
``` xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

2. یک پروژه جدید Node.js ایجاد کنید:

   ```bash
   mkdir my-express-app
   cd my-express-app
   npm init -y
   ```

3. سپس Express را نصب کنید:

   ```bash
   npm install express
   ```

4. یک فایل با نام `index.js` در پوشه پروژه ایجاد کنید و کد زیر را در آن قرار دهید:

   ```javascript
   // Import کردن Express
   const express = require('express');

   // ساخت یک اپلیکیشن Express
   const app = express();

   // تعریف یک مسیر ساده که به درخواست‌های GET پاسخ می‌دهد
   app.get('/', (req, res) => {
     res.send('Hello World');
   });

   // شروع سرور و گوش دادن روی پورت 3000
   const PORT = 3000;
   app.listen(PORT, () => {
     console.log(`Server is running on http://localhost:${PORT}`);
   });
   ```

5. حالا سرور خود را اجرا کنید:

   ```bash
   node index.js
   ```

6. اگر همه چیز به درستی تنظیم شده باشد، سرور شما در حال اجرا است و می‌توانید با باز کردن مرورگر و وارد کردن آدرس `http://localhost:3000` پیام "Hello World" را ببینید.


## write a gitlabci
![image](https://github.com/user-attachments/assets/156c5a9d-1c17-4652-994e-fb54cc6e6711)


## upload a project to gitlab
```
git init
git add .
git commit -m "Push existing project to GitLab"
git remote add origin https://gitlab.com/cameronmcnz/example-website.git
git push -u origin master
```


حالا وقتی pipe line اجرا میشود میبینیم که پایپ لاین در مرحله Deploy فیلد میشود .
این برای این است که پایپ لاین ما باید با اولویت اجرا شود اما هر دو جاب با هم اجرا میشوند و قبل از build شدن میخواهد که Deploy شود که ارور میگیرد .
برای این کار باید مراحل را به جای اینکه داخل یک stage قرار دهیم به جاب های دیگری تبدیل کنیم که با اولویت اجرا شود .

پس به این صورت اصلاح میکنیم :

![image](https://github.com/user-attachments/assets/5534c7bb-721e-42b9-9719-c826d05c396e)


حال pipeline جدید مجدد اجرا میشود اما مرحله Deploy مجدد به مشکل میخورد .
دلیل آن این است که وقتی مرحله اول با موفقیت اجرا میشود pipeline میاید و تمامی خروجی های مرحله اول را پاک میکند یعنی پکیج هایی که در مرحله اول نصب کردیم که در محلیه دوه از آنها استفاده کنیم پاک میشود.
حال راهکار چیست ؟

استفاده از artifact
یعنی مسیرایی که بهش میگیم رو بعد از اتمام Stage پاک نکن

![image](https://github.com/user-attachments/assets/ae326e66-3e5d-419c-986b-50fe466165f4)




