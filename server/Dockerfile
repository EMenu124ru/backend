FROM python:3.10.5-slim-bullseye

ARG MODE="--without dev"
ARG APP_HOME=/server

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev build-essential && \
    apt-get clean

COPY . ${APP_HOME}

WORKDIR ${APP_HOME}

RUN pip install poetry==1.5.1 && \
    poetry config virtualenvs.create false && \
    poetry install ${MODE} --no-interaction --no-ansi && \
    poetry cache clear --all .

RUN python ./manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]