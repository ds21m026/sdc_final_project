FROM python:3.8

EXPOSE 8000:8000
EXPOSE 443
EXPOSE 80

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY api.py ./api.py
COPY models ./models

RUN pip install -r requirements.txt

CMD uvicorn api:api --host=0.0.0.0 --port=8000
