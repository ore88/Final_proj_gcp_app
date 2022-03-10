FROM python:3.8

ENV PORT 80
ENV HOST 0.0.0.0

EXPOSE 80

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY ./requirements.txt

WORKDIR /Final_proj_gcp_app

RUN pip install -r requirements.txt

COPY . /app


CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app