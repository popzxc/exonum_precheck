#!/usr/bin/env python
import setuptools

PYTHON_REQUIRES = ">=3.4"
INSTALL_REQUIRES = ["pyyaml"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exonum_precheck",
    version="0.1.5",
    author="Igor Aleksanov",
    description="Exonum precheck deployment script",
    url="https://github.com/popzxc/exonum_precheck",
    packages=["exonum_precheck"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
)
