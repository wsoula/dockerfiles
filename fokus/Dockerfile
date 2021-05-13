FROM node
ENV version=0.4
WORKDIR /var/tmp/
RUN git clone https://github.com/pg07codes/fokus
WORKDIR /var/tmp/fokus
RUN sed -i "s/17.0.1/16.8.5/" package.json
RUN npm install
ENTRYPOINT ["yarn","dev"]
