import select
import socket
import struct

CLIENT_DATA = []
PACK_SIGN = "I"
INT_SIZE = 4

def check(lst1, lst2):
    """
    Check the guess against the chosen code and return a list of results.
    0 - right color, right spot
    1 - right color, wrong spot
    2 - wrong color

    :param lst1: guessed code
    :type lst1: list of int
    :param lst2: chosen code
    :type lst2: list of int

    :return: list of results
    :rtype: list of int
    """
    result = [0, 0, 0, 0]
    for i in range(4):
        if lst1[i] == lst2[i]:
            result[i] = 0
        elif lst1[i] in lst2:
            result[i] = 1
        else:
            result[i] = 2
    return result

def send(sock, data):
    """
    Send data through a socket with length prefix.

    :param sock: socket to send data through
    :type sock: socket.socket
    :param data: data to send
    :type data: bytes

    :return: True if data was sent successfully, False otherwise
    :rtype: bool
    """
    length = struct.pack(PACK_SIGN, socket.htonl(len(data)))
    to_send = length + data
    try:
        sent = 0
        while sent < len(to_send):
            sent += sock.send(to_send[sent:])
        return True
    except socket.error as err:
        print(f"error while sending at: {err}")
        return False

def recv(sock):
    """
    Receive data from a socket with length prefix.

    :param sock: socket to receive data from
    :type sock: socket.socket

    :return: received data
    :rtype: bytes
    """
    try:
        length = 0
        buf = b''
        data_len = b''
        data = b''

        while len(data_len) < INT_SIZE:
            buf = sock.recv(INT_SIZE - len(data_len))
            if buf == b'':
                data_len = b''
                break
            data_len += buf

        if data_len != b'':
            length = socket.ntohl(struct.unpack(PACK_SIGN, data_len)[0])

        while len(data) < length:
            buf = sock.recv(length - len(data))
            if buf == b'':
                data = b''
                break
            data += buf
        return data

    except socket.timeout:
        return b''

    except socket.error as err:
        # print(f"error while recv: {err}")
        return b'ERROR'

def main():
    """
    Main server function that handles client connections and game logic.
    """
    clients = []
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = socket.gethostname()
    port = 50006  # Port number (you can choose any available port)
    # Bind to the port
    server_socket.bind(("0.0.0.0", port))
    # Now wait for client connection.
    server_socket.listen(2)

    chooser, guesser = None, None
    chosen_code = None
    guessed_code = None
    num_guesses = 0
    # Establish connection with clients.
    while len(clients) < 2:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print("Got a connection from %s" % str(addr))

    while chooser is None:
        recv_list, _, _ = select.select(clients, [], [])
        if recv_list:
            chooser = recv_list[0]
            clients.remove(chooser)
            guesser = clients[0]
            chosen_code = chooser.recv(16).decode().split(',')
            chosen_code = [int(i) for i in chosen_code]

    guesser.send(b"START")  # tell guesser to start
    while guessed_code != chosen_code and num_guesses < 5:
        guess = guesser.recv(16).decode().split(',')
        guess = [int(i) for i in guess]
        print(guess)
        num_guesses += 1
        result = check(guess, chosen_code)
        if result == [0, 0, 0, 0]:
            break

        if num_guesses < 5:
            result = ','.join(map(str, check(guess, chosen_code)))
            guesser.send(result.encode())
    if num_guesses < 5:
        chooser.send(b"LOST")
        guesser.send(b"WON")
        # guesser won state
    else:
        chooser.send(b"WON")
        guesser.send(b"LOST")
        # guesser lost state


if __name__ == "__main__":
    main()
