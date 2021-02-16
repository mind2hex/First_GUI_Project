#!/usr/bin/python3

from subprocess import check_output as comando
from os import getcwd as pwd

info = "@echo off\n"
info += "cd " + pwd() + "\n"
info += comando("where python3").decode().rstrip("\r\n")
info += " main.py\n"
info += "pause"

with open("MOTOGP.bat", "w") as handler:
    handler.write(info)
