FROM ubuntu
RUN apt update
RUN apt install -y curl
ENV version=v1.10.0
RUN curl -Lo aic-$version.tar.gz https://github.com/TheZoraiz/ascii-image-converter/releases/download/$version/ascii-image-converter_Linux_amd64_64bit.tar.gz
RUN tar -xvf aic-$version.tar.gz
ENTRYPOINT ["./ascii-image-converter_Linux_amd64_64bit/ascii-image-converter"]
