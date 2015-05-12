
from setuptools import setup

setup(
    name='pipeup',
    version='0.0.1',
    packages=['pipeup'],
    entry_points={
        'console_scripts': ['pipeup=pipeup.cli:main'],
    },
    license='MIT',
    long_description=open('README.txt').read(),
)
