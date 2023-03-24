fspace
---
https://github.com/Mandrew0822/fspace

Build using this dockerfile (replaces code to set base url and garbage collection)

`docker build . -t fspace`

Create alias to use the built container

`alias fspace="docker run --rm -it --name fspace fspace"`
