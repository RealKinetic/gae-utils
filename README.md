Google App Engine Utiltites
===========================

This package is meant to be a set of utilities and scripts to help with the
development environment of developing Google App Engine standard (and flex)
applications.

gae-link-libs
-------------

AppEngine Standard has a very restrictive sandbox and the typical virtual env
does not usally work well with it. This library symlinks distributions listed
in your ``Pipfile.lock`` (via pipenv) or standard ``requirements.txt``. This
allows the pacakges installed in your virtual environment to be deployed to
AppEngine with minimal fuss and effort.

### Usage:

gae-link-libs --help
