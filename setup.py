from distutils.core import setup

setup(
    name='django-countries-plus',
    version='0.1.2',
    author='Andrew Cordery',
    author_email='cordery@gmail.com',
    packages=['countries_plus',],
    url='http://pypi.python.org/pypi/django-countries-plus/',
    license='LICENSE.txt',
    description='A django model & fixture containing all data from the countries table of Geonames.org',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.2",
    ],
)
