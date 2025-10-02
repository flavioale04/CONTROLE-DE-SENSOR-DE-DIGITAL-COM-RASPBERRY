# server.py
import socket
import threading
import os

SAVE_DIR = "received_digitais"

def ensure_folder():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"✅ Pasta criada: {SAVE_DIR}")
    else:
        print(f"📂 Pasta já existe: {SAVE_DIR}")

def get_next_filename(ext='.bin'):
    """Gera nome único para o próximo arquivo salvo."""
    existing_files = [f for f in os.listdir(SAVE_DIR) if f.startswith('digital_') and f.endswith(ext)]
    next_num = len(existing_files) + 1
    return f"digital_{next_num}{ext}"

def handle_sensor(client_socket, sensor_name):
    while True:
        try:
            header = client_socket.recv(1024)

            if not header:
                print(f"[DESCONECTADO] {sensor_name}")
                break

            decoded = None
            try:
                decoded = header.decode('utf-8')
            except:
                pass

            if decoded:
                if decoded.lower() == 'sair':
                    print(f"[DESCONECTADO] {sensor_name}")
                    break

                # Check for digital file header
                if decoded.startswith('BIN:'):
                    parts = decoded.split(':')
                    filesize = int(parts[2])
                    save_path = os.path.join(SAVE_DIR, get_next_filename())

                    print(f"[{sensor_name}] Recebendo digital: {save_path} ({filesize} bytes)")

                    with open(save_path, 'wb') as f:
                        received = 0
                        while received < filesize:
                            chunk = client_socket.recv(min(4096, filesize - received))
                            if not chunk:
                                break
                            f.write(chunk)
                            received += len(chunk)

                    client_socket.send(f"Digital recebida e salva como {os.path.basename(save_path)}".encode('utf-8'))
                else:
                    print(f"[{sensor_name}] Dados recebidos: {decoded}")
                    client_socket.send(f"Servidor recebeu: {decoded}".encode('utf-8'))

        except Exception as e:
            print(f"Erro: {e}")
            break

    client_socket.close()


if __name__ == "__main__":
    ensure_folder()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5859))
    server.listen()
    print("[SERVIDOR INICIADO] Aguardando sensores...")

    while True:
        client_socket, client_address = server.accept()
        sensor_name = client_socket.recv(1024).decode('utf-8')
        print(f"[NOVA CONEXÃO] {sensor_name} de {client_address}")
        thread = threading.Thread(target=handle_sensor, args=(client_socket, sensor_name))
        thread.start()
        print(f"[THREADS ATIVAS] {threading.active_count() - 1}")
