#!/usr/bin/env python3
"""Setup script for RPi Keyboard Config."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rpi-keyboard-config",
    version="1.0",
    author="Mathew Blowers",
    author_email="mathew.blowers@raspberrypi.com",
    description="RPi Keyboard Config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,

    py_modules=[
        "RPiKeyboardConfig",
    ],
    classifiers=[
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "rpi-keyboard-config=RPiKeyboardConfig.cli:main",
        ],
    },
)
