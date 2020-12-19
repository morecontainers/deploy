# docker-deploy

*WARNING* Alpha version not yet extensively tested.

Please try it out but do not trust it in a production environment!

## usage

Suppose we have a container called `prod` and we have staged (created, but not
started) a new container named `staged` which should replace `prod`.  Below
follows a mock log how that could work:

```
$ docker run -d --name=prod ubuntu:18.04 sleep inf
$ docker create --name=staged ubuntu:20.04 sleep inf
$ docker run --rm -v /var/run/docker.sock:/var/run/docker.sock morecontainers/deploy prod staged
INFO: deploy prod from staged
INFO: prod: stopping
INFO: prod: removing
INFO: staged: renaming to prod
INFO: prod: starting
$ docker run --rm -v /var/run/docker.sock:/var/run/docker.sock morecontainers/deploy prod staged
ERROR: staged container not found
$ docker create --name=staged ubuntu:20.04 sleep inf
$ docker run --rm -v /var/run/docker.sock:/var/run/docker.sock morecontainers/deploy prod staged
INFO: prod: deployment not needed
INFO: staged: removing
INFO: staged: removed
```
