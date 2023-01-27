FROM python:3.8
EXPOSE 8000:8000
EXPOSE 443
EXPOSE 80
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD uvicorn api:api --host=0.0.0.0 --port=8000
