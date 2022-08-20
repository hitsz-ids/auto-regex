from os import path
from codecs import open
from setuptools import setup, find_packages

__version__ = '0.1.1'

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(current_dir, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = [x.strip() for x in f.read().split('\n')]

setup(
    name='opendlp',
    version=__version__,
    description='openDLP',
    long_description=long_description,
    url='https://github.com/hitsz-ids/openDLP',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
    ],

    keywords='privacy, dlp, data-protection, data-loss-prevention, sensitive-data-discovery',
    packages=find_packages(exclude=['docs', 'tests*', 'service']),
    include_package_data=True,
    author='histsz-ids',
    install_requires=install_requires,
    author_email='1337913069@qq.com'
)