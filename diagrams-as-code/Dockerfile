FROM python
WORKDIR /var/tmp/
RUN apt update
RUN apt install -y graphviz xdg-utils
#RUN git clone https://github.com/dmytrostriletskyi/diagrams-as-code
#WORKDIR /var/tmp/diagrams-as-code
RUN pip3 install diagrams-as-code
WORKDIR /tmp
ENTRYPOINT ["diagrams-as-code"]
