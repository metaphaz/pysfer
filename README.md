# Pysfer

[![jhc github](https://img.shields.io/badge/GitHub-metaphaz-181717.svg?style=flat&logo=github)](https://github.com/metaphaz) 
[![python](	https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)


Pysfer is a Python library for transfering data between python procseses. With pysfer you can:

+ Acsess variables or data from different Python programs.
+ Acsess variables or data between 'Main program' and other procseses.
+ Access variables or data in same Python program.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pysfer
```

## Usage

```python
import pysfer

# update or create "my_var" with "Hello World" value
pysfer.localvar.update("my_var","Hello World!")

# returns the value of "my_var"
new_var = pysfer.localvar.get("my_var")

# delete "my_var" and its value
pysfer.localvar.delete("my_var")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)