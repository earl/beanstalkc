import socket

class Connection(object):
    def __init__(self, host='127.0.0.1', port=11300, decode_yaml=True):
        if decode_yaml:
            global yaml
            import yaml
        self.host = host
        self.port = port
        self.decode_yaml = decode_yaml
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
        status, results = self.read_response()
        if status in expected:
            return status, results
        else:
            raise 'unexpected-response', status # @@

    def read_response(self):
        response = self.socket_file.readline().split()
        return response[0], response[1:]

    def read_body(self, size):
        body = self.socket_file.read(size)
        self.socket_file.read(2) # trailing crlf
        return body

    def interact_value(self, command, expected):
        _, results = self.interact(command, expected)
        return results[0]

    def interact_job(self, command, expected_ok, expected_err):
        status, results = self.interact(command, [expected_ok] + expected_err)
        if status in expected_ok:
            jid, size = results
            body = self.read_body(int(size))
            return status, (jid, size, body)
        else:
            return status, results

    def interact_yaml(self, command, expected):
        size = self.interact_value(command, expected)
        body = self.read_body(int(size))
        return yaml.load(body) if self.decode_yaml else body

    # -- public interface --

    def put(self, body, priority=2147483648, delay=0, ttr=120):
        jid = self.interact_value(
                'put %d %d %d %d\r\n%s\r\n' %
                    (priority, delay, ttr, len(body), body),
                ['INSERTED', 'BURIED'])
        return int(jid)

    def reserve(self, timeout=None):
        if timeout is not None:
            command = 'reserve-with-timeout %d\r\n' % timeout
        else:
            command = 'reserve\r\n'
        status, results = self.interact_job(command,
                                            'RESERVED',
                                            ['DEADLINE_SOON', 'TIMED_OUT'])
        if status == 'TIMED_OUT':
            return None
        elif status == 'DEADLINE_SOON':
            raise 'deadline-soon', results # @@
        else:
            jid, size, body = results
            return Job(self, int(jid), body, True)

    def tubes(self):
        return self.interact_yaml('list-tubes\r\n', 'OK')

    def using(self):
        return self.interact_value('list-tube-used\r\n', 'USING')

    def use(self, name):
        return self.interact_value('use %s\r\n' % name, 'USING')

    def watching(self):
        return self.interact_yaml('list-tubes-watched\r\n', 'OK')

    def watch(self, name):
        return int(self.interact_value('watch %s\r\n' % name, 'WATCHING'))

    def ignore(self, name):
        status, results = self.interact('ignore %s\r\n' % name,
                                        ['WATCHING', 'NOT_IGNORED'])
        return int(results[0]) if status == 'WATCHING' else 1

    def stats(self):
        return self.interact_yaml('stats\r\n', 'OK')

    # -- job interactors --

    def delete(self, jid):
        self.interact('delete %d\r\n' % jid, 'DELETED')


class Job:
    def __init__(self, conn, jid, body, reserved=True):
        self.conn = conn
        self.jid = jid
        self.body = body
        self.reserved = reserved

    # -- public interface --

    def delete(self):
        if self.reserved:
            self.conn.delete(self.jid)
            self.reserved = False
