# install gitlab runner

setting > CICD > gitlab runner > expand > new gitlab runner for project


کامند های زیر را بر روی runner اجرا میکنیم . یک سیستم لینوکس دیگر

# Download the binary for your system
sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

# Give it permission to execute
sudo chmod +x /usr/local/bin/gitlab-runner

# Create a GitLab Runner user
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# Install and run as a service
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo gitlab-runner start

سپس برای رجیستر کردن بک کد رجیستری در اختیار ما قرار گرفته است .


```
gitlab-runner register

https://gitlab.com

Enter the registration token:
glrt-xCgsUkcLpxuTEp184N
Verifying runner... is valid                        runner=xCgsUkcLp

Enter a name for the runner. This is stored only in the local config.toml file:
[myubuntu]: testrunner

Enter an executor: kubernetes, shell, docker, parallels, virtualbox, docker-windows, docker+machine, docker-autoscaler, instance, custom, ssh:
shell

Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!

Configuration (with the authentication token) was saved in "/etc/gitlab-runner/config.toml"

```
