Nafas
---
https://github.com/pg07codes/fokus

Build using this dockerfile

`docker build . -t fokus`

Create alias to use the built container

`alias fokus="docker run --rm -it -p 8001:3000 fokus"`

Run as daemon

`docker run --rm -d -p 8001:3000 fokus`
