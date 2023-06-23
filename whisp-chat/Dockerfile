FROM node
WORKDIR /var/tmp/
RUN git clone https://github.com/maelswarm/whisp-chat
WORKDIR /var/tmp/whisp-chat
RUN npm i
#ENTRYPOINT ["node","app.js","--","--host"]
ENTRYPOINT ["node","app.js","--host"]
#ENTRYPOINT ["npm","run","dev","--","--host"]
