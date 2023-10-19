FROM python:3.10-slim

WORKDIR /app

COPY . /app

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["/app/wait-for-it.sh", "db:5432", "--", "flask", "run", "--host=0.0.0.0"]