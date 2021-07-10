FROM python:3

COPY . /harkn

WORKDIR /harkn

RUN pip install -r requirements.txt
