FROM swaggerapi/swagger-ui

ARG PORT

ENV PORT=$PORT \ 
    SWAGGER_JSON="/app/openapi.yaml"

ADD ./openapi.yaml /app/openapi.yaml

EXPOSE $PORT
