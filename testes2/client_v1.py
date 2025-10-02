#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from pyfingerprint.pyfingerprint import PyFingerprint

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5859
SENSOR_NAME = "Sensor_Biometrico"


def init_sensor():
    try:
        f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError("Senha do sensor incorreta.")
        print("✅ Sensor iniciado")
        print("Capacidade:", f.getStorageCapacity())
        print("Digitais cadastradas:", f.getTemplateCount())
        return f
    except Exception as e:
        print("❌ Erro ao inicializar sensor:", e)
        exit(1)


def enroll_and_send(f, client_socket):
    """
    Captura digital, cria template e envia diretamente ao servidor.
    """
    try:
        print("\n=== Captura de nova digital ===")
        print("Coloque o dedo no sensor...")

        while not f.readImage():
            pass

        f.convertImage(0x01)

        print("Remova o dedo...")
        while f.readImage():
            pass

        print("Coloque o mesmo dedo novamente...")
        while not f.readImage():
            pass

        f.convertImage(0x02)

        if f.compareCharacteristics() == 0:
            print("❌ Digitais não coincidem. Tente novamente.")
            return

        f.createTemplate()
        # Armazena temporariamente no sensor
        position = f.storeTemplate()
        print(f"✅ Digital cadastrada na posição #{position}")

        # Faz o download do template para enviar
        template_data = f.downloadCharacteristics(0x01)
        data_bytes = bytearray(template_data)

        # Monta o header
        header = f"BIN:digital_{position}.bin:{len(data_bytes)}"
        client_socket.send(header.encode('utf-8'))
        client_socket.sendall(data_bytes)

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Servidor: {response}")

    except Exception as e:
        print("❌ Erro no cadastro/envio:", e)


if __name__ == "__main__":
    sensor = init_sensor()

    # Conecta ao servidor
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    client.send(SENSOR_NAME.encode('utf-8'))
    print(f"[CONECTADO] ao servidor {SERVER_IP}:{SERVER_PORT} como {SENSOR_NAME}")

    try:
        while True:
            input("\nPressione Enter para capturar e enviar uma digital ou Ctrl+C para sair...")
            enroll_and_send(sensor, client)

    except KeyboardInterrupt:
        client.send("sair".encode('utf-8'))

    client.close()
    print("Conexão encerrada.")
