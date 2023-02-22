Roguelike
---
https://github.com/fungamer2-2/Roguelike

Build using this dockerfile (replaces code to set base url and garbage collection)

`docker build . -t roguelike`

Create alias to use the built container

`alias roguelike="docker run --rm -it --name roguelike"

The `?` to bring up the controls doesn't work so here are the controls:
* `wsad` - up, down, left, right
* `t` - throw
* `u` - use
* `p` - pickup
* attack by running into monster
