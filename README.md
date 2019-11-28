# windrvmap - Windows drive mapping tool

This tools allows to control the drive mapping in Windows 10.

## Installation

### For users

Install the package [from GitHub](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
(venv) C:\Users\Adrien>pip install git+https://github.com/afaucon/pywindrvmap.git@v0.0.1
(venv) C:\Users\Adrien>pip list
```

### For developpers

Clone the package from GitHub and install it in editable mode (i.e. [setuptools "develop mode"](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode)).

```bash
(venv) C:\Users\Adrien>git clone git+https://github.com/afaucon/pywindrvmap.git
(venv) C:\Users\Adrien>pip install --editable pywindrvmap
(venv) C:\Users\Adrien>pip list
```

## Usage

Within a python module:

```python
import windrvmap

windrvmap.__author__
windrvmap.__version__
```

```python
import windrvmap

windrvmap.service_1()
```

With the command line interface:

```bash
(venv) C:\Users\Adrien>python -m templated_package service_1
```

Or directly:

```bash
(venv) C:\Users\Adrien>templated_package service_1
```
