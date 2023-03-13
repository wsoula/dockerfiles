MimicMania
---
https://github.com/asciimoo/exrex

Build using this dockerfile (replaces code to set base url and garbage collection)

`docker build . -t exrex`

Create alias to use the built container

`alias exrex="docker run --rm -it --name exrex exrex"
