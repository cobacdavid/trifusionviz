from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='trifusionviz',
    version='0.7',
    description='illustration du tri fusion',
    long_description_content_type='text/markdown',
    long_description=long_description,
    # url='https://twitter.com/david_cobac',
    url="https://github.com/cobacdavid/trifusionviz",
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    license='CC-BY-NC-SA',
    keywords=['merge sort',
    	      'sort',
              'tri',
              'tri fusion',
              'graphviz'],
    packages=find_packages(),
    install_requires=["graphviz"],
    python_requires='>3.5',
    scripts=['bin/tfv']
)
