
returncodes = {}

def init(client, id, filename):
    file = open(filename)
    fileContent = file.read()
    file.close()

    returncodes[id] = None

    client.publish("exec/" + str(id) + "/code", fileContent)
    client.subscribe("exec/" + str(id) + "/out", 0)
    client.subscribe("exec/" + str(id) + "/status", 0)

def process(msg):
    global returncode

    if msg.topic.startswith("exec/"):
        if msg.topic.endswith("/out"):
            payload = str(msg.payload, 'utf-8')
            if len(payload) > 0:
                id = msg.topic[5 : len(msg.topic) - 4]
                if payload.endswith("\n"):
                    print(id + ": " + payload, end="")
                else:
                    print(id + ": " + payload)
            return True
        elif msg.topic.endswith("/status"):
            payload = str(msg.payload, 'utf-8')
            id = msg.topic[5: len(msg.topic) - 7]
            returncodes[id] = payload
            return True

    return False

def returncode(id):
    return returncodes[id]
