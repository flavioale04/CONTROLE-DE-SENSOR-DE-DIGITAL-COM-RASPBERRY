#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyfingerprint.pyfingerprint import PyFingerprint

def init_sensor():
    try:
        f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError("Senha do sensor incorreta.")

        print("✅ Sensor iniciado com sucesso")
        print("Capacidade:", f.getStorageCapacity())
        print("Digitais cadastradas:", f.getTemplateCount())
        return f

    except Exception as e:
        print("❌ Erro ao inicializar sensor:", e)
        exit(1)


def enroll(f):
    """
    Cadastra uma nova digital.
    """
    try:
        print("\n=== Cadastro de nova digital ===")
        print("Coloque o dedo no sensor...")

        # Espera até detectar um dedo
        while not f.readImage():
            pass

        # Converte para características
        f.convertImage(0x01)

        print("Remova o dedo...")
        while f.readImage():
            pass

        print("Coloque o mesmo dedo novamente...")
        while not f.readImage():
            pass

        f.convertImage(0x02)

        # Compara as duas leituras
        if f.compareCharacteristics() == 0:
            raise Exception("As digitais não coincidem")

        # Cria template
        f.createTemplate()
        position = f.storeTemplate()
        print("✅ Digital cadastrada na posição #", position)

    except Exception as e:
        print("❌ Erro no cadastro:", e)


def search(f):
    """
    Busca digital no banco do sensor.
    """
    try:
        print("\n=== Busca de digital ===")
        print("Coloque o dedo no sensor...")

        while not f.readImage():
            pass

        f.convertImage(0x01)

        # Faz a busca
        result = f.searchTemplate()
        positionNumber = result[0]
        accuracyScore = result[1]

        if positionNumber == -1:
            print("❌ Digital não encontrada")
        else:
            print("✅ Digital encontrada na posição #", positionNumber)
            print("Score de precisão:", accuracyScore)

    except Exception as e:
        print("❌ Erro na busca:", e)


if __name__ == "__main__":
    sensor = init_sensor()

    while True:
        print("\nEscolha uma opção:")
        print("1 - Cadastrar nova digital")
        print("2 - Buscar digital")
        print("0 - Sair")
        choice = input("> ")

        if choice == "1":
            enroll(sensor)
        elif choice == "2":
            search(sensor)
        elif choice == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")
