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
    arc_file_path = "versions/web_static_{}.tgz".format(date)

    # Create the archive file.
    arc_file_created = local("tar -cvzf {} web_static".format(arc_file_path))
    logging.info("Archive file {} created".format(arc_file_path))

    if arc_file_created.succeeded:
        return arc_file_path
    else:
        return None


# Deploy archive
def do_deploy(archive_path):
    """Sends an archive to a web server"""

    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        new_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file, new_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(new_version, new_version))
        run("sudo rm -rf {}/web_static".format(new_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_version))

        print("Yay! Alfeenah, new version deployed!")
        return True

    return False
