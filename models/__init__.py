#!/usr/bin/python3

"""Initializes the module's global (singleton) variables."""

from .engine.file_storage import FileStorage
"""Retrieves the storage instance"""
storage = FileStorage()
storage.reload()
