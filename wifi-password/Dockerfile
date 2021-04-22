FROM alpine
# Install base packages
RUN apk update && apk upgrade
# Clean APK cache
RUN rm -rf /var/cache/apk/*
RUN apk add git python3 curl py3-setuptools networkmanager
# Install setuptools
#RUN curl https://bootstrap.pypa.io/ez_setup.py -o - | python3
# Install wifi-password
#RUN python3 -m pip install wifi-password
RUN git clone https://github.com/sdushantha/wifi-password && \
    cd wifi-password && \
    python3 setup.py install
RUN wifi-password -h
ENTRYPOINT ["wifi-password"]
#CMD ["wifi-password"]
