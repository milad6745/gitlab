در YAML (که معمولاً در CI/CD ابزارهایی مثل GitLab CI, GitHub Actions, CircleCI و غیره استفاده می‌شه)، **anchors** و **aliases** برای **بازاستفاده از کد** استفاده می‌شن تا از تکرار جلوگیری کنن.

### 📌 تعریف Anchor و Alias در YAML

* **Anchor (`&`)**: برای تعریف یک بلاک قابل بازاستفاده.
* **Alias (`*`)**: برای استفاده مجدد از بلاکی که قبلاً با Anchor تعریف شده.

---

### 🧪 مثال ساده:

```yaml
.defaults: &defaults
  image: node:18
  before_script:
    - npm install

build-job:
  <<: *defaults
  script:
    - npm run build

test-job:
  <<: *defaults
  script:
    - npm test
```

🔍 در این مثال:

* `.defaults` یک anchor با نام `defaults` است (علامت `&`).
* در هر job (`build-job` و `test-job`) با `<<: *defaults` محتویات آن anchor را وارد می‌کنیم.

---

### ✅ مزایا:

* جلوگیری از تکرار (DRY - Don’t Repeat Yourself)
* راحت‌تر کردن نگهداری فایل‌های YAML
* خوانایی و سازمان‌دهی بهتر

---

اگه داری با یک ابزار خاص مثل GitLab CI یا GitHub Actions کار می‌کنی و می‌خوای مثال اون رو ببینی، بگو تا دقیق‌تر راهنمایی‌ت کنم.
