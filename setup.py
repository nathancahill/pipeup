
from setuptools import setup

setup(
    name='pipeup',
    version='0.1.1',
    packages=['pipeup'],
    install_requires=['click', 'websocket-client'],
    extras_require={
        'server': ['tornado'],
        'server-pubnub': ['tornado', 'pubnub', 'redis']
    },
    entry_points={
        'console_scripts': ['pipeup=pipeup.cli:main'],
    },
    author='Nathan Cahill',
    author_email='nathan@nathancahill.com',
    url='http://github.com/nathancahill/pipeup',
    keywords=['pipeup', 'pipe', 'stream', 'websockets'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    license='MIT',
    description='A command line tool for piping to a webpage',
    long_description=open('README.rst').read(),
)
