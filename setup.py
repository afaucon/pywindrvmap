import os
from setuptools import setup, find_packages


package_name = "windrvmap"


python_requires = ">=3.8"
# Justifications:
#   Just tested with python 3.8


dependency_links = []
# Justifications:
#   No external dependancy


install_requires = [
    'Click',
]
# Justifications:
#   {{USER_CODE}}


entry_points = {
    'console_scripts': [
        'drives = windrvmap.cli_drives:main',
        'drives-cfg = windrvmap.cli_drives_cfg:main',
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
