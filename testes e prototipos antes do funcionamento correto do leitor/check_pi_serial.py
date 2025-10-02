#!/usr/bin/env python3
import os
import platform
import subprocess
import grp
import getpass
from pathlib import Path

print("=== CHECK SERIAL NO RASPBERRY PI (Python) ===\n")

# 1) Versão do sistema
print("[1] Versão do sistema:")
print(platform.uname())
print()

# 2) Modelo do Raspberry Pi
print("[2] Modelo do Raspberry Pi:")
try:
    with open("/proc/device-tree/model", "r") as f:
        print(f.read().strip())
except Exception as e:
    print("Não foi possível ler modelo:", e)
print()

# 3) Configurações do boot/config.txt
print("[3] Status do boot config (procura por serial):")
try:
    with open("/boot/config.txt", "r") as f:
        for line in f:
            if "enable_uart" in line or "serial" in line:
                print(line.strip())
except Exception as e:
    print("Não foi possível abrir /boot/config.txt:", e)
print()

# 4) Interfaces seriais disponíveis
print("[4] Interfaces serial disponíveis:")
for dev in Path("/dev").glob("tty*"):
    if "AMA" in dev.name or "S" in dev.name or "serial" in dev.name:
        print(" -", dev)
print()

# 5) Serviços que podem estar usando UART
print("[5] Serviços UART ativos (systemd):")
for service in ["serial-getty@ttyAMA0.service", "serial-getty@ttyS0.service"]:
    try:
        status = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True
        )
        print(f" - {service}: {status.stdout.strip()}")
    except Exception as e:
        print(f"Erro ao checar {service}:", e)
print()

# 6) Grupos do usuário atual
print("[6] Grupos do usuário atual (precisa ter 'dialout'):")
user = getpass.getuser()
groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
print(f"Usuário: {user}")
print("Grupos:", ", ".join(groups))
print()

# 7) Permissões das portas seriais
print("[7] Permissões das portas seriais encontradas:")
for dev in ["/dev/ttyAMA0", "/dev/ttyS0"]:
    if os.path.exists(dev):
        st = os.stat(dev)
        print(f" - {dev}: {oct(st.st_mode)} dono UID={st.st_uid} GID={st.st_gid}")
print()

print("=== FIM DO CHECK ===")
