#!/usr/bin/python3
"""
Defines the Amenity model, which inherits from BaseModel.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    name: str = ""
