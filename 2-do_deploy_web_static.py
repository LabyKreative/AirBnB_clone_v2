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

    # Create a folder to store the archive file.
    local("mkdir -p versions")
    logging.info("Folder versions/ created")

    # Use the current date and time to name the archive file.
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    arc_f_path = "versions/web_static_{}.tgz".format(date)

    # Create the archive file.
    local("tar -cvzf {} web_static".format(arc_f_path))
    logging.info("Archive file {} created".format(arc_f_path))

    # Return the path to the archive file.
    return arc_f_path


# Deploy archive
def do_deploy(archive_path):
    """Sends an archive to a web server"""
    if os.path.exists(archive_path):
        arcd_file = archive_path[9:]
        new_ver = "/data/web_static/releases/" + arcd_file[:-4]
        arcd_file = "/tmp/" + arcd_file

        put(archive_path, "/tmp/")
        print("Archive {} uploaded to /tmp/{}".format(arcd_file, arcd_file))
        run("sudo mkdir -p {}".format(new_ver))
        print("Folder {} created".format(new_ver))
        run("sudo tar -xzf {} -C {}/".format(arcd_file, new_ver))
        print("Uncompressed {} to {}".format(arcd_file, new_ver))
        run("sudo rm {}".format(arcd_file))
        print("Deleted {}".format(arcd_file))
        run("sudo mv {}/web_static/* {}".format(new_ver, new_ver))
        print("Moved content of {}/web_static/ to {}".format(new_ver, new_ver))
        run("sudo rm -rf {}/web_static".format(new_ver))
        print("Deleted folder {}/web_static/".format(new_ver))
        run("sudo rm -rf /data/web_static/current")
        print("Deleted /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_ver))
        print("Created symlink {} -> {}".format(new_ver, current))

        return True

    return False