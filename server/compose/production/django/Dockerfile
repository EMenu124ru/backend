FROM python:3.10.5-slim-bullseye

ARG APP_HOME=/server

RUN apt-get update && apt-get install --no-install-recommends -y build-essential libpq-dev

WORKDIR ${APP_HOME}

COPY ./server ${APP_HOME}

RUN pip install poetry && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=django:django ./server/compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./server/compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=django:django ./server/compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY --chown=django:django ./server/compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]
