from setuptools import setup

setup(
   name='PyTA',
   version='0.5.0',
   description='A python module for technical analysis',
   author='Ben Rathbone',
   author_email='rath3.14159@protonmail.com',
   packages=['PyTA'],
   install_requires=['numpy', 'matplotlib', 'pandas', 'get-all-tickers', 'pandas-datareader'],
)