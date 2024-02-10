#!/usr/bin/python3
"""
This file defines the StateModel class.
"""


from models.base_model import BaseModel


class State(BaseModel):
    name: str = ""
