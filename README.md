# Overview

This plugs data streaming sources into rabbitmq so they can be easily consumed and played around with.

## docker-compose

### environment

Depending on which service you're using, you'll need different environment variables for credentials, query configuration etc.

[docker-compose.yml](docker-compose.yml) declares the variables needed for each service in the `environment` sections.

These variables can simply be set in the shell you use to launch docker-compose, eg.

```
export CONSUMER_KEY="*********************"
export CONSUMER_SECRET="*********************"
export ACCESS_TOKEN_KEY="*********************"
export ACCESS_TOKEN_SECRET="*********************"
...

docker-compose up -d rabbitmq stream_twitter
```

### rebuild images

`docker-compose build`

### start subsystems

1. `docker-compose up -d rabbitmq` will start the rabbitmq service
2. `docker-compose up -d stream_twitter` will stream tweets to rabbitmq
3. `docker-compose up -d stream_reddit` will stream reddit submissions & comments to rabbitmq

### connect to rabbitmq from host

* rabbitmq is available at [http://localhost:5672](http://localhost:5672)
  * run `env/bin/python -m harkn.watch` to connect to the rabbitmq exchanges and stream messages
* rabbitmq management interface at [http://localhost:15672](http://localhost:15672)
  * user: `guest`
  * password: `guest`

### shutdown

`docker-compose down` will shut everything down.
