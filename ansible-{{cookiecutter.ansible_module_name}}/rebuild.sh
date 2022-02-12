#!/bin/sh

cd "$(dirname "$0")"
set -x
set -e

rm -rf .build
mkdir .build
ansible-galaxy collection build --force --output-path .build
ansible-galaxy collection install --force .build/*.tar.gz
(cd test ; ansible-playbook -vvv -i test-hosts.ini test-playbook.yml -e _rebuild_golang_module=yes) 
