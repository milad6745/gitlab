## flake8
main.py

```yml
def say_hello():

    print("Hello, World!")


say_hello()
```



gitlab-ci
```yml
stages:
  - lint

lint:
  stage: lint
  image: python:3.8
  script:
    - pip install flake8
    - flake8 main.py
```
