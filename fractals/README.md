Fractals
---
https://github.com/joweich/fractals

Build using this dockerfile

`docker build . -t fractals`

Create alias to use the built container

`alias fractals="docker run --rm -it -v${PWD}:/tmp --name fractals fractals"

Copy locations.json to get a more interesting one:
https://raw.githubusercontent.com/joweich/fractals/main/locations.json
