from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pyrugga',
      version='1.2',
      description='A library to analyse Rugby matches using Opta\'s SuperScout files',
      url='https://github.com/jlondal/pyrugga',
      author='James Londal',
      license='GNU AFFERO GENERAL PUBLIC LICENSE',
      install_requires=[
         'pandas',
         'scipy',
         'scikit-learn',
         'matplotlib',
         'statsmodels',
         'sqlalchemy'
      ],
      packages=['pyrugga'],
      zip_safe=False,
      include_package_data=True
)
