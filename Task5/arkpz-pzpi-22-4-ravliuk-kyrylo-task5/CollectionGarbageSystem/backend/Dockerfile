FROM python:3.13

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/migration.sh"]