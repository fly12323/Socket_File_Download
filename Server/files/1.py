import socket
import os

def send_file(client_socket, file_path, chunk_size=1024*1024):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            client_socket.sendall(chunk)
        client_socket.sendall(b'')

def find_file(client_socket, filename):
    filepath = os.path.join('files', filename)
    if os.path.exists(filepath):
        print("文件存在")
        client_socket.send("找到文件，正在下载...".encode())
        send_file(client_socket, filepath)
    else:
        client_socket.send("没有找到该文件".encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8090))
    server_socket.listen(5)
    print("服务器已启动，等待客户端连接...")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"客户端{client_addr}已连接")
        client_socket.send("你好, 客户端!".encode("UTF-8"))
        while True:
            filename = client_socket.recv(1024).decode("UTF-8")
            if filename == "exit":
                break
            if filename == "quit":
                return
            print(f"收到客户端请求的文件名为：{filename}")
            find_file(client_socket, filename)
        client_socket.close()
        print(f"客户端{client_addr}已断开连接")

if __name__ == '__main__':
    main()