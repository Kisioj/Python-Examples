import json

client_id = None
remote_commands = {}


def remote(func):
    remote_commands[func.__name__] = func
    return func


@remote
def output(server, data):
    print(f"{data}")


@remote
def set_client_id(server, data):
    global client_id
    client_id = data


def send_loop(connection):
    name = input('Name: ')
    message = json.dumps({
        "command": "set_name",
        "data": name,
    }).encode()
    try:
        connection.send(message + b'\n')
    except BrokenPipeError:
        print("Connection has been broken.")
        return

    while True:
        message = json.dumps({
            "command": "say",
            "data": input(),
        }).encode()
        try:
            connection.send(message + b'\n')
        except BrokenPipeError:
            print("Connection has been broken.")
            return


def dispatch(connection, json_data):
    packet = json.loads(json_data)
    command_name = packet['command']
    data = packet['data']

    command = remote_commands[command_name]
    command(connection, data)
