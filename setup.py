from setuptools import find_packages, setup

from pip.req import parse_requirements


def get_meta():
    mod_locals = {}

    execfile(
        'gae/__about__.py',
        mod_locals,
        mod_locals,
    )

    return dict(
        (k, v) for k, v in mod_locals.items() if k in mod_locals['__all__']
    )


def get_requirements(filename):
    try:
        from pip.download import PipSession

        session = PipSession()
    except ImportError:
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


meta = get_meta()


setup_args = dict(
    name='gae-utils',
    version=meta['version'],
    maintainer=meta['maintainer'],
    maintainer_email=meta['maintainer_email'],
    description=meta['description'],
    url=meta['url'],
    packages=find_packages(),
    namespace_packages=['gae'],
    install_requires=get_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'gae-link-libs = gae.link_libs.__main__:main',
        ]
    },
)


if __name__ == '__main__':
    setup(**setup_args)
