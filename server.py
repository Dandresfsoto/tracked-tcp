from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer


class Server(TCPServer):
    message_separator = b'\r\n'

    async def handle_stream(self, stream, address):
        while True:
            try:
                request = await stream.read_until(self.message_separator)
            except StreamClosedError:
                stream.close(exc_info=True)
                return
            try:
                await stream.write(request)
                print(request.decode('UTF-8'))
            except StreamClosedError:
                stream.close(exc_info=True)
                return


if __name__ == '__main__':
    Server().listen(8000)
    print('Starting the server...')
    IOLoop.instance().start()
    print('Server has shut down.')