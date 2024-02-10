from setuptools import setup, find_packages

setup(
	name='assignment0',
	version='1.0',
	author='Rahul Talari',
	author_email='rtalari@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)