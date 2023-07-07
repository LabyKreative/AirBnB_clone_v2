#!/usr/bin/python3
# a Fabric script (based on the file 2-do_deploy_web_static.py) that creates
# and distributes an archive to your web servers, using the function deploy:
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["100.26.154.241", "35.153.194.206"]


def do_pack():
    """Creates a tar gzipped archive fie web_static dir."""
    dt = datetime.utcnow()
    tar_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                             dt.month,
                                                             dt.day,
                                                             dt.hour,
                                                             dt.minute,
                                                             dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(tar_file)).failed is True:
        return None
    return tar_file


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    tar_file = archive_path.split("/")[-1]
    name = tar_file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(tar_file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(tar_file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(tar_file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Creates and distributes an archive to a web server."""
    tar_file = do_pack()
    if tar_file is None:
        return False
    return do_deploy(tar_file)
