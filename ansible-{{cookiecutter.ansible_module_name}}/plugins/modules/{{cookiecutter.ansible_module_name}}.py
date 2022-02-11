#!/usr/bin/python

DOCUMENTATION = r'''
---
module: {{cookiecutter.ansible_module_name}}
short_description: Create a large prime with high probability
description: 
  - Creates a prime with the number of bits requested
  - Defaults to 2048 bits
  - The probability of being a prime is very high and is probabilistic
    rather than guaranteed due to the prime factorization problem.  This
    is the method generally used for generating primes for, e.g., RSA.
  - Uses https://pkg.go.dev/crypto/rand#Prime
  - Uses golang internally which must be installed on the operator machine
options:
  bits:  
    description:
      - the number of bits needed to represent the prime
      - also determines difficulty in factoring
    type: int
  _rebuild_golang_module:
    description:
      - causes the golang source code to be recompiled unconditionally
    type: bool
'''

EXAMPLES = r'''
- name: Generate a big ol' prime
  {{cookiecutter.ansible_namespace}}.{{cookiecutter.ansible_collection_name}}.{{cookiecutter.ansible_module_name}}:
    bits: 8192

- name: Recompile and generate a tiny prime to test
  {{cookiecutter.ansible_namespace}}.{{cookiecutter.ansible_collection_name}}.{{cookiecutter.ansible_module_name}}:
    bits: 10
    _rebuild_golang_module: yes
'''

from __future__ import absolute_import, division, print_function
__metaclass__ = type
