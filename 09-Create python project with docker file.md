## Create python project with docker file

میخواهیم با استفاده از فلاسک یک پروژه بنویسیم
### install flask

```
pip install flask
```

### Flask Project
```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
```


### create docker file
```
FROM python:3.8.0-slim
WORKDIR /app
ADD . /app
RUN pip install-trusted-host pypi.python.org Flask
ENV NAME Mark
CMD ["python", "app.py"]
```

### create gitlab-ci.yml
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
    - docker run --name pyappcontainer -p 9090:9090 pyapp
```



