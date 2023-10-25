FROM python:3.12

WORKDIR /app

ENV FLASK_APP=hwalloc
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_INSTANCE_PATH='/instance'
ENV FLASK_CONFIG_FILE='/etc/hwalloc/config.py'

COPY app/. .
COPY hwalloc_config.py /etc/hwalloc/config.py
RUN pip install .

EXPOSE 5000

CMD ["flask", "run"]
