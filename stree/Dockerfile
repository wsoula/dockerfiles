FROM golang
#RUN git clone https://github.com/orangekame3/stree
#RUN cd numb && go get -d ./... && go build
RUN go install github.com/orangekame3/stree@latest
RUN cd ~ && pwd
ENTRYPOINT ["stree"]
