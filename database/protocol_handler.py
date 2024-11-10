class protocol_handler(object):
    def __init__(self):
        self.handlers = {
                '+' : self.handle_simple_string,
                '$' : self.handle_string,
                '*' : self.handle_array,
                '-' : self.handle_error,
                ':' : self.handle_integer,
                '%' : self.handle_dict,
                }

    def handle_request(self, socket_file):
        first_byte = socket_file.read(1)
        if not first_byte:
            raise Disconnect()

        try:
            return self.handlers[first_byte](socket_file)
        except KeyError:
            raise command_error('bad request')

    def handle_simple_string(self, socket_file):
        return socket_file.readline().rstrip("\r\n")

    def handle_error(self, socket_file):
        return Error(socket_file.readline().rstrip("\r\n"))

    def handle_integer(self, socket_file):
        return int(socket_file.readline().rstrip('\r\n')) 

    def handle_string(self, socket_file):
        length = int(socket_file.readline().rstrip("\r\n"))
        if length == -1:
            return None  # Handle null string case
        length += 2 # Include traling \r\n
        data = socket_file.read(length[:-2])
        socket_file.read(2)  # Read the trailing CRLF
        return data

    def handle_array(self, socket_file):
        length = int(socket_file.readline().rstrip("\r\n"))
        if length == -1:
            return None  # Handle null array case
        elements = []
        for _ in range(length):
            elements.append(self.handle_request(socket_file))
        return elements

    def handle_dict(self, socket_file):
        length = int(socket_file.readline().rstrip("\r\n"))
        if length == -1:
            return None  # Handle null dictionary case
        dictionary = {}
        for _ in range(length*2):
            key = self.handle_request(socket_file)
            value = self.handle_request(socket_file)
            dictionary[key] = value
        return dictionary
