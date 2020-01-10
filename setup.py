import setuptools

from peeweebuf.peeweebuf import __version__ as version

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(name="peeweebuf",
                 description='protocol buffer addons for peewee orm',
                 author='Brave Hager',
                 author_email='bravehager7@gmail.com',
                 license='MIT',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/bravehager/peeweebuf',
                 python_requires='>=3.6',
                 version=version)
