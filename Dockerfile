FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN virtualenv env --python=python3.10

RUN source/env/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 120

ENV FLASK_APP=core/server.py

CMD ["bash", "run.sh"]