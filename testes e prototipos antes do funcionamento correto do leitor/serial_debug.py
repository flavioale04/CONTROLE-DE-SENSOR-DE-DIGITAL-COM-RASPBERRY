import serial
import time

# CONFIGURAÇÃO
PORTS = ['/dev/serial0', '/dev/ttyAMA0']  # portas a testar
BAUDRATES = [57600, 115200]               # baudrates comuns do AS608
TIMEOUT = 2                               # segundos

for port in PORTS:
    for baud in BAUDRATES:
        print(f"\n=== Testando porta {port} @ {baud} bps ===")
        try:
            ser = serial.Serial(port=port, baudrate=baud, timeout=TIMEOUT)
            if ser.is_open:
                print(f"✅ Porta aberta com sucesso: {port} @ {baud} bps")
            else:
                print(f"❌ Não foi possível abrir a porta: {port}")
                continue

            print("Tentando ler 16 bytes do sensor (timeout 2s)...")
            ser.flushInput()
            data = ser.read(16)
            if data:
                print(f"Recebido ({len(data)} bytes): {data.hex()}")
            else:
                print("⚠ Nenhum byte recebido do sensor.")

            ser.close()

        except Exception as e:
            print(f"❌ Erro ao abrir {port} @ {baud}: {e}")
