FROM python:latest


COPY . .
WORKDIR .

RUN pip install -r requirements.txt
