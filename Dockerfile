FROM python:3.11.4

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirement.txt /code/

RUN pip install -r requirement.txt

COPY . /code/
