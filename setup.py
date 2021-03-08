#!/usr/bin/env python
# Playwright Gym Visual Web envs for RL Agent training

from setuptools import setup, find_packages
import pathlib

parent_dir = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (parent_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="playwright_gym",  # Required
    version="0.0.1",  # Required
    description="Reinforcement Learning Environments for web-based tasks using Playwright",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/praveen-palanisamy/playwright-gym",  # Optional
    author="Praveen Palanisamy",  # Optional
    author_email="praveen.palanisamy@outlook.com",
    classifiers=[  # Optional
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="playwright-gym, rl web tasks, rl web navigation, rl in browser, Gym environments",  # Optional
    package_dir={"": "src"},  # Optional
    packages=find_packages(where="src"),  # Required
    include_package_data=True,
    python_requires=">=3.6, <4",
    install_requires=["gym"],
    project_urls={  # Optional
        "Source": "https://github.com/praveen-palanisamy/playwright-gym",
        "Author website": "https://praveenp.com",
    },
)
