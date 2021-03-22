F-a-maze-ing
---
https://github.com/aPixelInSpace/F-a-maze-ing

Build using this dockerfile

`docker build . -t maze`

Create alias to use the built container

`alias maze="docker run --rm -it -v $PWD:/var/tmp/maze-output maze"`

And use like this

`maze s-rectangle -r 6 -c 10 : g-ortho : a-hk -s 1 : rt-ortho -e : o-file -p /var/tmp/maze-output/test.txt`
