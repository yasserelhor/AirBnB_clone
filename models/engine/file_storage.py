#!/usr/bin/python3

"""
This file defines the storage system for the project.
It will use JSON format to either serialize or deserialize objects.
"""

import json
from json.decoder import JSONDecodeError
from .errors import *
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime


class FileStorage:
    """
    This will serve as an Object-Relational Mapping
    (ORM) interface to the database.
    Class private variables.
    """
    __objects: dict = {}
    __file_path: str = 'file.json'
    models = (
            "BaseModel",
            "User", "City", "State", "Place",
            "Amenity", "Review"
            )

    def __init__(self):
        """initializer"""
        pass

    def all(self):
        """Return all stored instances."""
        return FileStorage.__objects

    def new(self, obj):
        """Store a new object."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize stored objects and persist them in a file."""
        serialized = {
            key: val.to_dict()
            for key, val in self.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(serialized))

    def reload(self):
        """Deserialize persisted objects."""
        try:
            deserialized = {}
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.loads(f.read())
            FileStorage.__objects = {
                key:
                    eval(obj["__class__"])(**obj)
                    for key, obj in deserialized.items()}
        except (FileNotFoundError, JSONDecodeError):
            # No need for error
            pass

    def find_by_id(self, model, obj_id):
        """Find and return an element of the model by its id."""
        file = FileStorage
        if model not in file.models:
            # Invalid Model Name
            # Not yet Implemented
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in file.__objects:
            # invalid id
            # Not yet Implemented
            raise InstanceNotFoundError(obj_id, model)

        return file.__objects[key]

    def delete_by_id(self, model, obj_id):
        """Find and return an element of the model by its id."""
        file = FileStorage
        if model not in file.models:
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in file.__objects:
            raise InstanceNotFoundError(obj_id, model)

        del file.__objects[key]
        self.save()

    def find_all(self, model=""):
        """Find all instances or instances of the model."""
        if model and model not in FileStorage.models:
            raise ModelNotFoundError(model)
        results = []
        for key, val in FileStorage.__objects.items():
            if key.startswith(model):
                results.append(str(val))
        return results

    def update_one(self, model, iid, field, value):
        """Update an instance."""
        file = FileStorage
        if model not in file.models:
            raise ModelNotFoundError(model)

        key = model + "." + iid
        if key not in file.__objects:
            raise InstanceNotFoundError(iid, model)
        if field in ("id", "updated_at", "created_at"):
            return
        inst = file.__objects[key]
        try:
            vtype = type(inst.__dict__[field])
            inst.__dict__[field] = vtype(value)
        except KeyError:
            inst.__dict__[field] = value
        finally:
            inst.updated_at = datetime.utcnow()
            self.save()
