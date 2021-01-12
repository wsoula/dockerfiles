FROM alpine
RUN apk add curl jq fzf util-linux
RUN curl -L "https://git.io/tmpsms" > /var/tmp/tmpsms && chmod +x /var/tmp/tmpsms
ENTRYPOINT ["/var/tmp/tmpsms"]
