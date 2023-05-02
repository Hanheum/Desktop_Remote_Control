from socket import *
from struct import unpack, pack
from os import listdir, startfile, remove

self_dir = 'D:\\PycharmProjects\\self_driving_car_server\\'

HOST = ''
PORT = 3653

ser_sock = socket(AF_INET, SOCK_STREAM)
ser_sock.bind((HOST, PORT))
ser_sock.listen()

def accept():
    cli_sock, addr = ser_sock.accept()
    print('connected by {}'.format(addr))
    return cli_sock

class cli:
    def __init__(self, cli_sock):
        self.cli_sock = cli_sock

    def receive(self):
        command_len = self.cli_sock.recv(4)
        command_len = unpack('<i', command_len)[0]
        command = self.cli_sock.recv(command_len)
        command = command.decode()

        if command == 'code':
            file_size = self.cli_sock.recv(4)
            file_size = unpack('<i', file_size)[0]
            recved_len = 0

            recved_code = b''
            while recved_len < file_size:
                data = self.cli_sock.recv(1024)
                recved_len += len(data)
                recved_code += data
            recved_code = recved_code.decode()
            code_file = open('{}remote_code.py'.format(self_dir), 'w')
            code_file.write(recved_code)
            code_file.close()

        if command == 'dir':
            requested_dir = self.cli_sock.recv(1024)
            requested_dir = requested_dir.decode()
            arr = listdir(requested_dir)
            arr = '{}'.format(arr)
            arr_byte = arr.encode()
            file = open('./arr_returned.txt', 'wb')
            file.write(arr_byte)
            file.close()
            arr_byte_len = len(arr_byte)
            arr_byte_len_byte = pack('<i', arr_byte_len)
            self.cli_sock.send(arr_byte_len_byte)
            sent_len = 0
            file = open('./arr_returned.txt', 'rb')
            while sent_len < arr_byte_len:
                data = file.read(1024)
                sent_len += len(data)
                self.cli_sock.send(data)
            file.close()
            remove('./arr_returned.txt')

        if command == 'execute':
            startfile('{}execute_code.bat'.format(self_dir))

while True:
    cli_sock = accept()
    client = cli(cli_sock)
    try:
        while True:
            client.receive()
    except Exception as e:
        print(e)
        del(client)