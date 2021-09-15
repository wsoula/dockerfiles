ascii-image-converter
---
https://github.com/TheZoraiz/ascii-image-converter

Build using this dockerfile

`docker build . -t ascii-image-converter`

Create alias to use the built container

`alias ascii-image-converter=docker run -t -v "$(pwd)":/tmp/aic  ascii-image-converter -b /tmp/aic/image.jpeg`
