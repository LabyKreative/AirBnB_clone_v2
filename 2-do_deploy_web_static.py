#!/usr/bin/python3
# a Fabric script (based on the file 1-pack_web_static.py) that distributes
# an archive to your web servers, using the function do_deploy:
import os
import argparse
from os.path import exists, isfile
from fabric.api import env, put, run

env.hosts = ["100.26.154.241", "35.153.194.206"]
env.user = 'ubuntu'
env.private_key = '~/.ssh/school'


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        # Create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/'
            'web_static_{}/'.format(timestamp))

        # Uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C '
            '/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* '
            '/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/'
            'web_static_{}/web_static'
            .format(timestamp))

        # Delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/'
            'web_static_{}/ /data/web_static/current'
            .format(timestamp))
    except Exception:
        return False

    # Return True on success
    return True
