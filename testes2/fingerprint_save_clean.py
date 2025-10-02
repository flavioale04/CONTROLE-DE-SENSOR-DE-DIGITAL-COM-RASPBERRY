#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pyfingerprint.pyfingerprint import PyFingerprint

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
        print(f"✅ Digital cadastrada na posição #{position}")

        # Exporta template para arquivo
        template_data = f.downloadCharacteristics(0x01)
        file_path = os.path.join(SAVE_DIR, f"digital_{position}.bin")
        with open(file_path, "wb") as file:
            file.write(bytearray(template_data))
        print(f"💾 Digital salva em: {file_path}")

        # Limpa posição usada no sensor
        f.deleteTemplate(position)
        print(f"🗑️ Posição #{position} limpa do sensor.")

    except Exception as e:
        print("❌ Erro no cadastro/salvamento:", e)

if __name__ == "__main__":
    ensure_folder()
    sensor = init_sensor()

    while True:
        input("\nPressione Enter para cadastrar e salvar uma digital (Ctrl+C para sair)...")
        enroll_and_save(sensor)
