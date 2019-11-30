from setuptools import setup, find_packages


setup(
    name = 'virtualbrain',
    version = '0.1.0',
    author = 'Yair Karin',
    description = 'Virtual Brain interactive system',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)