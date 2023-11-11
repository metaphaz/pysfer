# Pysfer

[![jhc github](https://img.shields.io/badge/GitHub-metaphaz-181717.svg?style=flat&logo=github)](https://github.com/metaphaz) 
[![python](	https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)


Pysfer is a Python library for transfering data between python processes. With pysfer you can:

+ Acsess variables or data from different Python programs.
+ Acsess variables or data between 'Main program' and other procseses.
+ Access variables or data in same Python program.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pysfer.

```bash
pip install pysfer
```

## Usage

```python
import pysfer

# Update or create "my_var" with "Hello World" value
pysfer.default_synchronizer.update("my_var","Hello World!")

# Returns the value of "my_var"
new_var = pysfer.default_synchronizer.get("my_var")

# Delete "my_var" and its value
pysfer.default_synchronizer.delete("my_var")

# It can also read and write custom class values
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


p1 = Point(3, 4)
pysfer.default_synchronizer.update("p1", p1)

p2 = pysfer.default_synchronizer.get("p1", Point)
print(p2.x, p2.y) # Prints "3 4"
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)