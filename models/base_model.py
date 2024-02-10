#!/usr/bin/python3

"""This file defines the BaseModel class,
which will serve as the base of our model."""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """The Base class for the project"""

    def __init__(self, *args, **kwargs):
        """Serialize and deserialize a class."""

        """Initialize if nothing is passed."""
        if kwargs == {}:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)
            return

        """Initialize using keyword arguments (deserialize)."""
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid4())
        self.id = kwargs['id']

        for Key, val in kwargs.items():
            if Key == "__class_":
                continue
        if "created_at" in kwargs:
            self.created_at = datetime.strptime(
                    kwargs['created_at'],
                    '%Y-%m-%dT%H:%M:%S.%f')
        if "updated_at" in kwargs:
            self.updated_at = datetime.strptime(
                    kwargs['updated_at'],
                    '%Y-%m-%dT%H:%M:%S.%f')

    def __str__(self):
        """Override the string representation of self."""
        fmt = "[{}] ({}) {}"
        return fmt.format(
                type(self).__name__,
                self.id,
                self.__dict__)

    def to_dict(self):
        """Return a dictionary representation of self."""
        temp = {**self.__dict__}
        temp['__class__'] = type(self).__name__
        temp['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        temp['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return temp

    def save(self):
        """Update the last updated variable."""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    @classmethod
    def all(cls):
        """Retrieve all current instances of cls."""
        return models.storage.find_all(cls.__name__)

    @classmethod
    def create(cls, *args, **kwargs):
        """Creates an Instance"""
        new = cls(*args, **kwargs)
        return new.id

    @classmethod
    def count(cls):
        """Get the number of all current instances of the class."""
        return len(models.storage.find_all(cls.__name__))

    @classmethod
    def destroy(cls, instance_id):
        """Deletes an instance"""
        return models.storage.delete_by_id(
            cls.__name__,
            instance_id
        )

    @classmethod
    def show(cls, instance_id):
        """Retrieve an instance"""
        return models.storage.find_by_id(
            cls.__name__,
            instance_id
        )

    @classmethod
    def update(cls, instance_id, *args):
        """Update an instance.

        If args has one element and it's a dictionary:
            Update by key-value pairs from the dictionary.
        Else:
            Update by the first argument being the key
            and the second argument being the value.
        """
        if not len(args):
            print("** attribute name missing **")
            return
        if len(args) == 1 and isinstance(args[0], dict):
            args = args[0].items()
        else:
            args = [args[:2]]
        for arg in args:
            models.storage.update_one(
                cls.__name__,
                instance_id,
                *arg
            )
