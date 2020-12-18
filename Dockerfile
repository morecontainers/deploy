FROM alpine:3.12
RUN apk add python3 docker-py
COPY docker-redeploy /usr/lib/python3.8/site-packages/docker-redeploy
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
