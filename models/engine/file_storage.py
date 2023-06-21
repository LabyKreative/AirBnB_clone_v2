#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
import shlex
from models.base_model import BaseModel  # noqa
from models.user import User  # noqa
from models.state import State  # noqa
from models.city import City  # noqa
from models.place import Place  # noqa
from models.amenity import Amenity  # noqa
from models.review import Review  # noqa


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The path to the file where objects are stored.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[key] = self.__objects[key]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Save the objects to the file in JSON format."""
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """Calls object reload from the file, if it exists."""
                try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete an existing element"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """calls reload()"""
        self.reload()
