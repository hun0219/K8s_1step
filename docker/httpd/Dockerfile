FROM httpd:2.4

# docker build --build-arg REPO_URL....
ARG REPO_URL=https://github.com/hun0219/hun0219.github.io

COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf


RUN ["apt-get", "update"]
#RUN apt-get update 같은거
RUN ["apt-get", "install", "vim", "-y"]
RUN ["apt-get", "install", "git", "-y"]
#RUN ["git", "clone", "${REPO_URL}", "/usr/local/apach2/blog"]
RUN git clone ${REPO_URL} /usr/local/apache2/blog
