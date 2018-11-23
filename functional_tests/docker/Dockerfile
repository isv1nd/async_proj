FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

RUN mkdir /code
WORKDIR /code

ADD functional_tests/ /code
RUN pip install -r requirements.txt

CMD pytest -p no:cacheprovider -v functional_tests/