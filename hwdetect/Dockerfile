FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY app/. .

RUN pip install -r requirements.txt

CMD ["python", "detect_and_populate.py"]


