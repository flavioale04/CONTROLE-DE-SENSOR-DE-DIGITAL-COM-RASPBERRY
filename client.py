# client.py
import socket
import os

SENSOR_NAME = "Sensor_Biometrico"
BIN_DIR = "digitais_salvas"  # pasta onde estão os .bin do sensor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5859

def send_bin_file(client_socket, file_path):
    """Envia um arquivo .bin para o servidor."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        header = f"BIN:{os.path.basename(file_path)}:{len(data)}"
        client_socket.send(header.encode('utf-8'))
        client_socket.sendall(data)

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Servidor: {response}")

    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    client.send(SENSOR_NAME.encode('utf-8'))
    print(f"[CONECTADO] ao servidor {SERVER_IP}:{SERVER_PORT} como {SENSOR_NAME}")

    try:
        while True:
            arquivos = [f for f in os.listdir(BIN_DIR) if f.endswith('.bin')]
            if not arquivos:
                print(f"Nenhum arquivo .bin encontrado em {BIN_DIR}.")
                input("Cadastre pelo menos uma digital antes de enviar. Pressione Enter para continuar...")
                continue

            print("\nArquivos .bin disponíveis para envio:")
            for i, arq in enumerate(arquivos, start=1):
                print(f"{i} - {arq}")

            escolha = input("Digite o número do arquivo que deseja enviar ou 'q' para sair: ")

            if escolha.lower() == 'q':
                client.send("sair".encode('utf-8'))
                break

            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(arquivos):
                print("Escolha inválida.")
                continue

            file_path = os.path.join(BIN_DIR, arquivos[int(escolha)-1])
            send_bin_file(client, file_path)

    except KeyboardInterrupt:
        client.send("sair".encode('utf-8'))

    client.close()
    print("Conexão encerrada.")
