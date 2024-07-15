# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='dlis-invest',
    version="0.1.0",
    author="GIECAR - UFF",
    url="https://github.com/giecaruff/appy_core",
    description="dlis data library investigation",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8.8',
    install_requires=[
        "dlisio>=1.0.1",
        "numpy>=1.20.0",
        "pytest>=6.2.2, <6.2.5",
        "scipy>=1.4.1, <1.8.1",
        "scikit-learn>=0.22.1, <0.24.2",
        "jupyter==1.0.0",
        "matplotlib>=3.5.0, <3.5.3",
        "pandas==1.5.2",
    ],
)
