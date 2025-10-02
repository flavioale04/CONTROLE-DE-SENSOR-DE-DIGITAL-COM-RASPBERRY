# scan_fingerprint_baudrates.py
from pyfingerprint.pyfingerprint import PyFingerprint

baudrates = [9600, 19200, 38400, 57600, 115200]
port = '/dev/serial0'

print("=== Scan de baudrates para o sensor AS608 ===")

for baud in baudrates:
    print(f"\n>> Testando {port} @ {baud} bps")
    try:
        f = PyFingerprint(port, baud, 0xFFFFFFFF, 0x00000000)
        if f.verifyPassword():
            print(f'✅ Sensor encontrado @ {baud} bps')
            print(f'Template capacity: {f.getStorageCapacity()}')
            print(f'Security level: {f.getSystemParameters()}')
            break
        else:
            print("⚠ Sensor respondeu, mas senha incorreta")
    except Exception as e:
        print(f"❌ Falha: {e}")
