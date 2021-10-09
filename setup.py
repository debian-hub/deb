from setuptools import setup
from deb import __version__

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="debi",
    version=__version__,
    author="Jak Bin",
    author_email="jakbin4747@gmail.com",
    description="download and install deb packages from github and other resources",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/jakbin/deb",
    python_requires=">=3",
    install_requires=["tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords='deb,debian,github',
    packages=["deb"],
    entry_points={
        "console_scripts":[
            "deb = deb:main"
        ]
    },
    zip_safe=False,
)
