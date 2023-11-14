import json
import logging
from pathlib import Path
from guarded_file import GuardedFile
from typing import Any, Literal, IO
from typing_extensions import Self

class DataSynchronizer:
    def __init__(self, filename: str = '') -> None:
        """Create a new data synchronizer

        Args:
            filename (str, optional): The file path that you want to use for saving and reading. If left empty, it defaults to ./.pysfer/pysferlocaldata.json.
        """
        if filename:
            self.file_path = Path(filename)
        else:
            self.file_path: Path = Path(__file__).parent / ".pysfer/pysferlocaldata.json"
        
        self.file_path.parent.absolute().mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.touch()
            with GuardedFile(self.file_path.absolute(), 'w') as file:
                file.get_fd().write('{}')
        
        logging.basicConfig(filename=f'{self.file_path.parent.absolute() / "psyfer_logs.log"}',level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self) -> bool:
        return False
    
    def get(self, variable_name: str, class_type: type = None) -> Any:
        """Retrieves a variable by its name.

        Args:
            variable_name (str): The name of the variable that you want to retrieve.
            class_type (type, optional): If the saved variable is a dictionary and has a '__name__' field, You can pass the class to get an object from that class. Defaults to None.

        Returns:
            Any: Retrieved value
        """
        with GuardedFile(self.file_path.absolute(), 'r') as file:
            json_data: dict = json.load(file.get_fd(True))
            
            if variable_name not in json_data:
                logging.warning(f'Unable to get "{variable_name}"')
                return
            
            value: Any = json_data[variable_name]

            # If it is a class, create a new class instance using given class name.
            if type(value) is dict and '__name__' in value and value['__name__'] == class_type.__name__:
                value.pop('__name__')
                return class_type(**value)
            
            return value
    
    def update(self, variable_name: str, variable_value: Any) -> None:
        """Updates the value of the variable with given name.

        Args:
            variable_name (str): Name of the variable.
            variable_value (Any): New value of the variable.
        """
        
        with GuardedFile(self.file_path.absolute(), "r+") as file:
            json_data: dict = json.load(file.get_fd())
            var_type: type = type(variable_value)

            if hasattr(var_type, '__name__') and hasattr(variable_value, '__dict__'):
                vars_of_object = vars(variable_value)
                vars_of_object['__name__'] = type(variable_value).__name__
                json_data[variable_name] = vars_of_object
            else:
                json_data[variable_name] = variable_value
            
            self.__clear_file(file.get_fd())
            json.dump(json_data, file.get_fd())
    
    def delete(self, variable_name: str) -> None:
        """Deletes a variable by its name

        Args:
            variable_name (str): The name of the variable you want to delete.
        """
        
        with GuardedFile(self.file_path.absolute(), "r+") as file:
            json_data: dict = json.load(file.get_fd())
            if variable_name not in json_data:
                logging.warning(f'Cannot delete the variable: No variable with name "{variable_name}" exists!')
                return
            
            del json_data[variable_name]
            self.__clear_file(file.get_fd())
            json.dump(json_data, file.get_fd())
    
    def rename(self, current_name: str, new_name: str) -> None:
        """Renames a variable.

        Args:
            current_name (str): The current name of the variable
            new_name (str): New name of the variable
        """
        
        with GuardedFile(self.file_path.absolute(), "r+") as file:
            json_data: dict = json.load(file.get_fd())

            if not current_name in json_data:
                logging.warning(f'Cannot rename the variable: No variable with name "{current_name}" exists!')
                return
            
            json_data[new_name] = json_data[current_name]
            del json_data[current_name]
            
            self.__clear_file(file.get_fd())
            json.dump(json_data, file.get_fd())
        
    def get_content(self) -> None:
        """
        Retrieves the content of the file
        """
        with GuardedFile(self.file_path.absolute(), 'r') as file:
            return file.get_fd().read()
    
    def clear_content(self) -> None:
        """
        Clears the content of the file
        """
        with GuardedFile(self.file_path.absolute(), 'r+') as file:
            self.__clear_file(file.get_fd())
            file.get_fd().write('{}')
    
    def __clear_file(self, file_descriptor: IO[Any]) -> None:
        file_descriptor.seek(0)
        file_descriptor.truncate(0)


default_synchronizer = DataSynchronizer()

def test() -> None:
    # Basic stuff
    ds = DataSynchronizer("./.pysfer/custom.json")
    ds.update('myStr', 'Hello')
    ds.update('myInt', 42)
    ds.update('myFloat', 3.14)
    ds.update('myBool', True)
    ds.update('myList', ["This", "is", "a", "dummy", "list", 1.2, False])
    ds.update('myDict', {'a': 1, 'b': 2})
    
    # Loading custom objects
    class CustomClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    obj = CustomClass(3, 4)
    ds.update('obj', obj)
    print(ds.get('obj', CustomClass).x)

    # Deleting
    ds.update("somevar", 1234)
    ds.delete("somevar")

    # Renaming
    ds.update("foo", 1337)
    ds.rename("foo", "bar")
    print(ds.get("bar"))

if __name__ == '__main__':
    test()
