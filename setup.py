from setuptools import setup, find_packages

setup(
    name='space-invaders-pygame',
    version='1.0.0',
    description='A simple Space Invaders-style arcade game built with Pygame.',
    author='Nathaniel Mina',
    packages=find_packages(),
    py_modules=['main', 'player', 'enemy', 'bullet'],
    install_requires=[
        'pygame>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'space-invaders=main:main'
        ]
    },
    python_requires='>=3.7',
)
