import socket
import yaml

class Connection(object):
    def __init__(self, host='127.0.0.1', port=11300):
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket_file = self.socket.makefile('rb')

    def close(self):
        self.socket.close()

    def interact(self, command, expected):
        self.socket.send(command)
        return self.check_response(expected)

    def check_response(self, expected):
        word, vals = self.read_response()
        if word in expected:
            return vals
        else:
            raise 'unexpected-response' # @@

    def read_response(self):
        response = self.socket_file.readline().split()
        return response[0], response[1:]

    def read_body(self, size):
        body = self.socket_file.read(size)
        self.socket_file.read(2) # trailing crlf
        return body

    def interact_job(self, command, expected):
        [id, size] = self.interact(command, expected)
        body = self.read_body(int(size))
        return id, size, body

    def interact_yaml(self, command, expected):
        [size] = self.interact(command, expected)
        body = self.read_body(int(size))
        return yaml.load(body)

    # -- public interface --

    def put(self, body, priority=2147483648, delay=0, ttr=120):
        [id] = self.interact(
                'put %d %d %d %d\r\n%s\r\n' % 
                    (priority, delay, ttr, len(body), body),
                ['INSERTED', 'BURIED'])
        return int(id)

    def reserve(self, timeout=None):
        if timeout:
            command = 'reserve-with-timeout %d\r\n' % timeout
        else:
            command = 'reserve\r\n'
        id, size, body = self.interact_job(command, 'RESERVED')
        return Job(self, int(id), body, True)

    def tubes(self):
        return self.interact_yaml('list-tubes\r\n', 'OK')

    def using(self):
        return self.interact('list-tube-used\r\n', 'USING')[0]

    def use(self, name):
        return self.interact('use %s\r\n' % name, 'USING')[0]

    def watching(self):
        return self.interact_yaml('list-tubes-watched\r\n', 'OK')

    def watch(self, name):
        return int(self.interact('watch %s\r\n' % name, 'WATCHING')[0])

    def ignore(self, name):
        r = self.interact('ignore %s\r\n' % name, ['WATCHING', 'NOT_IGNORED'])
        return r[0] if r else 1

    def stats(self):
        return self.interact_yaml('stats\r\n', 'OK')

    # -- job interactors --

    def delete(self, id):
        self.interact('delete %d\r\n' % id, 'DELETED')


class Job:
    def __init__(self, conn, id, body, reserved=True):
        self.conn = conn
        self.id = id
        self.body = body
        self.reserved = reserved

    # -- public interface --

    def delete(self):
        if self.reserved:
            self.conn.delete(self.id)
            self.reserved = False
