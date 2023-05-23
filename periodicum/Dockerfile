FROM node
WORKDIR /var/tmp/
RUN git clone https://github.com/KaeserOfHonour/periodicum
WORKDIR /var/tmp/periodicum
RUN npm i
ENTRYPOINT ["npm","run","dev","--","--host"]
