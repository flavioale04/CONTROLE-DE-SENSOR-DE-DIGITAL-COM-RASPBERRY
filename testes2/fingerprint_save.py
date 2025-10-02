#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pyfingerprint.pyfingerprint import PyFingerprint

# Pasta onde os templates serão salvos
SAVE_DIR = "digitais_salvas"

def ensure_folder():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"✅ Pasta criada: {SAVE_DIR}")
    else:
        print(f"📂 Pasta já existe: {SAVE_DIR}")

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

def enroll_and_save(f):
    """
    Cadastra uma digital e salva o template em arquivo.
    """
    try:
        print("\n=== Cadastro de nova digital ===")
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
            raise Exception("As digitais não coincidem")

        f.createTemplate()
        position = f.storeTemplate()
        print("✅ Digital cadastrada na posição #", position)

        # Exporta template
        template_data = f.downloadCharacteristics(0x01)
        file_path = os.path.join(SAVE_DIR, f"digital_{position}.bin")
        with open(file_path, "wb") as file:
            file.write(bytearray(template_data))
        print(f"💾 Digital salva em: {file_path}")

    except Exception as e:
        print("❌ Erro no cadastro/salvamento:", e)

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
    ensure_folder()
    sensor = init_sensor()

    while True:
        print("\nEscolha uma opção:")
        print("1 - Cadastrar e salvar digital")
        print("2 - Buscar digital")
        print("0 - Sair")
        choice = input("> ")

        if choice == "1":
            enroll_and_save(sensor)
        elif choice == "2":
            search(sensor)
        elif choice == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")
