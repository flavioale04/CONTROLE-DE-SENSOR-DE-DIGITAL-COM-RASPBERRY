# !/bin/bash
echo "===== Diagnóstico Serial no Raspberry Pi ====="
echo

# 1) Versão do sistema
echo "[INFO] Versão do SO:"
uname -a
echo

# 2) Verificar enable_uart
echo "[INFO] Checando enable_uart no /boot/config.txt:"
grep -E '^enable_uart' /boot/config.txt || echo ">> enable_uart NÃO encontrado!"
echo

# 3) Verificar symlink serial0
echo "[INFO] Listando /dev/serial*"
ls -l /dev/serial* 2>/dev/null || echo ">> Nenhum dispositivo /dev/serial* encontrado"
echo

# 4) Verificar se o console ainda está usando a serial
echo "[INFO] Checando parâmetros de boot (cmdline.txt):"
grep -o 'console=[^ ]*' /boot/cmdline.txt || echo ">> Nenhuma entrada console= encontrada (ok)"
echo

# 5) Verificar grupos do usuário
echo "[INFO] Usuário atual: $(whoami)"
echo "[INFO] Grupos do usuário:"
groups $(whoami)
echo

# 6) Testar permissão em /dev/serial0
if [ -e /dev/serial0 ]; then
    if [ -r /dev/serial0 ] && [ -w /dev/serial0 ]; then
        echo "[OK] Usuário tem permissão de leitura e escrita em /dev/serial0"
    else
        echo "[ERRO] Usuário NÃO tem permissão em /dev/serial0 (adicione ao grupo 'dialout')"
    fi
else
    echo "[ERRO] /dev/serial0 não existe!"
fi
echo

# 7) Testar pacotes Python
echo "[INFO] Testando Python e bibliotecas..."
python3 - <<'PY'
try:
    import serial
    print("[OK] pyserial instalado")
except ImportError:
    print("[ERRO] pyserial não instalado")

try:
    import pyfingerprint
    print("[OK] pyfingerprint instalado")
except ImportError:
    print("[ERRO] pyfingerprint não instalado")

import sys
print("Versão Python:", sys.version)
PY
echo

echo "===== Diagnóstico concluído ====="
