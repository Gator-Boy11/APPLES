#!/usr/bin/env python3

import logging

from ... import plugins

from . import handlers

_logger = logging.getLogger(f"{__name__}")


def install(plugin_list: str, repository=None, update=False, **_):
    if repository is None:
        for plugin_remote_url in plugin_list:
            handlers.install(plugin_remote_url, repository)
    else:
        _logger.error("Installing from repositories is not supported at this time.")


def post_load_core():
    core = plugins.services["core"][0]

def post_load_terminal():
    terminal = plugins.services["terminal"][0]

    install_parser = terminal.ArgumentParser(prog="plugman.install",
                                             description="Install plugins.",
                                             exit_on_error=False)
    install_parser.add_argument("plugin_list", nargs="*",
                                help="Plugins to install.")
    install_parser.add_argument("-r",
                                "--repository",
                                help="Update the following plugins.",
                                action="store_const",
                                const=None)
    install_parser.add_argument("-u",
                                "--update",
                                help="Update the following plugins.",
                                action="store_true")
    terminal.create_command(install, "plugman.install", install_parser)
    terminal.create_command(install, "install", install_parser)
