FROM python:3.9-slim-buster
ARG ver
RUN pip install mwdstdcore[gunicorn]==${ver}

ENTRYPOINT ["gunicorn", "mwdstdcore.server:app"]
