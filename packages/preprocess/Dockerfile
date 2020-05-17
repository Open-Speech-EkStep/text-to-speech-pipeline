FROM python:3.7

RUN mkdir /opt/preprocess/
WORKDIR /opt/preprocess/

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /opt/preprocess/