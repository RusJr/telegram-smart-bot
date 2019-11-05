FROM python:3.6.9-stretch
MAINTAINER Rus Jr

ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y nodejs

RUN mkdir /src 
ADD requirements.txt /src/
WORKDIR /src
RUN pip install -r requirements.txt
ADD /src/ /src/

CMD python run_telebot.py
