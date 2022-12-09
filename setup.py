#!/usr/bin/env python

import errno
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from with_2_6 import __doc__, __version__
except SyntaxError:
    from with_2_2 import __doc__, __version__

project_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(project_directory, 'README.rst')

readme_file = open(readme_path)
try:
    long_description = readme_file.read()
finally:
    readme_file.close()


def bdist_wheel_tag_check(tag, args=sys.argv):
    if 'bdist_wheel' not in args:
        return False
    if '--python-tag' in args and tag in args:
        return True
    if ('--python-tag=' + tag) in args:
        return True
    return False


if 'sdist' in sys.argv:
    # When building a source distribution, include all variants:
    modules = [
        'with_3_3',
        'with_2_6',
        'with_2_5',
        'with_2_2',
        'with_skulpt_2',
        'with_skulpt_3',
        'with_brython',
        # `with_transcrypt.js` is included in MANIFEST.in
    ]
else:
    # When not building a source distribution, we select
    # just the file for the matching Python version:
    modules = ['with_']

    path_setup_py_uses = os.path.join(project_directory, 'with_.py')
    if bdist_wheel_tag_check('py33'):
        source_path = os.path.join(project_directory, 'with_3_3.py')
    elif bdist_wheel_tag_check('py26.py30'):
        source_path = os.path.join(project_directory, 'with_2_6.py')
    elif bdist_wheel_tag_check('py25'):
        source_path = os.path.join(project_directory, 'with_2_5.py')
    elif bdist_wheel_tag_check('py22'):
        source_path = os.path.join(project_directory, 'with_2_2.py')
    elif sys.version_info >= (3, 3):
        source_path = os.path.join(project_directory, 'with_3_3.py')
    elif sys.version_info >= (2, 6):
        source_path = os.path.join(project_directory, 'with_2_6.py')
    elif sys.version_info >= (2, 5):
        source_path = os.path.join(project_directory, 'with_2_5.py')
    else:
        source_path = os.path.join(project_directory, 'with_2_2.py')
    try:
        os.unlink(path_setup_py_uses)
    except OSError as error:
        if error.errno != errno.ENOENT:
            raise
    try:
        link = os.link
    except AttributeError:
        link = os.symlink
    link(source_path, path_setup_py_uses)

setup(
    name='with-as-a-function',
    version=__version__,
    description=__doc__.split('\n')[0],
    long_description=long_description,
    license='0BSD',
    url='https://github.com/mentalisttraceur/python-with',
    author='Alexander Kozhevnikov',
    author_email='mentalisttraceur@gmail.com',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
    py_modules=modules,
)
