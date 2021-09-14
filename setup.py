import setuptools
from deb.a import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deb",
    version=__version__,
    author="Jak Bin",
    description="download and install deb packages from github",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakbin/anonfile-upload",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='deb packages github',

    packages=["deb"],

    entry_points={
        "console_scripts":[
            "deb = deb:main"
        ]
    }
)
