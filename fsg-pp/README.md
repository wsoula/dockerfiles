Fsg-Pp
---
https://github.com/EngMarchG/Fsg-Pp

Build using this dockerfile

`docker build . -t fsg-pp`

Create alias to use the built container

`alias fsg-pp="docker run --rm -it -p 7860:7860 fsg-pp"
