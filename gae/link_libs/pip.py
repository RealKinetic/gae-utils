"""
pip
"""

from __future__ import absolute_import

try:
    from pip import get_installed_distributions
except ImportError:
    from pip._internal.utils.misc import get_installed_distributions

try:
    from pip import req as pip_req
except ImportError:
    import pip._internal.req as pip_req


from . import base


__all__ = [
    'load_distributions',
    "get_installed_distributions",
]


def load_requirements(requirements):
    """
    Loads/parses a requirements.txt style file and returns a list of
    distributions that match.
    """
    ret = []

    for req in pip_req.parse_requirements(requirements, session=""):
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
