from setuptools import setup
from setuptools import find_packages 

setup(
    name="nepygui",
    version="0.1",
    description='non-extraordinary python gui package',
    author='kleist0202',
    author_email='pk0202@protonmail.com',
    url='https://github.com/kleist0202/nepygui',
    # packages=find_packages(exclude=('tests*')),
    packages=['nepygui'],
    install_requires=[
        'pygame',
    ],
)
