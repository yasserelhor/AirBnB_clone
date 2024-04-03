#!/usr/bin/python3
"""Python function to create a compressed .tgz file using Fabric."""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Creates a .tgz archive containing the contents of the web_static folder."""
    try:
        local('mkdir -p versions')
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
    except Exception:
        return None
