Booki
---
https://github.com/winsbe01/booki

Build using this dockerfile

`docker build . -t booki`

`mkdir -p ~/.config/booki` on your local machine before running

Create alias to use the built container

`alias booki="docker run -v ~/.config/booki:/root/.config/booki -it --rm booki"`
