"""
Adapted from https://github.com/bmwant/podmena/blob/master/podmena/cli.py
"""

import os
import shutil
import sys

import click

from whatcha_readin._config import VERSION
from whatcha_readin.cli.utils import (
    _warn,
    _note,
    get_git_root_dir,
)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "../resources")
HOOK_FILENAME = "commit_msg.py"
HOOK_FILENAME_DEST = "commit-msg"


@click.group()
@click.version_option(version=VERSION, prog_name="whatcha-readin")
def cli():
    pass


@cli.command(
    name="status", help="Shows whether whatcha-readin is activated for this repository"
)
def status():
    active = False

    git_root_dir = get_git_root_dir()
    if git_root_dir is not None:
        local_hooks_path = os.path.join(git_root_dir, ".git", "hooks")
        hook_path = os.path.join(local_hooks_path, HOOK_FILENAME_DEST)
        if os.path.exists(hook_path):
            _note("whatcha-readin is activated for this repository!")
            active = True

    if not active:
        _warn("whatcha-readin is not activated for this repository")


@cli.command(name="install", help="Install whatcha-readin for current git repository")
def install():
    git_local_root = os.path.join(os.getcwd(), ".git")
    local_hooks_path = os.path.join(git_local_root, "hooks")
    if os.path.exists(git_local_root) and os.path.isdir(git_local_root):
        # copy our hook file over
        src_file = os.path.join(RESOURCES_DIR, HOOK_FILENAME)
        dst_file = os.path.join(local_hooks_path, HOOK_FILENAME_DEST)
        shutil.copyfile(src_file, dst_file)
        os.chmod(dst_file, 0o0775)
        _note("Successfully installed for this repository!")
    else:
        _warn("Not a git repository")
        sys.exit(1)


@cli.command(
    name="uninstall", help="Uninstall whatcha-readin for current git repository"
)
def uninstall():
    git_local_root = os.path.join(os.getcwd(), ".git")
    hook_filepath = os.path.join(git_local_root, "hooks", HOOK_FILENAME_DEST)
    if os.path.exists(hook_filepath):
        os.remove(hook_filepath)
        _note("Uninstalled for current repository")
    else:
        _warn("whatcha-readin is not installed for current repository!")
        sys.exit(1)


if __name__ == "__main__":
    cli()
