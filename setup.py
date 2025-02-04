from setuptools import setup, find_packages
from os import getenv

setup(
    name='juke-box-hero',
    version=getenv('VERSION', '0.0.1'),
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    python_requires='>=3.13, <4',
    include_package_data=True,
    install_requires=[
        'pydantic~=2.10.6',
        'fastapi~=0.115.8',
    ],
    author='Steven Hatch',
    author_email='stevegreghatch@gmail.com',
    description='',
    long_description='',
    scripts=["app.py"]
)
