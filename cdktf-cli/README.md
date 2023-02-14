See https://github.com/denstorti/cdktf-cli

Steps
---
* `curl -Ls https://github.com/denstorti/cdktf-cli/archive/refs/heads/master.zip | bsdtar -xvf-`
* `cd cdktf-cli-master`
* Edit the Makefile for the cdktf and terraform versions, update as necessary
* `make build`
* add an alias - `alias cdktf-cli='docker run -it --rm -v $pwd:/src -w "/src" cdktf-cli:latest sh'`
* init project (or any other cdktf command in existing project) - `cdktf-cli` then `cdktf init --template-python`
