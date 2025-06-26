#!/usr/bin/env python3
"""
TGameHub Setup Script
A collection of classic terminal-based games in Python
"""

from setuptools import setup, find_packages
import sys
import os

# Read the README file for long description
readme_path = os.path.join(os.path.dirname(__file__), 'ReadMe.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A collection of classic terminal-based games in Python"

# Read requirements
requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
requirements = []
try:
    with open(requirements_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Handle platform-specific requirements
                if ';' in line:
                    requirements.append(line)
                else:
                    requirements.append(line)
except FileNotFoundError:
    requirements = ['numpy>=1.21.0', 'chess>=1.999']

# Platform-specific requirements
if sys.platform.startswith('win'):
    requirements.append('windows-curses>=2.3.0')

setup(
    name="tgamehub",
    version="1.0.0",
    author="Licnex",
    description="A collection of classic terminal-based games in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Licnex/tgamehub",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Arcade",
        "Environment :: Console :: Curses",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tgamehub=Main:main_menu",
        ],
    },
    include_package_data=True,
    package_data={
        'Games': ['words.txt'],
    },
    keywords="games, terminal, console, retro, classic, snake, chess, tic-tac-toe",
    project_urls={
        "Bug Reports": "https://github.com/Licnex/tgamehub/issues",
        "Source": "https://github.com/Licnex/tgamehub",
        "Documentation": "https://github.com/Licnex/tgamehub#readme",
    },
)
