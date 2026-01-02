#!/usr/bin/env python3
"""
Setup script for the Experimental Habitat System
"""

from setuptools import setup
import os

# Read the README for long description
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='experimental-habitat',
    version='1.0.0',
    description='A safe, isolated containment system for experimental code',
    long_description=read_file('HABITAT_README.md'),
    long_description_content_type='text/markdown',
    author='Anthony James Padavano',
    author_email='4-b100m@users.noreply.github.com',
    url='https://github.com/4-b100m/solve-et-coagula',
    license='MIT',

    # Package discovery
    py_modules=[
        'experimental_habitat_implementation',
        'habitat_manager',
        'interactive_habitat',
        'simple_habitat_demo',
        'complete_workflow_demo',
        'test_habitat_system'
    ],

    # Python version requirement
    python_requires='>=3.7',

    # No external dependencies - uses only standard library
    install_requires=[],

    # Optional development dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ]
    },

    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'habitat-manager=habitat_manager:main',
            'habitat-interactive=interactive_habitat:main',
            'habitat-demo=simple_habitat_demo:main',
            'habitat-workflow=complete_workflow_demo:main',
        ],
    },

    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],

    # Keywords
    keywords='experimental containment isolation habitat sandbox testing',

    # Include package data
    include_package_data=True,

    # Zip safe
    zip_safe=False,
)
