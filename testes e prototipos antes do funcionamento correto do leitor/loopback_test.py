#!/usr/bin/env python3
import serial, time

PORT = '/dev/serial0'
BAUDRATES = [115200, 57600, 38400, 19200, 9600]
MSG = b'LOOPTEST\n'
TIMEOUT = 0.5

print("=== LOOPBACK TEST ===")
for baud in BAUDRATES:
    try:
        print(f"\nTestando {PORT} @ {baud} bps")
        ser = serial.Serial(port=PORT, baudrate=baud, timeout=TIMEOUT)
        ser.reset_input_buffer()
        time.sleep(0.05)
        ser.write(MSG)
        time.sleep(0.05)
        data = ser.read(len(MSG))
        ser.close()
        if data:
            print(f"✅ Recebido ({len(data)} bytes): {data!r}")
        else:
            print("⚠ Nenhum dado recebido (loopback falhou neste baudrate)")
    except Exception as e:
        print("❌ Erro ao abrir/usar porta:", e)
