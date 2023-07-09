#!/usr/bin/python3
# a Fabric script that generates .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack.
import os
from datetime import datetime
from fabric.api import local, run, put


def do_pack():
    """Creates an archive files of the directory web_static directory"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(date)
    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(path))
        return path
    except:
        return None
