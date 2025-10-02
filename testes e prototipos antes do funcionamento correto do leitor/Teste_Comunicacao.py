from pyfingerprint.pyfingerprint import PyFingerprint

try:
    sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

    if sensor.verifyPassword():
        print("OK Conexão com o AS608 estabelecida!")
        print("Capacidade de armazenamento:", sensor.getStorageCapacity())
        print("Segurança atual:", sensor.getSecurityLevel())
    else:
        print("X Senha incorreta para o sensor")

except Exception as e:
    print("Erro ao conectar no sensor:", str(e))
