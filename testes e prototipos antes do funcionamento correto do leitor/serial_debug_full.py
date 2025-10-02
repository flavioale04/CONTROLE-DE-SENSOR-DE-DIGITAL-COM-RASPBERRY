import serial
import time

PORT = '/dev/serial0'
BAUDRATES = [57600, 115200]
TIMEOUT = 1  # 1 segundo de timeout para leitura
READ_BYTES = 16  # número de bytes para tentar ler
TRIES = 5  # tentativas por baudrate

print("=== SERIAL DEBUG ROBUSTO ===\n")

for baud in BAUDRATES:
    print(f"\nTestando porta {PORT} @ {baud} bps")
    try:
        ser = serial.Serial(port=PORT, baudrate=baud, timeout=TIMEOUT)
        print(f"✅ Porta aberta com sucesso: {PORT} @ {baud} bps")

        for attempt in range(1, TRIES + 1):
            ser.flushInput()
            print(f"Tentativa {attempt}/{TRIES}: lendo {READ_BYTES} bytes...")
            data = ser.read(READ_BYTES)
            if data:
                print(f"✅ Bytes recebidos: {len(data)} -> {data.hex()}")
            else:
                print("⚠ Nenhum byte recebido")

        ser.close()
        print(f"Porta {PORT} fechada\n")

    except Exception as e:
        print(f"❌ Erro ao abrir {PORT} @ {baud}: {e}")
