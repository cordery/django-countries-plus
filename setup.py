from setuptools import setup, find_packages

setup(
    name='django-countries-plus',
    version='1.0.0',
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
        "Django >= 1.4",
        "requests>=2",
        "six>1"
    ],
    test_suite="runtests.runtests",
)
