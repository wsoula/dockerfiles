FROM golang
RUN git clone https://github.com/nkanaev/numb.git
RUN cd numb && go get -d ./... && go build
ENTRYPOINT ["numb/numb"]
