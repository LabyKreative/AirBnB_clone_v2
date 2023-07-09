#!/usr/bin/python3
# a Fabric script (based on the file 1-pack_web_static.py) that distributes
# an archive to your web servers, using the function do_deploy:
import os
import argparse
from os.path import exists, isfile
from fabric.api import env, put, run

env.hosts = ["100.26.154.241", "35.153.194.206"]


def do_deploy(archive_path):
    """Sends an archive to a web server"""
    if not exists(archive_path) and not isfile(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        no_ext = os.path.splitext(archive_filename)[0]

        # Uploads the the archive to /tmp/ dir of the web server
        put(archive_path, '/tmp/')

        # Unzip the archive to the specified dir
        release_folder = '/data/web_static/releases/' + no_ext + '/'
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Deletes archive from the web server and move files specified dir:
        run('rm /tmp/{}'.format(archive_filename))
        run('mv {}web_static/* {}'.format(release_folder, release_folder))

        run('rm -f /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print('New version deployed!')
        return True

    except Exception:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_path", type=str,
                        help="path to the archive file")
    parser.add_argument("-u", "--username", type=str,
                        help="SSH username")
    parser.add_argument("-i", "--private-key", type=str,
                        help="Path to SSH private key")
    args = parser.parse_args()

    if args.username:
        env.user = args.username

    if args.private_key:
        env.key_filename = args.private_key

    do_deploy(args.archive_path)
