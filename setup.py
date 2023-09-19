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
    version='3.10.0-rc4',
    description='Fresh autocompletes for Django',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://django-autocomplete-light.rtfd.org',
    project_urls={
        'Source': 'https://github.com/yourlabs/django-autocomplete-light',
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    license='MIT',
    keywords='django autocomplete',
    install_requires=[
        'django>=3.2',
    ],
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
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
