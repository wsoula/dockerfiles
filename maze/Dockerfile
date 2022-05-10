FROM mcr.microsoft.com/dotnet/sdk:5.0
# Install base packages
#RUN apk update
RUN apt update && apt upgrade -y
#RUN apk upgrade
#RUN apk add curl wget bash
RUN apt-get install -y curl zip
# Clean APK cache
#RUN rm -rf /var/cache/apk/*
# Install maze
#RUN mkdir /var/tmp/maze
#RUN curl -Lo /var/tmp/maze/maze.zip https://github.com/aPixelInSpace/F-a-maze-ing/releases/download/v1.0/F-a-maze-ing.1.0.zip
RUN curl -Lo /var/tmp/maze.tar.gz https://github.com/aPixelInSpace/F-a-maze-ing/archive/refs/tags/v1.0.tar.gz
RUN cd /var/tmp && gunzip maze.tar.gz && tar -xvf maze.tar
RUN ls /var/tmp/
RUN mkdir /var/tmp/F-a-maze-ing-1.0/output
RUN cd /var/tmp/F-a-maze-ing-1.0 && dotnet build --output /var/tmp/F-a-maze-ing-1.0/output
RUN ls /var/tmp/F-a-maze-ing-1.0/output
#RUN chmod +x /var/tmp/F-a-maze-ing-1.0/Mazes
ENTRYPOINT ["/var/tmp/F-a-maze-ing-1.0/output/Mazes"]
