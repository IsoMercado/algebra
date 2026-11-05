"""
Conversor de decimal a binario con árbol de divisiones.

El usuario hace las divisiones entre 2 y escribe solo el cociente (parte entera) en cada paso.
El resto lo calcula el programa solo (dividendo % 2).
El programa NO corrige en el momento: dibuja el árbol con lo que se ingresó
y recién al final dice si el resultado es correcto o incorrecto.

En el árbol:
  - hijo izquierdo  = cociente
  - hijo derecho    = (resto)  -> es el bit
"""

MAX_PASOS = 64  # límite de seguridad por si las respuestas nunca llegan a 0


def pedir_entero(mensaje, minimo=None):
    """Pide un número entero por teclado, repitiendo hasta que sea válido."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("  Ingresá un número entero válido.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  El número debe ser mayor o igual a {minimo}.")
            continue
        return valor


def dibujar_arbol(pasos):
    """
    Devuelve el árbol como texto.
    pasos: lista de tuplas (dividendo, cociente, resto)
    """
    k = len(pasos)
    if k == 0:
        return ""

    raiz = str(pasos[0][0])
    cocientes = [str(p[1]) for p in pasos]
    restos = [f"({p[2]})" for p in pasos]

    ancho = max(len(t) for t in [raiz] + cocientes + restos)
    u = ancho + 3                      # separación horizontal entre nodos
    margen = ancho // 2 + 1

    # centro (columna) del nodo i: la raíz queda a la derecha y el árbol crece hacia la izquierda
    centros = [margen + u * (k - i) for i in range(k + 1)]

    filas = 2 * k + 1
    columnas = centros[0] + u + ancho + 2
    lienzo = [[" "] * columnas for _ in range(filas)]

    def escribir(fila, centro, texto):
        inicio = centro - len(texto) // 2
        for j, ch in enumerate(texto):
            lienzo[fila][inicio + j] = ch

    escribir(0, centros[0], raiz)
    for i in range(k):
        fila_conector = 2 * i + 1
        fila_hijos = 2 * i + 2
        escribir(fila_conector, centros[i] - u // 2, "/")
        escribir(fila_conector, centros[i] + u // 2, "\\")
        escribir(fila_hijos, centros[i + 1], cocientes[i])   # hijo izquierdo: cociente
        escribir(fila_hijos, centros[i] + u, restos[i])      # hijo derecho: resto

    return "\n".join("".join(fila).rstrip() for fila in lienzo)


def pasos_correctos(n):
    """Calcula las divisiones correctas de n entre 2."""
    pasos = []
    while n > 0:
        pasos.append((n, n // 2, n % 2))
        n //= 2
    return pasos


def resultado_de(pasos):
    """Los restos leídos de abajo hacia arriba forman el número binario."""
    return "".join(str(r) for _, _, r in reversed(pasos))


def mostrar_arbol(titulo, pasos):
    print(f"\n{titulo}")
    print("(izquierda = cociente | derecha = (resto))\n")
    print(dibujar_arbol(pasos))


def main():
    print("=== Conversor a binario con árbol de divisiones ===")
    n = pedir_entero("Ingresá un número entero positivo: ", minimo=1)

    pasos = []
    dividendo = n

    while dividendo > 0 and len(pasos) < MAX_PASOS:
        print(f"\n--- Paso {len(pasos) + 1}: {dividendo} ÷ 2 ---")
        cociente = pedir_entero("  Cociente (parte entera): ", minimo=0)
        resto = dividendo % 2  # el resto lo calcula el programa

        pasos.append((dividendo, cociente, resto))
        mostrar_arbol("Así va el árbol:", pasos)

        dividendo = cociente

    if dividendo > 0:
        print(f"\nSe alcanzó el máximo de {MAX_PASOS} pasos sin llegar a cociente 0. Se detiene el proceso.")

    # ---- Resultado final ----
    print("\n" + "=" * 50)
    mostrar_arbol("ÁRBOL FINAL:", pasos)

    tu_resultado = resultado_de(pasos)
    correcto = bin(n)[2:]

    print(f"\nLos restos de abajo hacia arriba dan: {tu_resultado}")
    print(f"Tu resultado: {n} en binario = {tu_resultado}")

    if tu_resultado == correcto:
        print("\n✅ El resultado es CORRECTO. ¡Muy bien!")
    else:
        print("\n❌ El resultado es INCORRECTO.")
        print(f"La respuesta correcta es: {correcto}")
        mostrar_arbol("Así era el árbol correcto:", pasos_correctos(n))


if __name__ == "__main__":
    main()