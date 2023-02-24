MimicMania
---
https://github.com/everydaycodings/MimicMania

Build using this dockerfile (replaces code to set base url and garbage collection)

`docker build . -t mimicmania`

Create alias to use the built container

`alias mimicmania="docker run --rm -it -p 8501:8501 --name mimicmania mimicmania"
