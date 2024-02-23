diagrams-as-code
---
https://github.com/nccgroup/ScoutSuite

Build using this dockerfile

`docker build . -t scout`

Create alias to use the built container

`alias scout="docker run --rm -it -v $(PWD):/tmp -v ~/.aws:/root/.aws --name scout scout"`
