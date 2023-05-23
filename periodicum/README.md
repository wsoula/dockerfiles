Periodicum
---
https://github.com/KaeserOfHonour/Periodicum

Build using this dockerfile

`docker build . -t periodicum`

Create alias to use the built container

`alias periodicum="docker run --rm -it -p 5173:5173 periodicum"`

Run as daemon

`docker run --rm -d -p 5173:5173 periodicum`
