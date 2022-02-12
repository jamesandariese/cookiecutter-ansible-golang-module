#!/bin/sh

cd /
yes '' | cookiecutter src
cd ansible-generate_prime
bash rebuild.sh
