FROM python:3.8
EXPOSE 8501:8501
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run streamlit.py --server.port=8501
