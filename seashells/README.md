Seashells
---
https://github.com/anishathalye/seashells-server

Build using this dockerfile (replaces code to set base url and garbage collection)

`docker build . -t seashells-server`

Create alias to use the built container

`alias seashells-server="docker run --rm -it -p 8888:8888 -p 1337:1337 --name seashells-server seashells-server"

Example usage:

`./infinite_loop.py| nc 127.0.0.1 1337` or `tail -f log.log | nc 127.0.0.1 1337`

`x=1; while true ; do clear ;  echo $x ; x=$((x+1)) ; sleep 1 ; done | nc 127.0.0.1 1337`

And visit the resulting url
