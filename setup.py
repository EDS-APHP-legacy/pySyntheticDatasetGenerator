from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='sdgen',
      version='0.1',
      description='Synthetic Dataset Generator',
      long_description=readme(),
      # url='http://github.com/aphp/dsfaker',
      author='AP-HP',
      # author_email='wind@aphp.fr',
      # license='MIT',
      packages=['sdgen',
                'sdgen.jobpool',
                'sdgen.config'
                ],
      install_requires=[
            'numpy==1.12.0'
      ],
      zip_safe=False)
