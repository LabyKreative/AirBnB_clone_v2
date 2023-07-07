#!/usr/bin/python3
# a Fabric script that generates a .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""
    now = datetime.now()
    archive_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
    archive_path = "versions/{}".format(archive_name)
    if not os.path.exists("versions"):
        os.makedirs("versions")
    result = local("tar -czvf {} web_static".format(archive_path))
    if result.succeeded:
        return archive_path
    return None
