import os
from setuptools import setup,find_packages


setup(
        name = "USFQ_manager",
        version = '1.0',
        author = "GrupoRedes",
        author_email="robdres123@gmail.com",
        packages = find_packages(),
        description="A application to manage and control your network",
        entry_points={
        'console_scripts': [
            'my_application=my_application.cli:main',
        ],}
)

