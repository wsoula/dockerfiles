FROM golang
# Install base packages
RUN apt update && apt upgrade -y
#RUN apt-get install -y git libpcap-dev
# Install seashells
ENV install_dir=/var/tmp/seashells-server
RUN git clone https://github.com/anishathalye/seashells-server $install_dir && ls $install_dir
WORKDIR $install_dir
# Change base url
RUN sed -i s%https://seashells.io/v/%http://127.0.0.1:8888/v/%g main.go
# Change garbage collection time
RUN sed -i "s/1 * 24/2 * 24/g" main.go
RUN go build
# Copy config
RUN cp env.sample env
RUN ls
ENTRYPOINT ["sh", "-c", "$install_dir/run.bash"]
# Running just the binary, no config
#ENTRYPOINT ["sh", "-c", "$install_dir/seashells-server"]
