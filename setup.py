from setuptools import setup, find_namespace_packages

setup(
    name='pocket_helper',
    version='1.0.0',
    description='adressbook',
    url='https://github.com/Vladosinfo/knowledge_base',
    author='Pasko Vladyslav, Yaremenko Valeriy, Prus Valerii, Tsybrovskyi Oleksii, Palamar Anna',
    author_email='vladyslav.pasko@gmail.com, prusvalerii@gmail.com, tsybrovsky@gmail.com, yar.valeriy@yahoo.com, anna.palamar1210@gmail.com',
    license='BSD',
    packages=find_namespace_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['pocket_helper = src.main:main']},
)
