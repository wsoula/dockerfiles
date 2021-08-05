FROM ubuntu
RUN apt update
RUN apt install -y curl
ENV version=0.2.0
RUN curl -Lo rare-${version}.tar.gz https://github.com/zix99/rare/releases/download/${version}/rare_${version}_Linux_x86_64.tar.gz
RUN tar -xvf rare-${version}.tar.gz
RUN mkdir /tmp/rare
WORKDIR "/tmp/rare"
ENTRYPOINT ["/rare"]
