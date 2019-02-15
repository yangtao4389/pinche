# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04

MAINTAINER yangtao

# Install required packages and remove the apt packages cache when done.
# add (the rest of) our code、
# 改成国内镜像
#RUN  cp /etc/apt/sources.list /etc/apt/sources.list.bak
#COPY sources.list  /etc/apt/
#RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
RUN rm -rf /var/lib/apt/lists/* &&\
    apt clean && \
    apt-get update && \
    apt-get upgrade -y
RUN apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	sqlite3 \
	vim\
	net-tools\
	curl\
	locales\
	tzdata


# 安装chrome实现自订购
RUN apt-get install -y  fonts-liberation libasound2 libnspr4 libnss3 libxss1 lsb-release xdg-utils libappindicator1\
     libindicator7\
     wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome*.deb
RUN apt-get install -f

# 安装rabbitmq实现celery
# RabbitMQ Dockerfile
# https://github.com/dockerfile/rabbitmq

# Install RabbitMQ.
ADD rabbitmq-start /usr/local/bin/
RUN apt-get install -y rabbitmq-server && \
    rabbitmq-plugins enable rabbitmq_management && \
    echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config && \
    chmod +x /usr/local/bin/rabbitmq-start

# Define environment variables.
ENV RABBITMQ_LOG_BASE /home/logs/rabbitmq
ENV RABBITMQ_MNESIA_BASE /data/rabbitmq/mnesia


# Define mount points.
VOLUME ["/home/logs",'/data/rabbitmq/mnesia','/home/logs/rabbitmq']





# Expose ports. rabbitmq 5672服务器端口，15672 web网页端口
EXPOSE 5672
EXPOSE 15672


# 实现时区支持
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata


#实现中文支持
RUN locale-gen zh_CN.UTF-8 &&\
  DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8


# 建立文件共享 运行容器的时候再说
#VOLUME /home/statistic /home/docker/code/

# 不要copy，做目录映射
#COPY . /home/docker/code/


RUN mkdir /root/.pip
COPY pip.conf /root/.pip/

RUN pip3 install -U pip setuptools
RUN pip3 install uwsgi
COPY requirements.txt /home/conf/
RUN pip3 install -r /home/conf/requirements.txt


RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# 进入目录
WORKDIR /home/
EXPOSE 80
CMD ["supervisord", "-n"]

