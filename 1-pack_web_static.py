#!/usr/bin/python3
# a Fabric script that generates a .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create an archive file of the directory web_static directory"""
    dt = datetime.utcnow()
    tar_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if local("mkdir -p versions").failed:
        return None

    result = local("tar -cvzf {} web_static".format(tar_file))
    if result.failed:
        return None

    size_result = local("wc -c {}".format(tar_file), capture=True)
    size = size_result.stdout.split()[0]

    print("web_static packed: {} -> {} Bytes".format(tar_file, size))

    return tar_file
