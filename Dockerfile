FROM python:3.12.0a4-alpine3.17

WORKDIR /app

# RUN apk update
RUN apk add tor
RUN apk add nginx
RUN pip install Flask

RUN mkdir /etc/torrc.d
RUN mkdir /var/www/html/

COPY ./nginx.conf /etc/nginx/
COPY ./torrc /etc/tor/
COPY ./entry_point.sh /app/
COPY ./src/ /app/

RUN rm /etc/nginx/http.d/default.conf

ENTRYPOINT [ "/app/entry_point.sh" ]