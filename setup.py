import os
from setuptools import setup, find_packages


package_name = "{{package_name}}"


python_requires = "{{USER_CODE}}"
# Justifications:
#   {{USER_CODE}}


dependency_links = {{USER_CODE}}
# Justifications:
#   {{USER_CODE}}


install_requires = {{USER_CODE}}
# Justifications:
#   {{USER_CODE}}


entry_points = {
    'console_scripts': [
        '{{package_name}} = {{package_name}}.__main__:{{package_name}}_cli',
        {{USER_CODE}}
    ],
    'gui_scripts': [
    ]
}


# ------------------------------------------------------------------------------

about = {}
with open(os.path.join(package_name, '__info__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=package_name,
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires=python_requires,
    dependency_links=dependency_links,
    install_requires=install_requires,
    entry_points=entry_points,
)
