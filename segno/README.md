Segno
---
https://github.com/heuer/segno

Build using this dockerfile

`docker build . -t segno`

Create alias to use the built container

`alias segno='docker run --rm -it -v $PWD:/tmp segno'`

Then if you want to output to a file you can run below to generate it in the current directory
`segno -o /tmp/flimflam.png "FlimFlam"`

WiFi
---
`segno --scale 5 --output=/tmp/wifi_qr.png "WIFI:T:WPA;S:YourNetworkName;P:YourPassword;;"`
