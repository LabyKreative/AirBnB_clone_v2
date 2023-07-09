#!/usr/bin/python3
# a Fabric script that generates .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack.
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create an archive file of the directory web_static directory"""
    dt = datetime.utcnow().strftime('%Y%m%d%H%M%S')

    arc_file = "versions/web_static_{}.tgz".format(dt)
    print("Packing web_static to {}".format(arc_file))
    if not os.path.exists("versions"):
        local("mkdir versions")

    fab_file = local("tar -cvzf {} web_static".format(arc_file))
    if fab_file.succeeded:
        size = os.path.getsize(arc_file)
        print("web_static packed: {} -> {} Bytes".format(arc_file, size))
        return arc_file
    else:
        return None
