FROM jupyterhub/jupyterhub:4.0.2

COPY ./conf /conf/

RUN pip install --upgrade pip && \
    pip install --upgrade dockerspawner && \
    pip install --upgrade jupyter_client && \
    curl -sfSL https://get.docker.com | sh

EXPOSE 8000
EXPOSE 8081

ENTRYPOINT [ "jupyterhub" ]

CMD [ "-f", "/conf/jupyterhub_config.py" ]
