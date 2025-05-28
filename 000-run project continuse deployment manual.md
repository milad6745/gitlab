میخواهیم یک پروژه بنویسیم با فلاسک بعد ببریمش داخل gitlabci و مراحل build , deploy روی کوبرنتیز را انجام دهیم
پروژه به فایل های زیر نیاز دارد
```
ls -lha
total 44K
drwxr-xr-x 6 root root 4.0K May 28 09:00 .
drwxr-xr-x 4 root root 4.0K May 27 15:25 ..
-rw-r--r-- 1 root root  410 May 26 15:09 app.py
-rw-r--r-- 1 root root  148 May 26 14:53 Dockerfile
drwxr-xr-x 8 root root 4.0K May 28 09:15 .git
-rw-r--r-- 1 root root    7 May 27 12:51 .gitignore
-rw-r--r-- 1 root root  952 May 28 09:00 .gitlab-ci.yml
drwxr-xr-x 5 root root 4.0K May 27 12:51 myenv
-rw-r--r-- 1 root root   13 May 26 14:51 requirements.txt
drwxr-xr-x 3 root root 4.0K May 26 15:08 static
drwxr-xr-x 2 root root 4.0K May 28 09:15 templates
```

app.py
```
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        user_text = request.form.get('user_text')
        message = f"شما نوشتید: {user_text}"
    return render_template('resume.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

Dockerfile
```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

.gitlab-ci.yml
```
stages:
  - build
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

build:
  stage: build
  image: docker:24.0.5
  services:
    - docker:dind
  before_script:
    - echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin  # 👈 برای جلوگیری از Rate Limit Docker Hub
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER $CI_REGISTRY --password-stdin
  script:
    - docker build -t $IMAGE_TAG .
    - |
      for i in {1..3}; do
        docker push $IMAGE_TAG && break || sleep 10
      done
#    - docker push $IMAGE_TAG

deploy:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: [""]
  script:
    - echo "$KUBECONFIG_DATA" | base64 -d > kubeconfig
    - export KUBECONFIG=$CI_PROJECT_DIR/kubeconfig
    - kubectl set image deployment/myapp-deployment myapp-container=$IMAGE_TAG
    - kubectl rollout status deployment/myapp-deployment
  only:
    - main

```

requirements.txt
```
flask==2.3.2
```

static/css/style.css
```
body {
    font-family: 'Vazir', Tahoma, sans-serif;
    background-color: #f8f9fa;
}

.square-menu .nav-link {
    width: 100px;
    height: 80px;
    background-color: #0d6efd;
    color: white !important;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-weight: 600;
    font-size: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgb(13 110 253 / 0.4);
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.square-menu .nav-link:hover,
.square-menu .nav-link:focus {
    background-color: #084298;
    box-shadow: 0 6px 12px rgb(8 66 152 / 0.6);
    text-decoration: none;
}

h2 {
    color: #0d6efd;
    font-weight: 700;
}

.timeline {
    border-left: 3px solid #0d6efd;
    margin-left: 10px;
    padding-left: 20px;
}

.timeline-item {
    margin-bottom: 20px;
    position: relative;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -12px;
    top: 5px;
    width: 14px;
    height: 14px;
    background-color: #0d6efd;
    border-radius: 50%;
    box-shadow: 0 0 8px #0d6efd;
}

a {
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

templates/resume.html
```
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>رزومه میلاد باوسی - مهندس DevOps</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet" />
  <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet" />
</head>
<body class="bg-light">

<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm mb-4">
  <div class="container justify-content-center">
    <ul class="navbar-nav gap-3">
      <li class="nav-item"><a class="nav-link" href="#about">درباره من</a></li>
      <li class="nav-item"><a class="nav-link" href="#skills">مهارت‌ها</a></li>
      <li class="nav-item"><a class="nav-link" href="#experience">تجربه‌ها</a></li>
      <li class="nav-item"><a class="nav-link" href="#education">تحصیلات</a></li>
      <li class="nav-item"><a class="nav-link" href="#contact">تماس</a></li>
    </ul>
  </div>
</nav>

<header class="text-center py-5 mb-4 bg-primary text-white rounded shadow-sm container-lg">
  <h1 class="fw-bold">میلاد باوسی</h1>
  <p class="lead">مهندس دواپس (DevOps Engineer)</p>
</header>

<main class="container-lg">

  <!-- درباره من -->
  <section id="about" class="mb-5 p-4 bg-white rounded shadow-sm border">
    <h2 class="mb-3 border-bottom pb-2">درباره من</h2>
    <p>سلام! من میلاد باوسی هستم، مهندس دواپس با تجربه در پیاده‌سازی زیرساخت‌های ابری، اتوماسیون و مدیریت سیستم‌ها. علاقه‌مند به استفاده از ابزارهای نوین مانند Kubernetes، Docker، Jenkins و AWS هستم.</p>
  </section>

  <!-- مهارت‌ها -->
  <section id="skills" class="mb-5 p-4 bg-white rounded shadow-sm border">
    <h2 class="mb-3 border-bottom pb-2">مهارت‌ها</h2>
    <ul class="list-group list-group-flush">
      <li class="list-group-item"><strong>ابزارهای کانتینری:</strong> Docker, containerd, Kubernetes</li>
      <li class="list-group-item"><strong>اتوماسیون CI/CD:</strong> Jenkins, GitLab CI, Ansible</li>
      <li class="list-group-item"><strong>کلود و زیرساخت:</strong> AWS, Azure, Terraform</li>
      <li class="list-group-item"><strong>زبان‌ها:</strong> Python, Bash, Go</li>
    </ul>
  </section>

  <!-- تجربه‌ها -->
  <section id="experience" class="mb-5 p-4 bg-white rounded shadow-sm border">
    <h2 class="mb-3 border-bottom pb-2">تجربه‌های شغلی</h2>
    <div>
      <h5>مهندس دواپس - شرکت XYZ</h5>
      <small class="text-muted">فروردین ۱۴۰۱ تا اکنون</small>
      <p>مدیریت کلاستر Kubernetes، طراحی Pipeline‌های CI/CD، و مانیتورینگ با Prometheus و Grafana.</p>
    </div>
    <div class="mt-4">
      <h5>مدیر سیستم - شرکت ABC</h5>
      <small class="text-muted">دی ۱۳۹۸ تا اسفند ۱۴۰۰</small>
      <p>پیاده‌سازی اتوماسیون زیرساخت با Ansible و بهینه‌سازی محیط AWS.</p>
    </div>
  </section>

  <!-- تحصیلات -->
  <section id="education" class="mb-5 p-4 bg-white rounded shadow-sm border">
    <h2 class="mb-3 border-bottom pb-2">تحصیلات</h2>
    <ul>
      <li>کارشناسی مهندسی کامپیوتر - دانشگاه تهران (۱۳۹۴ - ۱۳۹۸)</li>
    </ul>
  </section>

  <!-- تماس -->
  <section id="contact" class="mb-5 p-4 bg-white rounded shadow-sm border">
    <h2 class="mb-3 border-bottom pb-2">تماس با من</h2>
    <p><strong>ایمیل:</strong> <a href="mailto:milad.baousi@example.com">milad.baousi@example.com</a></p>
    <p><strong>تلفن:</strong> ۰۹۱۲-۱۲۳-۴۵۶۷</p>
    <p><strong>LinkedIn:</strong> <a href="https://linkedin.com/in/miladbaousi" target="_blank">linkedin.com/in/miladbaousi</a></p>
    <p><strong>GitHub:</strong> <a href="https://github.com/miladbaousi" target="_blank">github.com/miladbaousi</a></p>
  </section>
</main>

<footer class="text-center py-3 bg-primary text-white mt-4 rounded shadow-sm container-lg">
  © 2025 میلاد باوسی - کلیه حقوق محفوظ است.
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

ساخت ایمیج با داکر فایل مربوطه : 

```
docker build -t myapp:latest .
```

آپلود ایمیج به کانتینر رجیستری gitlab

```
docker tag myapp:latest registry.gitlab.com/YOUR_PROJECT_PATH/myapp:latest
docker push registry.gitlab.com/YOUR_PROJECT_PATH/myapp:latest
```

دپلود کردن در کوبرنتیز و اجرا در کوبرنتیز
Deployment.yml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp-container
          image: registry.gitlab.com/milad6745/kuber/myapp:latest
          ports:
            - containerPort: 8080
```
service.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30007  # یا خالی بذار تا خودش عدد بده
```

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

تست
```
curl http://<Node-IP>:30007/
```

خیلی خوب! 😎
حالا برای اینکه با هر push کد، اپلیکیشن به صورت **اتوماتیک** build بشه، به GitLab Registry push بشه و روی **Kubernetes Deploy** بشه، فایل `.gitlab-ci.yml` زیر رو استفاده کن:

---

## 🛠️ فایل `.gitlab-ci.yml`

```yaml
stages:
  - build
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

before_script:
  - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER $CI_REGISTRY --password-stdin

build:
  stage: build
  image: docker:24.0.5
  services:
    - docker:dind
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG

deploy:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: [""]
  script:
    - echo "$KUBECONFIG_DATA" | base64 -d > kubeconfig
    - export KUBECONFIG=$CI_PROJECT_DIR/kubeconfig
    - kubectl config use-context default
    - kubectl set image deployment/myapp-deployment myapp-container=$IMAGE_TAG
    - kubectl rollout status deployment/myapp-deployment
  only:
    - main  # یا master بسته به نام شاخه اصلی پروژه‌ات
```

---

## 🔐 GitLab CI Variables

برو به:
**GitLab > Settings > CI/CD > Variables** و این‌ها رو تنظیم کن:

| نام متغیر              | مقدار                                                        |
| ---------------------- | ------------------------------------------------------------ |
| `CI_REGISTRY_USER`     | (معمولاً خودکار تنظیم شده، ولی اگه نشد، یوزر GitLab رو بذار) |
| `CI_REGISTRY_PASSWORD` | GitLab Access Token یا Password (اگر private registry داری)  |
| `KUBECONFIG_DATA`      | محتویات `~/.kube/config` به صورت Base64 شده                  |
| `DOCKER_PASS`      | pass                   |
| `KUBECONFIG_DATA`      | محتویات کیوب کانفیگ کلاستر برای اتصال گیت لب بیس 64                  |


```bash
cat ~/.kube/config | base64 -w 0
```

---

## ✅ نتیجه نهایی

با هر بار push به شاخه `main`:

1. ایمیج ساخته می‌شه با tag جدید (SHA commit)
2. به GitLab Registry push می‌شه
3. deployment در Kubernetes آپدیت می‌شه با ایمیج جدید

---

اگر بخوای فایل YAML deployment و service رو هم در قالب یک Helm chart برای استفاده حرفه‌ای‌تر تنظیم کنم یا دیپلوی با ArgoCD راه بندازم، کافیه بگی.

آیا می‌خوای این CI رو با Helm ادغام کنم هم؟

