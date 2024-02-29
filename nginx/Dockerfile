FROM ghcr.io/emenu124ru/django:latest AS server

#########################################

FROM nginx:1.19.2

COPY ./nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
