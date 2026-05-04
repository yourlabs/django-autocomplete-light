from setuptools import setup, find_packages


setup(
    name='autocomplete-light',
    versioning='dev',
    setup_requires='setupmeta',
    packages=find_packages(),
    package_data={
        'autocomplete_light': ['static/autocomplete_light/*'],
    },
    extras_require=dict(
        test=[
            'pytest',
            'pytest-cov',
            'pytest-splinter',
            'selenium',
        ],
    ),
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/autocomplete-light',
    license='MIT',
    keywords='html autocomplete',
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
