from setuptools import setup, find_packages

setup(
    name='django-countries-plus',
    version='0.1.5',
    author='Andrew Cordery',
    author_email='cordery@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/django-countries-plus/',
    zip_safe=False,
    include_package_data=True,
    license='LICENSE.txt',
    description='A django model & fixture containing all data from the countries table of Geonames.org',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.2",
    ],
)
