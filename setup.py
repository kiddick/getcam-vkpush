import os

from setuptools import find_packages, setup

NAME = 'getvkpush'
DESCRIPTION = 'TODO'
URL = 'TODO'
EMAIL = 'me@example.com'
AUTHOR = 'Me'
REQUIRES_PYTHON = '>=3.7.2'
VERSION = '0.1'

# TODO
REQUIRED = []

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages('.'),
    # py_modules=['shot'],
    entry_points={
        'console_scripts': ['run=app.main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

# pip install -e ../getcam
