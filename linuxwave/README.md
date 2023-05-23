linuxwave
---
https://github.com/orhun/linuxwave

Create alias to use the repo's pre-built container

`alias linuxwave=docker run --rm -v "$(pwd)":/app "orhunp/linuxwave:${TAG:-latest}"`
