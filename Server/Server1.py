import socket
import os
import ssl
import hashlib

# 配置服务端证书和私钥文件路径
SERVER_CERT = 'SSL/server.crt'
SERVER_KEY = 'SSL/server.key'

def calculate_file_hash(file_path, hash_algorithm="sha256"):
    """计算文件的哈希值"""
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024 * 1024):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def send_file(client_socket, file_path):
    """发送文件及其哈希值"""
    file_size = os.path.getsize(file_path)
    file_hash = calculate_file_hash(file_path)
    client_socket.send(f"{file_size}|{file_hash}".encode())

    with open(file_path, 'rb') as f:
        while chunk := f.read(1024 * 1024):
            client_socket.sendall(chunk)
    print(f"文件发送完成: {file_path}")

def find_file(client_socket, filename):
    safe_dir = os.path.abspath('files')  # 限定文件根目录
    filepath = os.path.abspath(os.path.join(safe_dir, filename))
    
    if os.path.commonpath([safe_dir, filepath]) != safe_dir or not os.path.exists(filepath):
        client_socket.send("没有找到该文件".encode())
    else:
        print(f"文件存在: {filepath}")
        client_socket.send("找到文件，正在下载...".encode())
        send_file(client_socket, filepath)

def list_files(client_socket):
    files = os.listdir('files')
    client_socket.send(", ".join(files).encode())

def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8090))
    server_socket.listen(5)
    print("安全服务器已启动，等待客户端连接...")

    while True:
        client_socket, client_addr = server_socket.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)
        print(f"客户端{client_addr}已连接 (加密通道)")

        secure_socket.send("你好, 客户端!".encode("UTF-8"))
        while True:
            try:
                command = secure_socket.recv(1024).decode("UTF-8")
                if command == "exit":
                    break
                elif command == 'quit':
                    return
                elif command == "list":
                    list_files(secure_socket)
                elif command.startswith("get "):
                    filename = command[4:].strip()
                    print(f"客户端请求的文件名为: {filename}")
                    find_file(secure_socket, filename)
                else:
                    secure_socket.send("未知命令".encode())
            except Exception as e:
                print(f"服务端错误: {e}")
                break
        secure_socket.close()
        print(f"客户端{client_addr}已断开连接")

if __name__ == '__main__':
    os.makedirs('files', exist_ok=True)
    main()
