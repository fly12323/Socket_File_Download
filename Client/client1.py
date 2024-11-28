import socket
import ssl
import os
import hashlib

# 配置服务端证书路径（用于验证服务端身份）
SERVER_CERT = 'SSL/server.crt'

def verify_file_integrity(file_path, expected_hash, hash_algorithm="sha256"):
    """验证文件的完整性"""
    actual_hash = calculate_file_hash(file_path, hash_algorithm)
    return actual_hash == expected_hash

def calculate_file_hash(file_path, hash_algorithm="sha256"):
    """计算文件的哈希值"""
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024 * 1024):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def download_file(client_socket, filename):
    filepath = os.path.join('download', filename)
    os.makedirs('download', exist_ok=True)  # 确保下载目录存在

    # 接收文件大小和哈希值
    file_info = client_socket.recv(1024).decode("UTF-8")
    file_size, expected_hash = file_info.split('|')
    file_size = int(file_size)
    received_size = 0

    with open(filepath, 'wb') as file:
        while received_size < file_size:
            chunk = client_socket.recv(1024 * 1024)
            file.write(chunk)
            received_size += len(chunk)
            print(f"\r下载进度: {received_size / file_size:.2%}", end="")
    print(f"\n文件 '{filename}' 下载完成，保存到 '{filepath}'")

    # 验证文件完整性
    if verify_file_integrity(filepath, expected_hash):
        print(f"文件完整性校验成功: {expected_hash}")
    else:
        print("文件完整性校验失败！")

def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=SERVER_CERT)
    # context.check_hostname = False  # 禁用主机名验证

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    secure_socket.connect(('127.0.0.1', 8090))

    hello = secure_socket.recv(1024).decode("UTF-8")
    print(hello)

    while True:
        command = input("请输入 (list, get <filename>, exit): ")
        secure_socket.send(command.encode())
        if command == "exit":
            break
        elif command == "quit":
            secure_socket.recv(1024).decode("UTF-8")
            break
        elif command == "list":
            files = secure_socket.recv(1024).decode("UTF-8")
            print(f"可用文件: {files}")
        elif command.startswith("get "):
            filename = command[4:].strip()
            response = secure_socket.recv(1024).decode("UTF-8")
            print(f"服务端: {response}")
            if "正在下载" in response:
                download_file(secure_socket, filename)
            else:
                print("文件未找到")
        else:
            print("未知命令")
    secure_socket.close()

if __name__ == '__main__':
    main()
