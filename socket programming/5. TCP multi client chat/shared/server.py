import json

clients = []
connection_to_client_map = {}
remote_commands = {}


class Client:
    next_id = 1
    key = "John Doe"

    def __init__(self, connection, address):
        self.id = Client.next_id
        Client.next_id += 1
        self.connection = connection
        self.address = address

    @property
    def name(self):
        return '{} ({} {})'.format(self.key, self.id, self.address)

    def sendall(self, data):
        self.connection.sendall(data + b'\n')

    def recv_packets(self):
        raw_data = self.connection.recv(1024).decode()
        if raw_data:
            return [
                json.loads(json_data)
                for json_data in raw_data.split('\n')
                if json_data
            ]


def remote(func):
    remote_commands[func.__name__] = func
    return func


@remote
def say(client, data):
    output = f'{client.key}: {data}'

    message = json.dumps({
        'command': 'output',
        'data': output,
    }).encode()

    print(output)
    for client in clients:
        client.sendall(message)


@remote
def set_name(client, data):
    print(f"{client.key} ({client.address}) changed name to '{data}'")
    client.key = data


def setup(connection, client_address):
    print(f'client {id(connection)} joined')
    client = Client(connection, client_address)
    clients.append(client)
    connection_to_client_map[connection] = client

    client.sendall(json.dumps({
        'command': 'set_client_id',
        'data': client.id,
    }).encode())


def handle_packets(connection):
    """
    Returns false if there were no packets, true elsewhere
    """
    client = connection_to_client_map[connection]
    packets = client.recv_packets()

    if not packets:
        return False

    print('packets', packets)
    for packet in packets:
        print('packet', packet)
        command_name = packet['command']
        data = packet['data']

        command = remote_commands[command_name]
        command(client=client, data=data)

    return True


def handle(connection):
    # print('id', id(connection))
    while True:
        if not handle_packets(connection):
            break


def finish(connection):
    print(f'client {id(connection)} left')
    client = connection_to_client_map[connection]
    clients.remove(client)
    del connection_to_client_map[connection]