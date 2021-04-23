from distutils.core import setup

setup(
    name='pirdocopt',
    version='1.0.3',
    packages=['pirdocopt'],
    license='MIT License',
    long_description=open('README.rst').read(),
    requires=open('requirements.txt').read().split()
)
