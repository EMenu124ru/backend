FROM python:3.10.5-slim-bullseye AS server

WORKDIR /server

RUN apt-get update && apt-get install --no-install-recommends -y build-essential

COPY ./server/pyproject.toml /server/
COPY ./server/poetry.lock /server/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./server /server
RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.19.2

RUN rm -v /etc/nginx/nginx.conf
ADD ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
