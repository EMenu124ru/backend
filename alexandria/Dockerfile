FROM raisultan/alexandria:0.1

ARG PORT

ENV PORT=$PORT \ 
    ALEXANDRIA_YAML="/ws.yml"

ADD ./ws.yml /ws.yml

EXPOSE $PORT
