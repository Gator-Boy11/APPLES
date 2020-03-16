import threading, time
import json, os, socket, ssl

services = {}
plugin = {}
core = None
terminal = None
serverThreads = []
serverThreadsActive = []
serverSockets = []
serverNames = {}
clientThreads = []
clientThreadsActive = []
clientSockets = []
clientNames = {}

# openssl x509 -hash -fingerprint -noout -in FILENAME

configFile = "sslman/connections.acf"
defaultConfig = {
    "format": "0.1.0",
    }

_config_ = None

def _register_(serviceList, pluginProperties):
    global services, plugin, core, terminal, configFile, _config_
    services = serviceList
    plugin = pluginProperties
    core = services["core"][0]
    terminal = services["userInterface"][0]
    if not os.path.exists(configFile):
        createDefaultConfig()
    elif not os.path.isfile(configFile):
        raise FileNotFoundError
    with open(configFile, "r") as f:
        _config_ = json.load(f)
    core.addStart(startThread)
    core.addClose(closeThread)
    #core.addLoop(loopTask)

def createDefaultConfig():
    global configFile
    print("making config file")
    with open(configFile, "w")as f:
        json.dump(defaultConfig, f)
        f.close()
    pass

def loopTask():
    pass

def startThread():
    global _config_, serverThreads, serverThreadsActive, clientThreads, clientThreadsActive
    for i in range(0, len(_config_.get("serverSettings", []))):
        serverThreadsActive.append(True)
        serverThreads.append(threading.Thread(target = serverThreadScript, args=[i]))
        serverSockets.append([])
        serverThreads[i].start()
        serverNames[_config_["serverSettings"][i]["name"]] = i
    for i in range(0, len(_config_.get("clientSettings", []))):
        clientThreadsActive.append(True)
        clientThreads.append(threading.Thread(target = clientThreadScript, args=[i]))
        clientSockets.append(None)
        clientThreads[i].start()
        clientNames[_config_["clientSettings"][i]["name"]] = i

def closeThread():
    global runThread, _config_
    for i in range(0, len(_config_["serverSettings"])):
        serverThreadsActive[i] = False
    for i in range(0, len(_config_["serverSettings"])):
        serverThreads[i].join()
    for i in range(0, len(_config_["clientSettings"])):
        clientThreadsActive[i] = False
    for i in range(0, len(_config_["clientSettings"])):
        clientThreads[i].join()

def serverThreadScript(index):
    global serverThreadsActive, serverSockets, _config_
    socks =[]
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=_config_["serverSettings"][index]["serverCert"], keyfile=_config_["serverSettings"][index]["serverKey"])
    for certFile in _config_["serverSettings"][index]["clientCerts"]:
        context.load_verify_locations(cafile=certFile)
    for i in range(0, len(_config_["serverSettings"][index]["addresses"])):
        socks.append(socket.socket())
        socks[i].bind(tuple(_config_["serverSettings"][index]["addresses"][i]))
        socks[i].settimeout(_config_["serverSettings"][index]["addressTimeout"])
        socks[i].listen(_config_["serverSettings"][index].get("listenQueue", 8))
    while serverThreadsActive[index]:
        for sock in socks:
            try:
                serverSockets[index].append(context.wrap_socket((sock.accept())[0], server_side=True))
            except socket.timeout:
                pass
                #print("timeout waiting for connection")
    for i in range(0, len(_config_["serverSettings"][index]["addresses"])):
        socks[i].close()
    serverThreadsActive[index] = False

def clientThreadScript(index):
    global clientThreadsActive, clientSockets, _config_
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=_config_["clientSettings"][index]["serverCert"])
    context.load_cert_chain(certfile=_config_["clientSettings"][index]["clientCert"], keyfile=_config_["clientSettings"][index]["clientKey"])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSockets[index] = context.wrap_socket(s, server_side=False, server_hostname=_config_["clientSettings"][index]["serverHostname"])
    clientSockets[index].connect(tuple(_config_["clientSettings"][index]["serverAddress"]))
    
    
def addServer():
    global _config_
