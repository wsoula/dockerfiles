FROM golang
RUN git clone https://github.com/irevenko/weebsay.git
RUN cd weebsay && go get -d ./... && go build
ENTRYPOINT ["weebsay/weebsay"]
