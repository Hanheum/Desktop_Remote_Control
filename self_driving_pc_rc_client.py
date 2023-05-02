from socket import *
from struct import pack, unpack
from os import stat

HOST = input('ip:')
PORT = 3653

cli = socket(AF_INET, SOCK_STREAM)
cli.connect((HOST, PORT))

while True:
    command = input('command:')
    command_byte = command.encode()
    command_byte_len = len(command_byte)
    command_byte_len_byte = pack('<i', command_byte_len)
    cli.send(command_byte_len_byte)
    cli.send(command_byte)

    if command == 'dir':
        directory = input('directory:')
        cli.send(directory.encode())
        arr_len = cli.recv(4)
        arr_len = unpack('<i', arr_len)[0]
        recved_len = 0
        recved = b''
        while recved_len < arr_len:
            data = cli.recv(1024)
            recved += data
            recved_len += len(data)
        arr = recved.decode()
        print(arr)

    if command == 'code':
        code_dir = input('code directory:')
        file_size = stat(code_dir).st_size
        file_size_byte = pack('<i', file_size)
        cli.send(file_size_byte)

        file = open(code_dir, 'rb')
        sent_len = 0
        while sent_len < file_size:
            data = file.read(1024)
            sent_len += len(data)
            cli.send(data)
        file.close()