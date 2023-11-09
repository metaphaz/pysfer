# Pyfer

[![jhc github](https://img.shields.io/badge/GitHub-metaphaz-181717.svg?style=flat&logo=github)](https://github.com/metaphaz) 
[![python](	https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)


Pyfer is a Python library for transfering data between python procseses. With pyfer you can:

+ Acsess variables or data from different Python programs.
+ Acsess variables or data between 'Main program' and other procseses.
+ Access variables or data in same Python program.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pyfer
```

## Usage

```python
import pyfer

# update or create "my_var" with "Hello World" value
pyfer.localvar.update("my_var","Hello World!")

# returns the value of "my_var"
new_var = pyfer.localvar.get("my_var")

# delete "my_var" and its value
pyfer.localvar.delete("my_var")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)