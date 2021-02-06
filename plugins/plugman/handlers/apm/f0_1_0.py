import urllib.request
import shutil
import os


from ..... import plugins

PLUGIN_DIRECTORY = plugins.PLUGIN_DIRECTORY


def install(plugin_manifest, plugin_manifest_file, plugin_remote_url, repository):
    plugin_name = plugin_manifest["name"]
    with open(os.path.join(PLUGIN_DIRECTORY, f"{plugin_name}.apm"), "wb") as plugin_local_file:
        plugin_manifest_file.seek(0)
        shutil.copyfileobj(plugin_manifest_file, plugin_local_file, -1)
    install_files(plugin_manifest)


def install_files(plugin_manifest):
    for file in plugin_manifest["files"]:
        local_url = file["local-url"]
        remote_url = file["remote-url"]
        try:
            os.makedirs(local_url)
        except FileExistsError:
            pass
        urllib.request.urlretrieve(remote_url, local_url)
