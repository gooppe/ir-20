FROM python:3.6

COPY . /app

RUN pip install /app

WORKDIR /workspace

ENTRYPOINT [ "bash" ]