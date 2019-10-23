#!/usr/bin/env bash

docker exec  $(docker ps -qf "name=redis")  redis-cli FLUSHALL