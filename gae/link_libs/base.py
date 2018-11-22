from __future__ import absolute_import

import imp
import os.path

__all__ = [
    'get_installed_distributions',
    'link_distributions',
]


# distributions that can't ever work on appengine
ignored_distributions = [
    'cffi',
    'cryptography',
    'pip',
    'setuptools',
]


def get_installed_distributions():
    """
    Returns a list of all the packages that are installed in this current
    environment.
    """
    from gae.link_libs import pip
    
    return pip.get_installed_distributions()


def get_installed_dist(dist_name):
    installed_distributions = get_installed_distributions()

    for dist in installed_distributions:
        if dist.key == dist_name.lower():
            return dist

    raise EnvironmentError(
        'Missing distribution {} (is it installed?)'.format(dist_name)
    )


def get_packages_from_dist(dist):
    """
    Get a list of all the installed packages for this distribtion.
    """
    # yes, this is an ugly hack but nowhere can i find a simple api to
    # expose this information.
    return list(dist._get_metadata('top_level.txt'))


def get_dependencies(dist):
    """
    Returns a list of Distribution objects that the this distribution instance
    depends on.
    """
    for req in dist.requires():
        yield get_installed_dist(req.project_name)


def flatten_dependency_graph(distributions, seen=None):
    """
    Expands and flattens the set of distributions objects that are required
    """
    seen = seen or set()

    for dist in distributions:
        if dist in seen:
            continue

        seen.add(dist)

        seen.update(flatten_dependency_graph(get_dependencies(dist), seen))

    return list(seen)


def link_distributions(dest_directory, distributions, skip):
    """
    Add symlinks for all the packages installed for all the distributions
    supplied into the `dest_directory`.
    """
    seen = set()

    for dist in flatten_dependency_graph(distributions):
        if dist.key in ignored_distributions:
            continue

        if dist.key in skip:
            continue

        packages = get_packages_from_dist(dist)

        for package in packages:
            if package in seen:
                continue

            seen.add(package)

            source = os.path.join(dist.location, package)

            if not os.path.exists(source):
                source = imp.find_module(package)[1]
                package = os.path.basename(source)

            os.symlink(
                source,
                os.path.join(dest_directory, package)
            )
