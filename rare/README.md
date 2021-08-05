rare
---
https://github.com/zix99/rare

Build using this dockerfile

`docker build . -t rare`

Create alias to use the built container and run from location of file

`rare histo input.txt`

`alias rare='docker run -it --rm -v $(PWD):/tmp/rare rare --notrim'`
