FROM python:3.11

WORKDIR /flaskr/build/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]