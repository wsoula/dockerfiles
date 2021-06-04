onefetch
---
https://github.com/o2sh/onefetch

Build using this dockerfile

`docker build . -t onefetch`

Create alias to use the built container and run only from root of repo

`alias onefetch="docker run -it --rm -v $(PWD):/tmp/onefetch onefetch /tmp/onefetch"`
