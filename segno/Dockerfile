FROM alpine
# Install base packages
RUN apk update && apk upgrade
RUN apk add py3-pip
# Clean APK cache
RUN rm -rf /var/cache/apk/*
# Install nin
RUN pip3 install segno
RUN segno -h
ENTRYPOINT ["segno"]
#CMD ["segno"]
