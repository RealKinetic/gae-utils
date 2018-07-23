__all__ = [
    'description',
    'maintainer',
    'maintainer_email',
    'url',
    'version_info',
    'version',
]

version_info = (1, 0, 0)
version = '.'.join(map(str, version_info))

maintainer = 'Nick Joyce'
maintainer_email = 'nick.joyce@realkinetic.com'

description = """
Utility to help tame python dependencies with Google AppEngine Standard
""".strip()

url = 'https://github.com/RealKinetic/gae-utils'
