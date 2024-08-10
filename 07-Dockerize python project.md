
## Dockerize Python Project

**install django**

``` 
pip install django
pip freeze | grep -i django
Django==4.2.14

#start a project
django-admin startproject simple_app

#check directory
cd simple_app/
ls
manage.py  simple_app

#run django project
python3 manage.py runserver
```

**create a test app**

```
cd simple_app/
python3 manage.py runserver app
cd app
```
```
nano test.py
from django.test import TestCase

class SimpleTest (TestCase):
  def test_basic_addition(self):
    self.assertEqual(1 + 1, 2)

  def test_basic_substraction(self):
    self.assertEqual(5 - 2, 3)

  def test_basic_multiplication(self):
    self.assertEqual(2 * 2, 4)

# run a test
python3 manage.py test
```

**create require.txt**
```
pip freeze > requirements.txt
```

**create docker file**

```yml
FROM python:3.11

ENV HOME=/home/app/simple_app
RUN mkdir -p $HOME
WORKDIR $HOME

ENV PYTHONUNBUFFERED=1 # بافر نشدن پايتون
ENV PYTHONDONTWRITEBYTECODE=1 # کاهش زمان تصوير

COPY . $HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000

```
**create docker compose**

```yaml
version: "3"

services:
  simple_app:
    build: .
    ports:
      - 8000:8000
```

```
docker-compose up -d
```

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

‍‍‍‍‍‍‍‍```
git remote -v
origin	https://gitlab.com/test7522003/dj.git (fetch)
origin	https://gitlab.com/test7522003/dj.git (push)
```

