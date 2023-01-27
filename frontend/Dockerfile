FROM python:3.8

EXPOSE 8501:8501

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY streamlit.py ./streamlit.py
COPY data ./data

RUN pip install -r requirements.txt

CMD ["streamlit run streamlit.py --server.port 8501 --server.address=0.0.0.0"]
