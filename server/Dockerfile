FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY main.py config.py boot.sh init.py ./
RUN chmod a+x boot.sh

RUN mkdir db
RUN touch db/app.db

ENV FLASK_APP main.py

EXPOSE 5000
ENTRYPOINT ADMIN_LOGIN=$ADMIN_LOGIN ADMIN_PASSWORD=$ADMIN_PASSWORD ./boot.sh
