import os
import sys

from setuptools import setup, find_packages, Command


# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class RunTests(Command):
    description = "Run the django test suite from the test_project dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "test_project")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_from_command_line
        os.environ["DJANGO_SETTINGS_MODULE"] = 'test_project.settings'
        execute_from_command_line(argv=[ __file__, "test",
                        "autocomplete_light"])
        os.chdir(this_dir)

if 'sdist' in sys.argv:
    dir = os.getcwd()
    os.chdir(os.path.join(dir, 'autocomplete_light'))
    os.system('django-admin.py compilemessages')
    os.chdir(dir)

setup(
    name='django-autocomplete-light',
    version='2.2.8',
    description='Fresh autocompletes for Django',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://django-autocomplete-light.rtfd.org',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    license='MIT',
    keywords='django autocomplete',
    cmdclass={'test': RunTests},
    install_requires=[
        'six>=1.4',
    ],
    extras_require={
        'Tags': 'django-taggit',
        'Generic m2m': 'django-generic-m2m',
    },
    tests_require=[
        'django',
        'selenium',
        'django-cities-light',
        'mock',
        'lxml',
        'cssselect',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
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
