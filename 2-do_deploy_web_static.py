#!/usr/bin/python3
# a Fabric script (based on the file 1-pack_web_static.py) that distributes
# an archive to your web servers, using the function do_deploy:
import os.path
from fabric.api import *
from datetime import datetime

env.hosts = ["100.26.154.241", "35.153.194.206"]
env.host = "ubuntu"
env.private_key = "~/.ssh/school"


def do_deploy(archive_path):
    """Sends an archive to the wae server """
    if not os.path.exists(archive_path):
        return False

    filename = archive_path.split("/")
    filename = filename[1]
    fname = filename.split('.')
    fname = fname[0]

    newpath = '/data/web_static/releases/{}/'.format(fname)

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(newpath))
        run("tar -xzf /tmp/{} -C {}".format(filename, newpath))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(newpath, newpath))
        run("rm -rf {}web_static".format(newpath))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(newpath))
        return True
    except:
        return False
