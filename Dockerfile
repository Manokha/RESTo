FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY README.md /code/
COPY setup.py /code/
COPY src /code/src
COPY config/resto.example.ini /code/resto.ini
COPY sql /code/sql
RUN pip install .
