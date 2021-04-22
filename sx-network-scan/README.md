SX
---
WIP - believe will only work on linux due to needing the host network

https://github.com/v-byte-cpu/sx

Build using this dockerfile

`docker build . -t sx`

Create alias to use the built container (I think the host network needs to be used otherwise the docker network is and nothing is returned)

`alias maze="docker run --rm --network host -it sx"`
