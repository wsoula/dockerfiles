FROM nginx:alpine

WORKDIR /app

RUN apk add git && git clone https://github.com/Valent-in/pulseq.git /app/static

COPY ./nginx.conf /etc/nginx/nginx.conf
