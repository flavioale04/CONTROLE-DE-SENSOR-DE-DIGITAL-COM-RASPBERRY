#!/usr/bin/env python3
# capture_as608_pi.py
# Captura imagem do AS608 (JM-101B) e salva PNG + template binário.
# Ajuste DEVICE se necessário.

from pyfingerprint.pyfingerprint import PyFingerprint
from PIL import Image
import time
import sys
import os

# =========== CONFIGURAÇÃO ===========
# Em Raspberry Pi use /dev/serial0 (ou '/dev/ttyAMA0' se preferir)
DEVICE = '/dev/serial0'
BAUDRATE = 57600          # padrão comum para AS608
ADDRESS = 0xFFFFFFFF
PASSWORD = 0x00000000

# Resolução típica AS608 (muitos AS608 usam 256x288)
IMG_WIDTH = 256
IMG_HEIGHT = 288

OUTPUT_PNG = 'fingerprint_capture.png'
OUTPUT_RAW = 'fingerprint_capture.raw'
OUTPUT_TEMPLATE_BIN = 'fingerprint_template.bin'
# =====================================

def save_template_to_file(f, filename):
    """Cria template e salva características (char buffer) como binário."""
    try:
        # converte imagem para característica no buffer 1
        f.createTemplate()
        chars = f.downloadCharacteristics(0x01)  # lista de ints 0..255
        b = bytes(chars)
        with open(filename, 'wb') as fh:
            fh.write(b)
        return True
    except Exception as e:
        print('Erro ao criar/baixar template:', e)
        return False

def main():
    try:
        f = PyFingerprint(DEVICE, BAUDRATE, ADDRESS, PASSWORD)
        if not f.verifyPassword():
            raise ValueError('Senha do sensor incorreta!')
    except Exception as e:
        print('Erro inicializando sensor:', e)
        sys.exit(1)

    print('Sensor inicializado.')
    print(f'Capacidade de armazenamento: {f.getStorageCapacity()} templates.')
    print('Coloque o dedo no sensor...')

    # Espera leitura da imagem
    try:
        while not f.readImage():
            time.sleep(0.1)
    except Exception as e:
        print('Falha durante readImage():', e)
        sys.exit(1)

    print('Imagem lida. Convertendo buffer para características (opcional)...')
    try:
        f.convertImage(0x01)
    except Exception as e:
        print('Falha ao converter imagem:', e)
        # prossegue pois queremos a imagem crua também

    # Tenta baixar imagem bruta
    print('Baixando imagem do sensor...')
    try:
        img_buffer = f.downloadImage()  # geralmente retorna lista de ints
    except Exception as e:
        print('downloadImage() falhou:', e)
        print('Algumas forks da lib nomeiam diferente. Verifique sua versão da pyfingerprint.')
        sys.exit(1)

    # Normaliza para bytes
    if isinstance(img_buffer, bytes):
        img_bytes = img_buffer
    else:
        img_bytes = bytes(img_buffer)

    expected_len = IMG_WIDTH * IMG_HEIGHT
    if len(img_bytes) != expected_len:
        print(f'Atenção: comprimento do buffer = {len(img_bytes)}, esperado = {expected_len}.')
        # tenta ajustar altura se possível
        if len(img_bytes) % IMG_WIDTH == 0:
            height = len(img_bytes) // IMG_WIDTH
            print(f'Calculando altura = {height} com largura = {IMG_WIDTH}.')
        else:
            print('Salvar raw e encerrar para inspeção manual.')
            with open(OUTPUT_RAW, 'wb') as rf:
                rf.write(img_bytes)
            print(f'Arquivo {OUTPUT_RAW} salvo. Ajuste IMG_WIDTH/IMG_HEIGHT se necessário e reexecute.')
            # tenta ainda criar template (se possível)
            if save_template_to_file(f, OUTPUT_TEMPLATE_BIN):
                print(f'Template salvo em {OUTPUT_TEMPLATE_BIN}')
            sys.exit(0)
    else:
        height = IMG_HEIGHT

    # Cria imagem PIL e salva PNG
    try:
        img = Image.frombytes('L', (IMG_WIDTH, height), img_bytes)
        # dependendo do sensor, talvez precise inverter:
        # img = Image.eval(img, lambda x: 255 - x)
        img.save(OUTPUT_PNG)
        print(f'Imagem salva: {OUTPUT_PNG}')
    except Exception as e:
        print('Erro ao criar/salvar PNG:', e)
        with open(OUTPUT_RAW, 'wb') as rf:
            rf.write(img_bytes)
        print(f'Raw salvo em {OUTPUT_RAW}')

    # Salvando template binário (características) — opcional mas útil
    if save_template_to_file(f, OUTPUT_TEMPLATE_BIN):
        print(f'Template de características salvo em {OUTPUT_TEMPLATE_BIN}')
    else:
        print('Não foi possível salvar template (verifique permissões / estado do sensor).')

if __name__ == '__main__':
    main()
