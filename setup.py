#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from os import path
from setuptools import setup

from pyload import __license__, __status__, __status_code__, __version__


PROJECT_DIR = path.abspath(path.join(__file__, ".."))

setup(
    name="pyload",
    version=__version__,
    description='Fast, lightweight and full featured download manager.',
    long_description=open(path.join(PROJECT_DIR, "README.md")).read(),
    keywords=('pyload', 'download-manager', 'one-click-hoster', 'download'),
    url="http://pyload.org",
    download_url="https://github.com/pyload/pyload/releases",
    license=__license__,
    author="pyLoad Team",
    author_email="support@pyload.org",
    platforms=('Any',),
    #package_dir={'pyload': 'src'},
    packages=['pyload'],
    #package_data=find_package_data(),
    #data_files=[],
    include_package_data=True,
    exclude_package_data={'pyload': ["docs*", "locale*", "tools*"]},  #: exluced from build but not from sdist
    install_requires=[
        "Beaker >= 1.6", "Getch", "MultipartPostHandler", "SafeEval",
        "bottle >= 0.10.0", "jinja2", "markupsafe", "pycurl",
        "rename_process", "thrift >= 0.8.0", "wsgiserver"
    ],
    extras_require={
        'Few plugins dependencies': ["BeautifulSoup >= 3.2, < 3.3"]
        'Colored terminal': ["colorama"]
        'Colored log': ["colorlog"]
        'Lightweight webserver': ["bjoern"]
        'RSS parsing': ["feedparser"]
        'SSL connection': ["pyOpenSSL"]
        'RSDF/CCF/DLC decrypting': ["pycrypto"]
        'Captcha recognition': ["PIL"]
        'JSON speedup': ["simplejson"]
    },
    #setup_requires=["setuptools_hg"],
    #test_suite='nose.collector',
    #tests_require=['nose', 'websocket-client >= 0.8.0', 'requests >= 1.2.2'],
    entry_points={
        'console_scripts': [
            'pyload = pyload.Core:main',
            'pyload-cli = pyload.cli.Cli:main'
        ]},
    zip_safe=False,
    classifiers=[
        "Development Status :: %(code)s - %(status)s" % {'code': __status_code__, 'status': __status__},
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: " + __license__,
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP"
    ]
)
