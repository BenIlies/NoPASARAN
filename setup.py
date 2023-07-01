import os
from setuptools import setup, find_packages
from pkg_resources import parse_requirements

with open("README.md", "r") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt file
requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = [str(req) for req in parse_requirements(f)]

setup(
    name="nopasaran",
    version="0.2.1",
    author="Ilies Benhabbour",
    author_email="ilies.benhabbour@kaust.edu.sa",
    description="NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenIlies/NoPASARAN",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'nopasaran = nopasaran.__main__:main'
        ]
    }
)
