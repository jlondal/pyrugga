from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pyrugga',
      version='0.1',
      description='A collection of tools to help analyse opta XML files for Rugby matches',
      url='https://github.com/jlondal/pyrugga',
      author='James Londal',
      author_email='jameslondal@hearts-science.com',
      license='MIT',
      install_requires=[
         'pandas',
         'scipy',
         'scikit-learn',
         'matplotlib',
         'statsmodels',
      ],
      packages=['pyrugga'],
      zip_safe=False)
