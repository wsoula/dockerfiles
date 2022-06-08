zk
---
https://github.com/coloradocolby/fsrx

Build using this dockerfile

`docker build . -t fsrx`

Create alias to use the built container and run only from root of repo

`alias fsrx="docker run -it --rm -v $(PWD):/tmp/fsrx fsrx"`
