import threading

services = {}
plugin = {}
core = None
run_thread = None
thread_active = False


def _register_(serviceList, pluginProperties):
    global services, plugin, core
    services = serviceList
    plugin = pluginProperties
    core = services["core"][0]
    # core.addStart(start_thread)
    # core.addClose(close_thread)
    # core.addLoop(loopTask)


def loopTask():
    pass


def start_thread():
    global run_thread, thread_active
    thread_active = True
    run_thread = threading._thread(target=thread_script)
    run_thread.start()


def close_thread():
    global run_thread, thread_active
    thread_active = False
    run_thread.join()


def thread_script():
    global thread_active
    thread_active = False
