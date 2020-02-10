import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pvcompare',
      version='0.0.1dev',
      description='Evaluating pv technologies in net zero energy communities.',
      url='https://github.com/greco-project/pvcompare',
      author='Reiner Lemoine Institut',
      # author_email='sabine.haas@rl-institut.de',
      license='MIT',
      packages=['pvcompare'],
      package_data={
          'pvcompare': [os.path.join('data', 'load_profiles', '*.csv'),
                        os.path.join('data', 'pv', '*.csv')]},
      long_description=read('README.md'),
      long_description_content_type='text/x-rst',
      zip_safe=False,  # todo
      python_requires=">=3.5, <4",
      install_requires=["pandas", "pvlib", "demandlib",
                        "scipy"],  # todo check if scipy is necessarily needed
      extras_require={
          'dev': ['pytest']})
