FROM python:3.6
EXPOSE 9001
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt

CMD alembic upgrade head && python -m aiohttp.web -H 0.0.0.0 -P 9001 app:init_func