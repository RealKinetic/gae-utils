"""
pip
"""

from __future__ import absolute_import

import pip.req

from . import base


__all__ = [
    'load_distributions',
]


def load_requirements(requirements):
    """
    Loads/parses a requirements.txt style file and returns a list of
    distributions that match.
    """
    ret = []

    for req in pip.req.parse_requirements(requirements, session=""):
        req_name = req.req.name

        installed_dist = base.get_installed_dist(req_name)

        if not installed_dist:
            raise EnvironmentError(
                'Could not find distribution {} (is it installed?)'.format(
                    req_name
                )
            )

        ret.append(installed_dist)

    return ret


def load_distributions(requirements_name):
    """
    Return a list of distributions based on the "default" section of the
    supplied `lockfile`.
    """
    return load_requirements(requirements_name)
