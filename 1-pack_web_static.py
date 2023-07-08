#!/usr/bin/python3
# a Fabric script that generates .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create an archive file of the directory web_static directory"""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    if os.path.isdir("versions") is false:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
