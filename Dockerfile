FROM ubuntu:18.04

LABEL maintainer="rath3.14159@protonmail.com"

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get update & apt-get install -y python3-dev python3-pip

RUN apt-get -y update

RUN pip3 install numpy matplotlib pandas get-all-tickers pandas-datareader

WORKDIR /PyTA

COPY . .

ENTRYPOINT ["python3", "-u", "main.py"]