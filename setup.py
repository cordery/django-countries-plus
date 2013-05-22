from distutils.core import setup

setup(
    name='django-countries-plus',
    version='0.1.0',
    author='Andrew Cordery',
    author_email='cordery@gmail.com',
    packages=['countriesplus',],
    url='http://pypi.python.org/pypi/django-countries-plus/',
    license='LICENSE.txt',
    description='A django model & fixture containing all data from the countries table of Geonames.org',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.2",
    ],
)
