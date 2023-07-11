#!/usr/bin/python3
# a Fabric script that generates .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack.
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Create an archive file of the web_static directory"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    dt = datetime.now()
    arc_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second
    )
    try:
        print("Packing web_static to {}".format(arc_file))
        local("tar -cvzf {} web_static".format(arc_file))
        file_size = os.stat(arc_file).st_size
        print("web_static packed: {} -> {} Bytes".format(arc_file, file_size))
    except Exception:
        arc_file = None
    return arc_file
