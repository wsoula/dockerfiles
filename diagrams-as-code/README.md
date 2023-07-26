diagrams-as-code
---
https://github.com/dmytrostriletskyi/diagrams-as-code

Build using this dockerfile

`docker build . -t diagrams-as-code`

Create alias to use the built container

`alias diagrams-as-code="docker run --rm -it -v $(PWD):/tmp --name diagrams-as-code diagrams-as-code"`
