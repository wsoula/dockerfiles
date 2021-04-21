FROM codesimple/elm:0.19
RUN apk add git
# Clean APK cache
RUN rm -rf /var/cache/apk/*
# Install Game
RUN cd / && git clone https://github.com/passiomatic/sunny-land.git
# Setup working dir
VOLUME ["/sunny-land"]
WORKDIR /sunny-land
ENTRYPOINT ["elm","reactor"]
