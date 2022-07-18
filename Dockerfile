FROM python:3.9-slim-buster as build-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install "poetry==1.1.13"
RUN python -m venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY ["pyproject.toml", "poetry.lock", "/app/"]
RUN poetry export --without-hashes -E gunicorn -f requirements.txt -o /requirements.txt && pip install --no-cache-dir -r /requirements.txt
COPY [".", "/app"]
RUN pip install .

FROM python:3.9-slim-buster as final
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=build-stage /venv /venv

ENTRYPOINT ["gunicorn", "mwdstdcore.server:app"]
