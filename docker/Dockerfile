FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt
