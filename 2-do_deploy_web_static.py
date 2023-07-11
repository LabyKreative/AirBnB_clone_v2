#!/usr/bin/python3
# a Fabric script (based on the file 1-pack_web_static.py) that distributes
# an archive to your web servers, using the function do_deploy:
import os
from fabric.api import *
from datetime import datetime

env.hosts = ["100.26.154.241", "35.153.194.206"]
env.user = "ubuntu"


def do_pack():
    """Create an archive file of the web_static directory"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    arc_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_arc = local("tar -cvzf {} web_static".format(arc_f_path))

    if t_gzip_arc.succeeded:
        return arc_f_path
    else:
        return None


def do_deploy(archive_path):
    """Sends an archive to a web server"""
    if os.path.exists(archive_path):
        arcd_file = archive_path[9:]
        new_ver = "/data/web_static/releases/" + arcd_file[:-4]
        arcd_file = "/tmp/" + arcd_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_ver))
        run("sudo tar -xzf {} -C {}/".format(arcd_file, new_ver))
        run("sudo rm {}".format(arcd_file))
        run("sudo mv {}/web_static/* {}".format(new_ver, new_ver))
        run("sudo rm -rf {}/web_static".format(new_ver))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_ver))

        print("New version deployed!")
        return True

    return False