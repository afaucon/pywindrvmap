# Templated package

Write a small description of the package.

## Installation

Install the package [from a CVS url](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
pip install git+https://github.com/afaucon/templated_package.git@v1.0.0
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

templated_package..module.run()
```

With the command line interface:

```bash
>> python -m templated_package
```

Or directly:

```bash
>> templated_package
```
