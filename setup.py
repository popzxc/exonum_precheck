#!/usr/bin/env python
from distutils.core import setup

PYTHON_REQUIRES = ">=3.4"

setup(
    name="exonum_precheck",
    version="0.1",
    description="Exonum precheck deployment script",
    packages=["exonum_precheck"],
    install_requires=[],
    python_requires=PYTHON_REQUIRES,
)
