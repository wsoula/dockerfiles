FROM python
RUN git clone https://github.com/winsbe01/booki.git
# makefile creates a folder in ~/.config, but doesn't create ~/.config
RUN mkdir /root/.config
RUN cd booki && make && make install
# Code expects nano
RUN apt-get update
RUN apt-get install nano
RUN ls /root/.config/booki
ENTRYPOINT ["/usr/local/bin/booki"]
