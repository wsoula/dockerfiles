ov
---
https://github.com/noborus/ov

Build using this dockerfile

`docker build . -t ov`

Create alias to use the built container

`alias ov="docker run --rm -it -v $(PWD):/tmp ov Dockerfile"`
