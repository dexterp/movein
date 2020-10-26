import os
import subprocess
import platform
import webbrowser

from invoke import task
from os import getenv
from os.path import abspath, dirname, getctime, join
from pathlib import Path
from glob import glob
from sys import version_info

home = getenv("HOME")

#
# Vars
#
root = dirname(__file__)

#
# Required tasks - All builds must always have these tasks. Or tasks with these names that do the same work.
#
@task
def clean(c):
    """
    Return project to original state
    """
    safe_rm_rf(c, slash("tmp"))


@task
def pip(c):
    """
    Lock packages to a version using pip compile
    """
    if not os.path.exists("requirements-setup.txt") or getctime("requirements-setup.in") > getctime("requirements-setup.txt"):
        c.run("pip-compile --quiet --output-file=requirements-setup.txt requirements-setup.in")
    if not os.path.exists("requirements.txt") or getctime("requirements.in") > getctime("requirements.txt"):
        c.run("pip-compile --quiet --output-file=requirements.txt requirements.in")
    c.run("pip install --quiet --requirement requirements-setup.txt")
    c.run("pip install --quiet --requirement requirements.txt")


@task
def pip_compile(c):
    """
    Update dependency requirements if any
    """
    touch("requirements-setup.in")
    touch("requirements.in")


@task(pre=[pip])
def movein(c):
    """
    Run move in code
    """
    c.run("mkdir -p dist")

#
# Utilities
#
def checkupdate(src:str, dst:str) -> bool:
    """
    Check if file source file is older or destination file does not exists
    """
    if not Path(dst).exists():
        return True
    if getctime(src) < getctime(dst):
        return True
    return False


def safe_rm_rf(c, pattern):
    """
    Safely delete files
    """
    projdir = abspath(dirname(__file__))
    for f in glob(pattern):
        fullpath = abspath(f)
        if not fullpath.startswith(projdir):
            msg = "File {} is not a project file".format(fullpath)
            raise Exception(msg)

        c.run("rm -rf {}".format(fullpath))


def slash(text: str) -> str:
    """
    Replace slashes to backslashes on windows
    """
    return str(Path(text))


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)