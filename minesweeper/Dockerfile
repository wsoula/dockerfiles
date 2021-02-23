FROM alpine
# Install base packages
RUN apk update
RUN apk upgrade
RUN apk add git make g++
# Clean APK cache
RUN rm -rf /var/cache/apk/*
# Install nin
RUN mkdir /var/tmp/minesweeper && git clone https://github.com/unknownblueguy6/minesweeper.git /var/tmp/minesweeper
RUN cd /var/tmp/minesweeper && make
# RUN ./mine
ENTRYPOINT ["/var/tmp/minesweeper/mine"]
#CMD ["nin"]
