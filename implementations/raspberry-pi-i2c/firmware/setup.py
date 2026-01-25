#!/usr/bin/env python3
"""
On-Body Haptics - Raspberry Pi Setup Script
Installs the Octopulse haptic server and utilities
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read dependencies from requirements.txt
def read_requirements():
    requirements = []
    filepath = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name='octopulse-haptics',
    version='2.0.0',
    description='Raspberry Pi I2C haptic feedback server for wearable devices',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='On-Body Haptics Project',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/On-body-haptics',
    license='MIT',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=read_requirements(),

    python_requires='>=3.7',

    entry_points={
        'console_scripts': [
            'octopulse-server=octopulse_server:main',
            'octopulse-ip-display=utils.ip_display:main',
            'octopulse-gpio-check=utils.gpio_check:main',
            'octopulse-buzz-test=utils.buzz_test:main',
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Hardware',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    ],

    keywords='haptics i2c raspberry-pi drv2605 osc wearable tactile-feedback',

    project_urls={
        'Bug Reports': 'https://github.com/yourusername/On-body-haptics/issues',
        'Source': 'https://github.com/yourusername/On-body-haptics',
        'Documentation': 'https://github.com/yourusername/On-body-haptics/tree/main/docs',
    },
)
