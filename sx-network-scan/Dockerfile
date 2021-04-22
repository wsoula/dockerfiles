FROM golang
# Install base packages
RUN apt update && apt upgrade -y
RUN apt-get install -y git libpcap-dev
# Install sx
RUN git clone https://github.com/v-byte-cpu/sx /var/tmp/sx && ls /var/tmp/sx
RUN cd /var/tmp/sx && go build
RUN ls /var/tmp/sx
ENTRYPOINT ["/var/tmp/sx/sx"]
