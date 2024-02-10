#!/usr/bin/python3
"""
Defines errors related to file storage.
"""


class InstanceNotFoundError(Exception):

    """Raised when an unknown id is passed as an argument."""

    def __init__(self, obj_id="", mod="BaseModel"):
        super().__init__(
                f"Insatnce of {mod} with id {obj_id} does not exist!")


class ModelNotFoundError(Exception):

    """Raised when an unknown module is passed as an argument."""
    def __init__(self, arg="BaseModel"):
        super().__init__(f"Model with name {arg} is not registered!")
