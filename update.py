#!/usr/bin/python3

# This module needs to be rewritten using git library


import git
from os import system as command
from subprocess import check_output

def update_remote_repo():
    ## Updating remote repo
    val = command("git remote update")
    return val

def check_update():
    """ Return True if there is a new version available """

    if update_remote_repo() != 0:
        # Return False cause unable to update remote repo        
        return False

    git_output = check_output(["git", "status", "-uno"]).decode()
    if "Your branch is behind" in git_output:
        return True


def update_repo():
    """ Just pull the repository """
    command("git pull origin main")
