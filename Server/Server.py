import socket
import os

def send_file(client_socket, file_path, chunk_size=1024 * 1024):
    file_size = os.path.getsize(file_path)
    client_socket.send(f"{file_size}".encode())  # 发送文件大小
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            client_socket.sendall(chunk)
    print(f"文件发送完成: {file_path}")

def find_file(client_socket, filename):
    safe_dir = os.path.abspath('files')  # 限定文件根目录
    filepath = os.path.abspath(os.path.join(safe_dir, filename))
    
    # 确保文件路径在安全目录内
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8091))
    server_socket.listen(5)
    print("服务器已启动，等待客户端连接...")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"客户端{client_addr}已连接")
        client_socket.send("你好, 客户端!".encode("UTF-8"))
        while True:
            try:
                command = client_socket.recv(1024).decode("UTF-8")
                if command == "exit":
                    break
                elif command == "list":
                    list_files(client_socket)
                elif command.startswith("get "):
                    filename = command[4:].strip()
                    print(f"客户端请求的文件名为: {filename}")
                    find_file(client_socket, filename)
                else:
                    client_socket.send("未知命令".encode())
            except Exception as e:
                print(f"服务端错误: {e}")
                break
        client_socket.close()
        print(f"客户端{client_addr}已断开连接")

if __name__ == '__main__':
    os.makedirs('files', exist_ok=True)  # 确保共享文件目录存在
    main()