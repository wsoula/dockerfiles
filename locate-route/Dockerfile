FROM alpine
# Install base packages
RUN apk update
RUN apk upgrade
# Install Dependencies
RUN apk add git cmake g++ make
# Clean APK cache
RUN rm -rf /var/cache/apk/*
# Install nin
RUN git clone https://github.com/junaidrahim/locate-route && cd locate-route && mkdir build && cd build && cmake .. && make
RUN ls /locate-route
ENTRYPOINT ["/locate-route/build/locate_route"]
