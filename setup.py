from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in process_manufacturing/__init__.py
from process_manufacturing import __version__ as version

setup(
	name="process_manufacturing",
	version=version,
	description="Process Manufacturing",
	author="Abhishek Chougule",
	author_email="chouguleabhis@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
