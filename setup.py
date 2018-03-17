from setuptools import setup, find_packages
from mlresearchkit import __version__, __author__

setup(
    name='mlresearchkit',
    version=__version__,
    description='A toolkit to help you do machine learning research quickly',
    long_description=open('README.md', encoding='utf-8').read(),
    url='https://github.com/zafarali/mlresearchkit',
    author=__author__,
    author_email='zafarali.ahmed@gmail.com',
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha'
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'mlresearchkit=mlresearchkit.cli:main'
        ]
    }
)