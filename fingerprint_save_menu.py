#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pyfingerprint.pyfingerprint import PyFingerprint

SAVE_DIR = "digitais_salvas"

def ensure_folder():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"✅ Pasta criada: {SAVE_DIR}")

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

def enroll_and_save(f):
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
            print("❌ Digitais não coincidem.")
            return

        f.createTemplate()
        position = f.storeTemplate()
        print(f"✅ Digital cadastrada na posição #{position}")

        template_data = f.downloadCharacteristics(0x01)
        file_path = os.path.join(SAVE_DIR, f"digital_{position}.bin")
        with open(file_path, "wb") as file:
            file.write(bytearray(template_data))
        print(f"💾 Digital salva em: {file_path}")

    except Exception as e:
        print("❌ Erro no cadastro/salvamento:", e)

def search_digital(f):
    try:
        print("\n=== Buscar digital ===")
        print("Coloque o dedo no sensor...")
        while not f.readImage():
            pass

        f.convertImage(0x01)
        result = f.searchTemplate()
        position = result[0]
        if position == -1:
            print("❌ Digital não encontrada.")
        else:
            print(f"✅ Digital encontrada na posição #{position}")
    except Exception as e:
        print("❌ Erro na busca:", e)

def clear_digital(f):
    try:
        pos = input("Digite a posição que deseja limpar: ")
        if not pos.isdigit():
            print("❌ Posição inválida")
            return
        pos = int(pos)
        if f.deleteTemplate(pos):
            print(f"🗑️ Digital da posição #{pos} apagada com sucesso")
        else:
            print(f"❌ Falha ao apagar posição #{pos}")
    except Exception as e:
        print("❌ Erro ao limpar digital:", e)

if __name__ == "__main__":
    ensure_folder()
    sensor = init_sensor()

    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar e salvar digital")
        print("2 - Buscar digital")
        print("3 - Limpar digital")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            enroll_and_save(sensor)
        elif escolha == '2':
            search_digital(sensor)
        elif escolha == '3':
            clear_digital(sensor)
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
