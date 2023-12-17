from setuptools import find_packages, setup
from typing import List
Hyphen_E_DOT='-e .'
# Utility function to read requirements from a file
def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if Hyphen_E_DOT in requirements:
            requirements.remove(Hyphen_E_DOT)
        return requirements

# Setup configuration
setup(
    name="BreastCancer",
    version='0.0.1',
    author='Abhishek',
    author_email='abhishekdhapola100@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
