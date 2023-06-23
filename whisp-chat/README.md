Whisp-Chat
---
https://github.com/maelswarm/whisp-chat

Build using this dockerfile

`docker build . -t whisp-chat`

Create alias to use the built container

`alias whisp-chat="docker run --rm -it -p 4321:4321 whisp-chat"`

To test it out with docker network start one container:

`docker run --rm -it -p 4321:4321 --name whisp-chat whisp-chat --src=172.17.0.2:4321 --dest=172.17.0.3:1234 --secret=foo:bar`

Then start another container to talk to it

`docker run --rm -it -p 1234:1234 --name whisp-chat2 whisp-chat -vh --src=172.17.0.3:1234 --dest=172.17.0.2:4321 --secret=foo:bar`

You should see "connected" in each terminal and can now send messages.  Theoretically should be able to run one and change the ip to
another computer on the network that will run the second container.  Or even across the internet if you routed it from your router.
