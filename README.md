# windrvmap - Windows drive mapping tool

This tools allows to control the drive mapping in Windows 10.

It internally works by calling windows `subst` and `net use` commands and by parsing `stdout` and `stderr` commands output.

## Installation

### For users

Install the package [from GitHub](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
(venv) C:\Users\Adrien>pip install git+https://github.com/afaucon/pywindrvmap.git@v1.0.0
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

```python
>>> import windrvmap
>>>
>>> windrvmap.__author__
>>> windrvmap.__version__
>>>
>>> drives = windrvmap.Drives()
>>> drives.letters(windrvmap.PHYSICAL)
C
>>> drives.letters(windrvmap.NETWORK)
Z --> \\ComputerName\SharedFolder\Resource
>>>
>>> drives.letters(windrvmap.LOCAL)

>>>
>>> drives.letters(windrvmap.USED)
C: physical drive
Z --> \\ComputerName\SharedFolder\Resource
>>>
>>> drives.add('D', 'C:\\Data')
('Success', 'D drive successfully added')
>>>
>>> drives.D.subst
'C:\\Data'
>>>
>>> drives.letters(windrvmap.LOCAL)
['D']
>>>
>>> drives.remove('D')
('Success', 'D drive successfully removed')
```

### With the command line interface

```bash
(venv) C:\Users\Adrien>python -m windrvmap
(venv) C:\Users\Adrien>python -m windrvmap --kind=local
(venv) C:\Users\Adrien>python -m windrvmap --kind=available
(venv) C:\Users\Adrien>python -m windrvmap add D C:\Data
(venv) C:\Users\Adrien>python -m windrvmap remove D
```

Or directly:

```bash
(venv) C:\Users\Adrien>drives
(venv) C:\Users\Adrien>drives --kind=local
(venv) C:\Users\Adrien>drives --kind=available
(venv) C:\Users\Adrien>drives add D C:\Data
(venv) C:\Users\Adrien>drives remove D
```
