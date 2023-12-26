from setuptools import (setup, find_packages)


setup(
    name='oqs',
    version='0.10.2',
    packages=find_packages(include=['oqs', 'oqs.*']),
    description=
    "OQS (Open Quick Script) is a Python library for interpreting versatile expressions, supporting basic to advanced "
    "operations, custom functions, and performance monitoring. It efficiently handles fundamental types and "
    "operations, interprets expressions using variables from dictionaries or JSON, and adheres to robust error "
    "handling standards. OQS enhances Python's expression evaluation capabilities, making it ideal for diverse "
    "applications.",
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
    license_files=('../LICENSE.md',),
)
