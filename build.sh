#!/usr/bin/env bash
set -o errexit
make install && make collectstatic && make migrate
