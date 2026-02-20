#!/usr/bin/env bash
set -o errexit
make install
make translate
make collectstatic
make migrate
