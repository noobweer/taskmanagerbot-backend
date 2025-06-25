FROM python:3.12-alpine3.20

WORKDIR /taskmanager-backend
COPY requirements.txt .
COPY taskmanager-backend .
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password taskmanager-user

user taskmanager-user

EXPOSE 8000
