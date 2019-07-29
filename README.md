# Templated package

Write a small description of the package.

## Installation

### For users

Install the package [from GitHub](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
(venv) C:\Users\Adrien>pip install git+https://github.com/afaucon/templated_package.git@v0.0.1
(venv) C:\Users\Adrien>pip list
```

### For developpers

Clone the package from GitHub and install it in editable mode (i.e. [setuptools "develop mode"](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode)).

```bash
(venv) C:\Users\Adrien>git clone git+https://github.com/afaucon/templated_package.git
(venv) C:\Users\Adrien>pip install --editable templated_package
(venv) C:\Users\Adrien>pip list
```

## Usage

Within a python module:

```python
import templated_package

templated_package.__author__
templated_package.__version__
```

```python
import templated_package.module

templated_package.service_1()
```

With the command line interface:

```bash
(venv) C:\Users\Adrien>python -m templated_package service_1
```

Or directly:

```bash
(venv) C:\Users\Adrien>templated_package service_1
```
