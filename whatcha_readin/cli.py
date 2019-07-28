"""
Adapted from https://github.com/bmwant/podmena/blob/master/podmena/cli.py
"""

import os
import shutil
import sys

import click
import configparser

from whatcha_readin.config import VERSION
from whatcha_readin.utils import _warn, _note, get_git_root_dir

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "resources")
CONFIG = "wr-config.ini"
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


def is_installed():
    git_local_root = os.path.join(os.getcwd(), ".git")
    hook_filepath = os.path.join(git_local_root, "hooks", HOOK_FILENAME_DEST)
    return os.path.exists(hook_filepath)


# def get_config():
#     git_local_root = os.path.join(os.getcwd(), ".git")
#     local_hooks_path = os.path.join(git_local_root, "hooks")
#     config_path = os.path.join(local_hooks_path, CONFIG)
#     parser = configparser.ConfigParser()
#     parser.read(config_path)
#     return parser


@cli.command(
    name="uninstall", help="Uninstall whatcha-readin for current git repository"
)
def uninstall():
    if is_installed():
        git_local_root = os.path.join(os.getcwd(), ".git")
        hook_filepath = os.path.join(git_local_root, "hooks", HOOK_FILENAME_DEST)
        os.remove(hook_filepath)
        _note("Uninstalled for current repository")
    else:
        _warn("whatcha-readin is not installed for current repository!")
        sys.exit(1)


@cli.command(name="config", help="configure your goodreads user by ID")
@click.option("--user-id", prompt="Your goodreads user ID", required=True)
@click.option("--key", prompt="Your goodreads API key", required=True)
def configure_user_id(user_id, key):
    if not is_installed():
        _warn(
            "Cannot configure without installing first. Please run `whatcha-readin install`"
        )
        sys.exit(1)

    config = configparser.ConfigParser()
    config["GOODREADS"] = {"api_key": key, "user_id": user_id}

    git_local_root = os.path.join(os.getcwd(), ".git")
    local_hooks_path = os.path.join(git_local_root, "hooks")
    config_path = os.path.join(local_hooks_path, CONFIG)
    with open(config_path, "w") as f:
        config.write(f)

    _note("Successfully configured goodreads access!")


if __name__ == "__main__":
    cli()
