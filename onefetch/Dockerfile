FROM ubuntu
RUN apt update
RUN apt install -y curl
ENV version=2.9.1
RUN curl -Lo onefetch-$version.tar.gz https://github.com/o2sh/onefetch/releases/download/v$version/onefetch-linux.tar.gz
RUN tar -xvf onefetch-$version.tar.gz
ENTRYPOINT ["./onefetch"]
