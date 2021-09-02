import os

from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description. It's nice because now 1) we have a top-level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-autocomplete-light',
    version='3.9.0rc1',
    description='Fresh autocompletes for Django',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://django-autocomplete-light.rtfd.org',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    license='MIT',
    keywords='django autocomplete',
    install_requires=['six'],
    extras_require={
        'nested': ['django-nested-admin>=3.0.21'],
        'tags': ['django-taggit'],
        'genericm2m': ['django-generic-m2m'],
        'gfk': ['django-querysetsequence>=0.11'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
