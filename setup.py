from setuptools import setup

setup(
    name='codeowl',
    version='0.0.1',
    description='Code Finding Owl',
    author='Florian Ludwig',
    author_email='f.ludwig@greyrook.com',
    packages=['codeowl'],
    install_requires=[
        'pygments>=1.6,<2.0',
        'clint>=0.3.4',
        'argcomplete>=0.6.6,<1.0',
    ],
    entry_points={
        'console_scripts': [
            'owl = codeowl.cli:main',
        ],
    },
)
