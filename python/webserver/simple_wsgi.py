#!/usr/bin/python
# coding:utf-8

import sys
import socket
import select
import StringIO


class WSGIServer(object):
    def __init__(self, server_address, application):

        self.server_address = server_address
        self.application = application
        self.address_family = socket.AF_INET
        self.socket_type = socket.SOCK_STREAM
        self.request_queue_size = 128

        self.socket_server_init()

    def socket_server_init(self):
        # Create a listening socket
        self.listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )

        # Allow to reuse the same address
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        self.listen_socket.bind(self.server_address)
        # Activate
        self.listen_socket.listen(self.request_queue_size)

        # self.epoller = select.epoll()
        # self.epoller.register(self.listen_socket.fileno(), select.EPOLLIN)

        # Get server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        # Return headers set by Web framework/Web application
        self.headers_set = []

    def server_forever(self):
        self.conn = {}

        while True:
            client_socket_fd, client_address = self.listen_socket.accept()

            print client_socket_fd, client_address

            fileno = client_socket_fd.fileno()

            self.conn[fileno] = {}

            self.conn[fileno]['socket_fd'] = client_socket_fd

            self.request(fileno)

            self.conn[fileno]['socket_fd'].close()

            # events = self.epoller.poll(0.05)
            #
            # for fileno, event in events:
            #     if fileno == self.listen_socket.fileno():
            #         # New client connection
            #         client_socket_fd, client_address = self.listen_socket.accept()
            #         self.epoller.register(client_socket_fd.fileno(), select.EPOLLIN | select.EPOLLET)
            #         self.conn[client_socket_fd.fileno()]['socket_fd'] = client_socket_fd
            #     else:
            #         self.request(fileno)
            #         self.epoller.unregister(fileno)
            #         self.conn[fileno].close()

    def request(self, fileno):
        # self.conn[fileno] = {}
        self.conn[fileno]['req_data'] = self.conn[fileno]['socket_fd'].recv(1024)



        print(''.join(
            '< {line}\n'.format(line = line)
            for line in self.conn[fileno]['req_data'].splitlines()
        ))

        self.request_unpack(fileno)

        # Construct environment dictionary using request data
        env = self.environ_get(fileno)

        # It's time to call our application callable and get
        # back a result that will become HTTP response body
        self.conn[fileno]['ans_data'] = self.application(env, self.response_pack)

        # Construct a response and send it back to the client
        self.response(fileno)

    def request_unpack(self, fileno):
        # Parse request
        (self.conn[fileno]['request_method'],  # GET
         self.conn[fileno]['path'],  # /hello
         self.conn[fileno]['request_version']  # HTTP/1.1
         ) = self.conn[fileno]['req_data'].splitlines()[0].rstrip('\r\n').split()

    def response_pack(self, status, response_headers, exc_info = None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def response(self, fileno):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status = status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in self.conn[fileno]['ans_data']:
                response += data
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '> {line}\n'.format(line = line)
                for line in response.splitlines()
            ))
            self.conn[fileno]['socket_fd'].sendall(response)
        finally:
            self.conn[fileno]['socket_fd'].close()

    def environ_get(self, fileno):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = StringIO.StringIO(self.conn[fileno]['req_data'])
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # Required CGI variables
        env['REQUEST_METHOD'] = self.conn[fileno]['request_method']  # GET
        env['PATH_INFO'] = self.conn[fileno]['path']  # /hello
        env['SERVER_NAME'] = self.server_name  # localhost
        env['SERVER_PORT'] = str(self.server_port)  # 8888

        return env


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # sys.exit('Please Provide a WSGI application object as module:callable')
        pass

    port = 8888
    # app_path = sys.argv[1]
    app_path = 'simple_web_server:app'
    module, application = app_path.split(':')
    module = __import__(module)

    httpd = WSGIServer(('', port), getattr(module, application))

    print('\nWSGIServer: Serving HTTP on port {port} ...\n'.format(port = port))

    httpd.server_forever()
