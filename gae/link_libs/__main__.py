from __future__ import absolute_import

import os.path
import shutil

import click

from . import base
from . import pip
from . import pipfile
from . import __version__


def find_requirements():
    """
    Attempts to automatically find requirements in the current path.

    :returns: (the implementation label, filename to reference)
    """
    if os.path.exists('Pipfile.lock'):
        return pipfile, 'Pipfile.lock'

    if os.path.exists('requirements.txt'):
        return pip, 'requirements.txt'


def determine_implementation(filename):
    """
    Based on the context of the supplied file, return the module that
    implements `load_distributions`.
    """
    try:
        pipfile.load_distributions(filename)
    except Exception:
        pass
    else:
        return pipfile

    try:
        pip.load_distributions(filename)
    except Exception:
        pass
    else:
        return pip

    raise ValueError(
        'Cannot determine requirements from {!r}'.format(filename)
    )


@click.command()
@click.option('-r', default=None, help=(
    'pip requirements file that contains the list of dependencies to link'
))
@click.option('-d', default='vendor', help=(
    'Destination directory for links'
))
@click.option('--force', is_flag=True)
@click.version_option(__version__)
def main(r, d, force):
    """
    Symlinks Python dependencies already installed in your environment to the
    vendor directory of your choice.

    Important note: The vendor directory will be wiped before the operation
    takes place.
    """
    if r is None:
        impl, r = find_requirements()
    else:
        impl = determine_implementation(r)

    click.echo('Linking requirements from {}'.format(r))

    distributions = impl.load_distributions(r)

    vendor_dir = os.path.join(os.getcwd(), d).encode('utf-8')

    if os.path.exists(vendor_dir):
        msg = 'Remove existing vendor dir {!r}?'.format(vendor_dir)

        if not force and not click.confirm(msg):
            raise click.Abort()

        shutil.rmtree(vendor_dir)

    if not os.path.exists(vendor_dir):
        os.mkdir(vendor_dir)

    base.link_distributions(
        vendor_dir,
        distributions,
        []
    )


if __name__ == '__main__':
    main()
