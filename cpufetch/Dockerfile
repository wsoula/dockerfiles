FROM alpine
RUN apk update
RUN apk add git make gcc libc-dev
RUN git clone https://github.com/Dr-Noob/cpufetch
RUN cd cpufetch && make
ENTRYPOINT ["./cpufetch/cpufetch"]
