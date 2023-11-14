from typing import Any, Literal, IO
from typing_extensions import Self
import hashlib
from pathlib import Path

class GuardedFile:
    """
    A class for preventing race conditions when reading or writing files.
    It doesn't prevent underlying file to be completely guarded. It just prevents any GuardedFile instances from reading/writing to it.
    Like the std::unique_ptr<T> in C++
    """
    
    def __init__(self, file: str = "", mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        """
        Creates a new GuardedFile objects. Arguments are passed to the open() function
        """
        
        self.__has_file: bool = False
        self.__fd: None|IO[Any] = None
        self.__file_path: None|Path = None
        self.__file_hash: None|str = None
        self.__locked_by_self: bool = False
        
        if file:
            self.open(file=file, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener)
    
    def __del__(self) -> None:
        self.close()
        
    def __enter__(self) -> Self:
        self.lock(True)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.close()
        return False
    
    def lock(self, wait_for_unlock: bool=False) -> None|IO[Any]:
        """Locks the file

        Returns:
            IO[Any]: The underlying file descriptor.
        """
        if not self.__has_file or self.is_locked():
            if not wait_for_unlock:
                return None
        
        while self.is_locked():
            pass
        
        parent_path: Path = self.__file_path.parent.absolute()
        guard_file: Path = parent_path / f".{self.__file_hash}.lock"
        guard_file.touch()
        self.__locked_by_self = True
        
        return self.__fd
    
    def unlock(self) -> None:
        """
        Unlocks the file.
        """
        if not self.__has_file or not self.is_locked():
            return
        
        if not self.__locked_by_self:
            raise RuntimeError("This object did not locked the file!")
        
        parent_path: Path = self.__file_path.parent.absolute()
        guard_file: Path = parent_path / f".{self.__file_hash}.lock"
        guard_file.unlink()
    
    def is_locked(self) -> bool:
        """Checks whether the file is locked or not

        Returns:
            bool: True if file is locked, False otherwise
        """
        if not self.__has_file:
            return False
        
        parent_path: Path = self.__file_path.parent.absolute()
        guard_file: Path = parent_path / f".{self.__file_hash}.lock"

        return guard_file.exists()
    
    def is_locked_by_self(self) -> bool:
        """Returns whether the file is locked by this object or not.

        Returns:
            bool: True if the file is locked by this object. False otherwise.
        """
        return self.__locked_by_self
    
    def close(self) -> None:
        """
        Closes the file.
        """
        if not self.__has_file:
            return 

        if self.__locked_by_self:
            self.unlock()
        
        self.__fd.close()
        self.__has_file = False
        self.__fd = None
        self.__file_path = None
        self.__file_hash = None
        self.__locked_by_self = False
    
    def get_fd(self, wait_for_unlock=False) -> None|IO[Any]:
        """Returns the underlying file descriptor.

        Args:
            wait_for_unlock (bool, optional): If set to true, this thread waits for underlying file to be unlocked. Defaults to False.

        Returns:
            None|IO[Any]: Returns None if file is locked and wait_for_unlock is set to False. Returns the file descriptor otherwise
        """
        
        if not self.is_locked() or self.__locked_by_self:
            return self.__fd
        
        while wait_for_unlock:
            if not self.is_locked():
                return self.__fd
        
        return None
    
    def open(self, file: str, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None) -> None:
        """
        Open a file from given path. Arguments are passed to the open() function
        """
        if self.__has_file:
            self.close()
        
        if not file:
            return
        
        self.__fd: IO[Any] = open(file=file, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener)
        self.__file_path: Path = Path(file)
        if self.__file_path.absolute().is_dir():
            raise RuntimeError("Given file is a directory!")
        self.__file_path.touch()
        self.__file_hash: str = hashlib.md5(str(self.__file_path.absolute()).encode('utf-8')).hexdigest()
        self.__has_file = True
        self.__locked_by_self = False


def test() -> None:
    filename = 'test.txt'
    def test_func(inp=False):
        f1 = GuardedFile(filename, 'w')
        is_locked = f1.is_locked()
        print(is_locked)

        fd = f1.lock()
        print(fd)
        
        if is_locked:
            fd = f1.get_fd(True)
            f1.lock()
            f1.close()
        else:
            while True:
                if inp:
                    input('>>>')
                    f1.close()
                    break
    
    import threading
    import time
    
    t1 = threading.Thread(target=test_func, args=(True,))
    t2 = threading.Thread(target=test_func, args=(False,))
    t1.start()
    t2.start()
    time.sleep(2)
    t1.join()
    t2.join()
    

if __name__ == '__main__':
    test()
