import subprocess

def leer_entrada_ir():
    # Ejecuta el comando ir-keytable para obtener la entrada IR
    resultado = subprocess.run(["ir-keytable", "-t", "-s", "rc0"], capture_output=True, text=True)
    salida = resultado.stdout

    print(salida)

    # Procesa la salida para obtener el código recibido
    codigo = None
    lineas = salida.split("\n")
    for linea in lineas:
        if "necx" in linea:  # Busca la línea que contiene el código NEC
            partes = linea.split(" ")
            codigo = partes[-1]  # El último elemento de la línea es el código NEC
            break

    return codigo

# Ejemplo de uso
while True:
    codigo = leer_entrada_ir()
    if codigo:
        print("Código recibido:", codigo)
