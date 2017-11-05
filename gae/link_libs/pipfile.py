"""
Pipfile support (typically via pipenv)
"""

from __future__ import absolute_import

import json

from . import base


__all__ = [
    'load_distributions'
]


def get_packages():
    """
    Returns a list of tuples containing the (package, root_dir) of the list of
    packages specified in the `Pipfile.lock`.
    """


def get_lockfile_distributions(lockfile, name):
    ret = {}
    installed_distributions = base.get_installed_distributions()

    for package in lockfile[name]:
        found = False

        for dist in installed_distributions:
            if dist.key == package:
                found = True
                ret[package] = dist

                continue

        if not found:
            raise EnvironmentError(
                'Could not find distribution {} (is it installed?)'.format(
                    package
                )
            )

    return ret


def load_distributions(lockfile_name):
    """
    Return a list of distributions based on the "default" section of the
    supplied `lockfile`.
    """
    with open(lockfile_name, 'rb') as fp:
        lockfile = json.loads(fp.read())

    return get_lockfile_distributions(lockfile, "default").values()
