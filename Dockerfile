FROM python:3.8-slim

WORKDIR /src

COPY . /src

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV PYTHONPATH /src

EXPOSE 5000

CMD ["python", "src/app.py"]
