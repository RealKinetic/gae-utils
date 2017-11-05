from gae.__about__ import version_info as __version__info__
from gae.__about__ import version as __version__

from gae.link_libs.base import get_installed_distributions
from gae.link_libs.base import link_distributions


__all__ = [
    '__version__',
    '__version__info__',
    'get_installed_distributions',
    'link_distributions',
]
