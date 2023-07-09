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
        """Sends an archive to the wae server"""
        try:
                if not (path.exists(archive_path)):
                        return False

                # Uploads the archive
                put(archive_path, '/tmp/')

                # Creates the target directory
                timestamp = archive_path[-18:-4]
                run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

                # Unzips the archive and remove .tgz
                run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'
                    .format(timestamp, timestamp))

                # Removes the archive
                run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

                # Moves the archive contents to host web_static director
                run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

                # Removes extraneous web_static directory
                run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

                # Deletes the pre-existing symbolic link
                run('sudo rm -rf /data/web_static/current')

                # Re-establishes symbolic link
                run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
        except:
                return False

        # Returns true on success
        return True
