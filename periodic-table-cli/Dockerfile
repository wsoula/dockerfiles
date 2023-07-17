FROM node
WORKDIR /var/tmp/
RUN git clone https://github.com/spirometaxas/periodic-table-cli
WORKDIR /var/tmp/periodic-table-cli
RUN npm install --global periodic-table-cli
ENTRYPOINT ["periodic-table-cli"]
