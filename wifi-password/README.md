wifi-password
---
WIP - I believe requires linux to use the host network

https://github.com/sdushantha/wifi-password

Build using this dockerfile

`docker build . -t wifi-password`

Create alias to use the built container

`alias wifi-password="sudo docker run --rm -it --net="host" --privileged wifi-password"
