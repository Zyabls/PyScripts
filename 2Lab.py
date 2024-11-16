import socket
import threading

# TCP-сервер (Echo-сервер)
def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("TCP-сервер ожидает подключения...")

    conn, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    data = conn.recv(1024)
    print(f"Получено сообщение: {data.decode()}")
    conn.sendall(data)

    conn.close()
    server_socket.close()

# TCP-клиент
def tcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    message = "Hello, TCP Server!"
    client_socket.sendall(message.encode())

    data = client_socket.recv(1024)
    print(f"Получен ответ от сервера: {data.decode()}")

    client_socket.close()

# UDP-сервер
def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12346))
    print("UDP-сервер ожидает данных...")

    data, addr = server_socket.recvfrom(1024)
    print(f"Получено сообщение от {addr}: {data.decode()}")
    server_socket.sendto(data, addr)

    server_socket.close()

# UDP-клиент
def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, UDP Server!"
    client_socket.sendto(message.encode(), ('localhost', 12346))

    data, addr = client_socket.recvfrom(1024)
    print(f"Получен ответ от сервера: {data.decode()}")

    client_socket.close()

def main():
    # Запуск TCP-сервера в отдельном потоке
    tcp_server_thread = threading.Thread(target=tcp_server)
    tcp_server_thread.start()

    # Запуск UDP-сервера в отдельном потоке
    udp_server_thread = threading.Thread(target=udp_server)
    udp_server_thread.start()

    # Даем немного времени для запуска серверов
    threading.Timer(1.0, tcp_client).start()
    threading.Timer(1.0, udp_client).start()

if __name__ == "__main__":
    main()
