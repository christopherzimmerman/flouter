import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("src/flouter/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="flouter",
    version=version,
    url="https://github.com/christopherzimmerman/flouter",
    project_urls={
        "Code": "https://github.com/christopherzimmerman/flouter",
        "Issue tracker": "https://github.com/christopherzimmerman/flouter/issues",
    },
    license="BSD-3 Clause",
    author="Chris Zimmerman",
    author_email="chris@chriszimmerman.me",
    maintainer="Chris Zimmerman",
    maintainer_email="chris@chriszimmerman.me",
    description="Convenient routing for a flask application",
    long_description=readme,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=["flask>=1.1"],
    extras_require={
        "dev": ["pytest", "coverage", "sphinx"],
        "docs": ["sphinx", "numpydoc"],
    },
)
