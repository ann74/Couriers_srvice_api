FROM python:3.10-alpine3.17

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD sh -c "alembic upgrade head && uvicorn app.main:app --host=0.0.0.0 --port=8080"