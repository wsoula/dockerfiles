polyglot
---
https://github.com/pranavbabura/polyglot

Build using this dockerfile

`docker build . -t polyglot`

Create alias to use the built container

`alias polyglot="docker run -it --rm -v $(PWD):/tmp/polyglot polyglot"`
