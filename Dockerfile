FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./* /code/
RUN pip install .
RUN cp /etc/peopledoc-test/resto.example.ini /etc/peopledoc-test/resto.ini
CMD ["resto-server"]
