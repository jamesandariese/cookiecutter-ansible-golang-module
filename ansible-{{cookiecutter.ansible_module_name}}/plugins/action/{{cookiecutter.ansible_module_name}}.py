#!/bin/python

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from pprint import pprint
from ansible.utils.display import Display
from pprint import pformat
import traceback
import subprocess
import os
import os.path

# The path elements from this action plugin's folder to the other ansible paths:
# Note: To use an absolute path, use "/" as the first element.
# For a collection-based hierarchy:
_GOLANG_MODULES_REL = ["..", "..", "golang_modules"]
_LIBRARY_REL        = ["..", "modules"]

# For a module developed locally:
#_GOLANG_MODULES_REL = ["..", "golang_modules"]
#_LIBRARY_REL        = ["..", "library"]

# The variable name which will cause this plugin to rebuild the module from
# source unconditionally (use for testing):
_REBUILD_MODULE_VAR = "_rebuild_golang_module"

display = Display()

_GOARCH_CONVERSIONS = {
    "x86_64": "amd64",
}
_GOOS_CONVERSIONS = {
}


def _goarch_converter(goarch):
    if goarch in _GOARCH_CONVERSIONS:
        return _GOARCH_CONVERSIONS[goarch]
    return goarch

def _goos_converter(goos):
    goos = goos.lower()
    if goos in _GOOS_CONVERSIONS:
        return _GOOS_CONVERSIONS[goos]
    return goos


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp # tmp isn't used anymore, free up the name to avoid confusion

        if 'ansible_system' not in task_vars or 'ansible_userspace_architecture' not in task_vars:
            raise AnsibleError("Must setup ansible_system and ansible_userspace_architecture via gather_facts or other means")

        ansible_system = task_vars['ansible_system']
        ansible_userspace_architecture = task_vars['ansible_userspace_architecture']

        module_logical_name = '.'.join(os.path.basename(self._original_path).split('.')[:-1])
        modname = f"{module_logical_name}_{ansible_system}_{ansible_userspace_architecture}"
        namespace = '.'.join(self._load_name.split('.')[1:-3])
        fqmn = f"{namespace}.{modname}"

        basepath = os.path.abspath(os.path.join(os.path.dirname(self._original_path), "..", ".."))
        golang_source_path = os.path.join(basepath, "golang_modules", module_logical_name)
        golang_outfile = os.path.join(basepath, "plugins" , "modules", modname)

        if _REBUILD_MODULE_VAR not in task_vars:
            task_vars[_REBUILD_MODULE_VAR] = False

        display.vvv(f"{_REBUILD_MODULE_VAR}={boolean(task_vars[_REBUILD_MODULE_VAR])}")
        if _REBUILD_MODULE_VAR in task_vars and boolean(task_vars[_REBUILD_MODULE_VAR]):
            display.vvv(f"____ DELETING EXISTING MODULE IF IT EXISTS ____")
            if os.path.exists(golang_outfile):
                display.vvv("it does so we are")
                os.unlink(golang_outfile)
    
        for trynum in (1, 2):
            try:
                result = self._execute_module(fqmn)
            except AnsibleError as e:
                if trynum == 1 and 'was not found in configured module paths' in str(e):
                    display.vvv("Attempting to build golang module")
                    env = dict(os.environ)
                    env["GOLANG_SOURCE_PATH"] = golang_source_path
                    env["OUTFILE"] = golang_outfile
                    env["GOOS"] = _goos_converter(task_vars['ansible_system'])
                    env["GOARCH"] = _goarch_converter(task_vars['ansible_userspace_architecture'])
                    display.vvv(subprocess.run(
                        "set -xe;cd \"$GOLANG_SOURCE_PATH\";go mod tidy;go build -o \"$OUTFILE\"".format(modname),
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        shell=True,
                        env=env,
                    ).stdout.decode('utf8'))
                else:
                    display.vvv("couldn't build so aborting instead")
                    raise e

        return result
