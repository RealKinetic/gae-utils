from setuptools import find_packages, setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


def get_meta():
    mod_locals = {}
    with open('./gae/__about__.py') as about_file:
        exec(
            about_file.read(),
            mod_locals,
            mod_locals,
        )

    return dict(
        (k, v) for k, v in mod_locals.items() if k in mod_locals['__all__']
    )


def get_requirements(filename):
    try:
        from pip._internal.download import PipSession

        session = PipSession()
    except ImportError:
        print("IMPORTERROR")
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


meta = get_meta()
from pprint import pprint
pprint(meta)

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
