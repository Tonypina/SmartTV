import subprocess

def leer_entrada_ir():
    try:
        # Ejecuta el comando ir-keytable con un timeout de 1 segundo
        resultado = subprocess.run(["ir-keytable", "-t", "-s", "rc0"], capture_output=True, text=True, timeout=1)
        salida = resultado.stdout

        # Procesa la salida para obtener el código recibido
        codigo = None
        lineas = salida.split("\n")
        for linea in lineas:
            if "nec" in linea:  # Busca la línea que contiene el código NEC
                partes = linea.split(" ")
                codigo = partes[-1]  # El último elemento de la línea es el código NEC
                break

        return codigo
    except subprocess.TimeoutExpired:
        return None  # Si el comando excede el timeout, retorna None

# Ejemplo de uso
while True:
    codigo = leer_entrada_ir()
    if codigo:
        print("Código recibido:", codigo)
