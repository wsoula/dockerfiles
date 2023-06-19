FROM golang
# Install base packages
RUN apt update && apt upgrade -y
# Install seashells
ENV install_dir=/var/tmp/fractals
RUN git clone https://github.com/joweich/fractals $install_dir && ls $install_dir
WORKDIR $install_dir
RUN go build
WORKDIR /tmp
ENTRYPOINT ["/var/tmp/fractals/fractals"]
