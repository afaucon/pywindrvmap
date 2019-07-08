# Templated package

Write a small description of the package.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package.

```bash
pip install templated_package
```

Or install the package [from a CVS url](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
pip install git+https://github.com/afaucon/templated_package.git@v1.0.0
```

## Usage

```python
import templated_package

templated_package.pluralize('word') # returns 'words'
templated_package.pluralize('goose') # returns 'geese'
templated_package.singularize('phenomena') # returns 'phenomenon'
```
