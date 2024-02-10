#!/usr/bin/python3

"""
Defines the City model, which inherits from BaseModel.
"""


from models.base_model import BaseModel


class City(BaseModel):
    state_id: str = ""
    name: str = ""
