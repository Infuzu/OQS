from setuptools import (setup, find_packages)


setup(
    name='oqs',
    version='0.4.1',
    packages=find_packages(include=['oqs', 'oqs.*']),
    description=
    "OQS (Open Quick Script) is a Python implementation of a versatile expression language optimized for processing "
    "fundamental types and operations. It allows for interpreting expressions, optionally with variables in the form "
    "of dictionaries, maps, or JSON, to deliver consistent and logical results. Adhering to the OQS Specification, "
    "this implementation supports a variety of features including basic and advanced operations, custom functions, "
    "performance monitoring, and extensive error handling. Ideal for a wide range of applications, OQS simplifies "
    "expression evaluation and enhances Python's computational capabilities.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Infuzu',
    author_email='oqs@infuzu.com',
    url='https://github.com/Infuzu/OQS',
    license='Creative Commons Attribution 4.0 International License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license_files=('../LICENSE.md',)
)
