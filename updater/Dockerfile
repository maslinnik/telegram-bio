FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY config.py update_all.py ./

CMD [ "python", "-u", "update_all.py" ]
