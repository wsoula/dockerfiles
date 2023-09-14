stree
---
https://github.com/orangekame3/stree

Build using this dockerfile

`docker build . -t stree`

Create alias to use the built container

`alias stree='docker run -it --rm -v ~/.aws:/root/.aws stree'`
