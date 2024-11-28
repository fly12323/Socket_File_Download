import socket
import os

def download_file(client_socket, filename):
    filepath = os.path.join('download', filename)
    os.makedirs('download', exist_ok=True)  # 确保下载目录存在

    # 接收文件大小
    file_size = int(client_socket.recv(1024).decode())
    received_size = 0

    with open(filepath, 'wb') as file:
        while received_size < file_size:
            chunk = client_socket.recv(1024 * 1024)
            file.write(chunk)
            received_size += len(chunk)
            print(f"\r下载进度: {received_size / file_size:.2%}", end="")
    print(f"\n文件 '{filename}' 下载完成，保存到 '{filepath}'")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8091))
    hello = client_socket.recv(1024).decode("UTF-8")
    print(hello)

    while True:
        command = input("请输入 (list, get <filename>, exit): ")
        client_socket.send(command.encode())
        if command == "exit":
            break
        elif command == "list":
            files = client_socket.recv(1024).decode("UTF-8")
            print(f"可用文件: {files}")
        elif command.startswith("get "):
            filename = command[4:].strip()
            response = client_socket.recv(1024).decode("UTF-8")
            print(f"服务端: {response}")
            if "正在下载" in response:
                download_file(client_socket, filename)
            else:
                print("文件未找到")
        else:
            print("未知命令")
    client_socket.close()

if __name__ == '__main__':
    main()