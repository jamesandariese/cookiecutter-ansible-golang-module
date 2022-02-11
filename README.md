# `cookiecutter-ansible-golang-module`

Template for making your own cross-platform ansible module in golang.

[![asciicast](https://asciinema.org/a/iev1hkmcXlwnRfZhfr7GPQs9v.svg)](https://asciinema.org/a/iev1hkmcXlwnRfZhfr7GPQs9v?speed=3)

## Usage

### Prerequisites

* [Cruft][1] or [Cookiecutter][2]
* [Ansible][3]
* [Golang][4]

If you use the defaults, you can run this to try out the cookiecutter template:

```bash
cruft create https://github.com/jamesandariese/cookiecutter-ansible-golang-module
cd ansible-generate_prime
bash rebuild.sh
ansible-doc -t module acme.samples.generate_prime
```

This will create a `samples` collection in the `acme` namespace.  In that
collection, there will be a `generate_prime` module which you can use in any
ansible playbook after running `rebuild.sh`.

### Cookiecutter

For using `cookiecutter` instead of `cruft`, use the following instead:
```bash
cookiecutter https://github.com/jamesandariese/cookiecutter-ansible-golang-module
```

### LICENSE

Ensure you update your license if you want to use something other than MIT.

[1]: https://github.com/cruft/cruft
[2]: https://github.com/cookiecutter/cookiecutter
[3]: https://github.com/ansible/ansible
[4]: https://go.dev
