FROM alpine
ENV version=0.30.0
WORKDIR /var/tmp/
RUN apk add curl
RUN curl -L -O https://github.com/noborus/ov/releases/download/v${version}/ov_${version}_linux_amd64.zip
RUN unzip ov_${version}_linux_amd64.zip
WORKDIR /tmp
ENTRYPOINT ["/var/tmp/ov"]
