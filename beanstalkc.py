import socket

class UnexpectedResponse(Exception): pass
class CommandFailed(Exception): pass
class DeadlineSoon(Exception): pass

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

    def interact(self, command, expected_ok, expected_err=[]):
        self.socket.send(command)
        status, results = self.read_response()
        if status in expected_ok:
            return results
        elif status in expected_err:
            raise CommandFailed(status, results)
        else:
            raise UnexpectedResponse(status, results)

    def read_response(self):
        response = self.socket_file.readline().split()
        return response[0], response[1:]

    def read_body(self, size):
        body = self.socket_file.read(size)
        self.socket_file.read(2) # trailing crlf
        return body

    def interact_value(self, command, expected_ok, expected_err=[]):
        return self.interact(command, expected_ok, expected_err)[0]

    def interact_job(self, command, expected_ok, expected_err):
        jid, size = self.interact(command, expected_ok, expected_err)
        body = self.read_body(int(size))
        return jid, size, body

    def interact_yaml(self, command, expected_ok, expected_err=[]):
        [size] = self.interact(command, expected_ok, expected_err)
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
        try:
            jid, size, body = self.interact_job(command,
                                                'RESERVED',
                                                ['DEADLINE_SOON', 'TIMED_OUT'])
            return Job(self, int(jid), body, True)
        except CommandFailed, (status, results):
            if status == 'TIMED_OUT':
                return None
            elif status == 'DEADLINE_SOON':
                raise DeadlineSoon(results)

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
        try:
            return int(self.interact_value('ignore %s\r\n' % name,
                                           'WATCHING',
                                           'NOT_IGNORED'))
        except CommandFailed:
            return 1

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


if __name__ == '__main__':
    import doctest, time, os
    pid = os.spawnlp(os.P_NOWAIT,
                     'beanstalkd',
                     'beanstalkd', '-l', '127.0.0.1', '-p', '14711')
    doctest.testfile('TUTORIAL')
    os.kill(pid, 9)
