NIN
---
https://github.com/aonemd/nin

Build using this dockerfile

`docker build . -t nin`

Create alias to use the built container

`alias nin="docker run --rm -it -v $HOME/.todos.yaml:/root/.todos.yaml nin"`
