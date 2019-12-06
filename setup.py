from setuptools import setup, find_packages


setup(
    name = 'brainiac',
    version = '0.1.0',
    author = 'Yair Karin',
    description = 'Brainiac interactive system',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)