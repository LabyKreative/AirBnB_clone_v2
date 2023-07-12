#!/usr/bin/python3
# a Fabric script (based on the file 3-deploy_web_static.py)
# that deletes out-of-date archives, using the function do_clean:
import os
from fabric.api import *

env.hosts = ["100.26.154.241", "35.153.194.206"]


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for x in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for x in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
