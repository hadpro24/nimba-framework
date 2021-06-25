from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='nimba-framework',
	long_description=long_description,
	long_description_content_type='text/markdown',
	package_data={
		"":['.py', '.html', '.css']
	}
)
