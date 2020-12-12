from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='trifusionviz',
    version='0.1',
    description='tri fusion visuel',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://twitter.com/david_cobac',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    license='CC-BY-NC-SA',
    keywords=['merge sort', 
    	      'sort',
              'tri'
              'tri fusion',
              'graphviz'],
    packages=find_packages(),
    python_requires='>3.5'
)
