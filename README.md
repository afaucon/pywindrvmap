# windrvmap - Windows drive mapping tool

This tools allows to control the drive mapping in Windows 10.

It internally works by calling windows `subst` and `net use` commands and by parsing `stdout` and `stderr` commands output.

## Installation

### For users

Install the package [from GitHub](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
(venv) C:\Users\Adrien>pip install git+https://github.com/afaucon/pywindrvmap.git@<git_tag_name>
(venv) C:\Users\Adrien>pip install git+https://github.com/afaucon/pywindrvmap.git@v1.0.1
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
>>> windrvmap.__version__
'1.0.0'
>>>
>>> drives = windrvmap.Drives()
>>>
>>> drives.letters(windrvmap.PHYSICAL)
['C']
>>>
>>> drives.letters(windrvmap.NETWORK_SHORTCUT)
['Z']
>>>
>>> drives.letters(windrvmap.LOCAL_SHORTCUT)
[]
>>>
>>> drives.letters(windrvmap.USED)
['C', 'Z']
>>>
>>> drives.add('D', 'C:\\Data')
('Success', 'D drive successfully added')
>>>
>>> drives.letters(windrvmap.LOCAL_SHORTCUT)
['D']
>>>
>>> drives.D.local_shortcut()
'C:\\Data'
>>>
>>> drives.remove('D')
('Success', 'D drive successfully removed')
>>>
```

### With the command line interface

Call `python -m windrvmap`, or `drives`.

Example:

```shell
(venv) C:\Users\Adrien>python -m windrvmap
C: physical drive
Y --> \\ComputerName\SharedFolder\Resource1
Z --> \\ComputerName\SharedFolder\Resource2

(venv) C:\Users\Adrien>drives
C: physical drive
Y --> \\ComputerName\SharedFolder\Resource1
Z --> \\ComputerName\SharedFolder\Resource2

(venv) C:\Users\Adrien>drives --kind=physical
C

(venv) C:\Users\Adrien>drives --kind=network
Y --> \\ComputerName\SharedFolder\Resource1
Z --> \\ComputerName\SharedFolder\Resource2

(venv) C:\Users\Adrien>drives --kind=local

(venv) C:\Users\Adrien>drives add D C:\Data
D drive successfully added

(venv) C:\Users\Adrien>drives --kind=local
D --> C:\Data

(venv) C:\Users\Adrien>drives remove D
D drive successfully removed
```
