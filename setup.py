from setuptools import find_packages, setup
from typing import List


def get_requirements()->List[str]:
    """
    Function to return requirements from requirements.txt as a list
    """
    requirements_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement!='-e .':
                    requirements_lst.append(requirement)
    
    except FileNotFoundError:
        print('requirements.txt file not found')
    
    return requirements_lst

setup(
    name='Network Security',
    version='0.0.1',
    author='Vikramjit Bora',
    author_email='vikramjitbora.pro@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements()
)