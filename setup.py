"""
Ggame package setup for pypi
"""

import setuptools
from ggame.__version__ import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ggame",
    include_package_data=True,
    version=VERSION,
    author="Eric Dennison",
    author_email="ericd@netdenizen.com",
    description="A lightweight sprite-based game and graphics framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BrythonServer/ggame",
    packages=setuptools.find_packages(exclude=["examples*"]),
    install_requires=("Pillow==2.9.0"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
