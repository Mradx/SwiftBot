from setuptools import setup, find_packages

setup(
    name='translation_checker',
    version='0.1.0',
    description='A flake8 plugin to check for missing translation keys',
    packages=find_packages(),
    entry_points={
        'flake8.extension': [
            'TC001 = linting.translation_checker:TranslationCheckerPlugin',
        ],
    },
    install_requires=[
        'flake8',
        'flake8-plugin-utils',
    ],
)
