# Ansible Collection - `{{cookiecutter.ansible_namespace}}.{{cookiecutter.ansible_collection_name}}`

{{cookiecutter.description}}

This collection is an example of how to create a golang module for ansible.
Use it as a skeleton or to generate primes if you need them in ansible for some
reason :D

The main purpose of this is to enable the use of golang for the development of
ansible modules targeting multiple architectures, a current pain point with
ansible's binary modules.  For example, this may be used to target Linux on
ARM and amd64.  In my own case, I am targeting macOS and Linux.  This may also
be used to target Windows or any other obscure GOOS/GOARCH combination.

Enjoy!

## Customizing

To create your own prime seive module, you may update this module entirely with
search and replace.  It is name independent as is to make it easy to modify.

### Search and replace keywords
The keywords to change are as follows:

* `{{cookiecutter.ansible_namespace}}` - your namespace
* `{{cookiecutter.ansible_collection_name}}` - your collectionname
* `{{cookiecutter.ansible_module_name}}` - your module's name
* `{{cookiecutter.author_name}}` - your name
* `{{cookiecutter.author_email}}` - your email address


### Steps
Making this into your own module requires some steps:

1) fork the `{{cookiecutter.ansible_collection_name}}` repo (a github fork or cloning and making a new one are both fine)
2) create your module (e.g. named `stuff_things`)
  1) create a folder with a go module (`go help mod init` at `golang_modules/stuff_things`
  2) copy `plugins/action/{{cookiecutter.ansible_module_name}}.py` to `plugins/action/stuff_things.py`
  3) copy `plugins/modules/{{cookiecutter.ansible_module_name}}.py` to `plugins/modules/stuff_things.py`
  4) edit `plugins/modules/{{cookiecutter.ansible_module_name}}.py` to include documentation (this file only has docs)
3) modify galaxy.yml
  1) modify relevant fields, especially the namespace and author
  2) in `build_ignore` change `{{cookiecutter.ansible_module_name}}_*` to `stuff_things_*` (note the underscore -- this is to keep the binary module from accidentally going to ansible-galaxy -- it will be too large!)
4) modify `test/test-playbook.yml` with the new module and collection names
5) modify this README.md

### Adding architectures and operating systems

If you need a new GOOS/GOARCH combination, you may need to edit
`plugins/action/{{cookiecutter.ansible_module_name}}.py` or whatever you renamed it to.

If the GOOS setting required is simply the output of uname on the host but
lowercase, the defaults will suffice.  If it's different, such as for `solaris`
which shows `SunOS`, modify it as follows:

```python3
_GOARCH_CONVERSIONS = {
    "x86_64": "amd64",
}
_GOOS_CONVERSIONS = {
    "sunos": "solaris",
}
```

Note the lowercase `sunos` in the map despite the uppercase `SunOS` in `uname`.
These maps are 100% lowercase for consistency.
