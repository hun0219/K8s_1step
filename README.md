# K8s_1step
- https://hub.docker.com/_/httpd

# BUILD $ RUN
```bash

## 빌드
$ docker build -t my-apache2 .

## 실행
$ docker run -dit --name my-running-app -p 8949:80 my-apache2

## 컨테이너 안으로
$ docker exec -it my-running-app bash
```
