from alpine
# Install base packages
RUN apk update
RUN apk upgrade
RUN apk add curl wget bash
# Install ruby
RUN apk add ruby ruby-dev build-base
# Clean APK cache
RUN rm -rf /var/cache/apk/*
# Install nin
RUN gem install json nin
RUN nin
ENTRYPOINT ["nin"]
