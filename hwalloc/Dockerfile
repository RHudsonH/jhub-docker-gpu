FROM python:3.12

WORKDIR /app


ENV FLASK_APP=hwalloc
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


RUN pip install .

EXPOSE 5000

CMD ["flask", "--app", "hwalloc", "run", "--host=0.0.0.0", "--port=5000"]
