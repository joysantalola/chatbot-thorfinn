# ============================================================
# CHATBOT DE THORFINN - VERSIÓN TERMINAL
# Archivo: chatbot.py
# ============================================================
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import ollama
from persona import SYSTEM_PROMPT

# ── CONFIGURACIÓN ────────────────────────────────────────────
MODELO = "thorfinn"
MAX_MENSAJES_HISTORIAL = 20  # Límite para no saturar la RAM


# ── FUNCIÓN PRINCIPAL DE RESPUESTA ──────────────────────────
def obtener_respuesta(historial: list) -> str:
    """
    Llama al modelo con el historial completo de la conversación.
    Devuelve la respuesta de Thorfinn como string.
    """
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}] + historial

    respuesta = ollama.chat(
        model=MODELO,
        messages=mensajes
    )

    return respuesta["message"]["content"]


# ── FUNCIÓN PARA RECORTAR EL HISTORIAL ──────────────────────
def recortar_historial(historial: list) -> list:
    """
    Si el historial supera el límite, elimina los mensajes más
    antiguos (pero siempre de dos en dos para mantener pares
    usuario/asistente).
    """
    if len(historial) > MAX_MENSAJES_HISTORIAL:
        historial = historial[-MAX_MENSAJES_HISTORIAL:]
    return historial


# ── INTERFAZ DE TERMINAL ─────────────────────────────────────
def iniciar_chat():
    """
    Bucle principal del chatbot en modo terminal.
    """
    print("\n" + "═" * 55)
    print("  ⚔️   VINLAND SAGA — CHATBOT DE THORFINN   ⚔️")
    print("═" * 55)
    print("  Etapa activa: ADULTO — Rumbo a Vinland")
    print("  Escribe 'salir' para terminar la conversación.")
    print("  Escribe 'limpiar' para borrar el historial.")
    print("═" * 55 + "\n")

    historial = []

    while True:
        # Leer input del usuario
        try:
            entrada = input("Tú: ").strip()
        except KeyboardInterrupt:
            # Si el usuario pulsa Ctrl+C, salir limpiamente
            print("\n\nThorfinn: ...El silencio también es una respuesta.\n")
            break

        # Comandos especiales
        if not entrada:
            continue

        if entrada.lower() == "salir":
            print("\nThorfinn: Que el camino sea tuyo.\n")
            break

        if entrada.lower() == "limpiar":
            historial = []
            print("\n[Historial borrado. Nueva conversación.]\n")
            continue

        # Añadir mensaje del usuario al historial
        historial.append({"role": "user", "content": entrada})

        # Obtener respuesta del modelo
        print("\nThorfinn: ", end="", flush=True)

        try:
            respuesta = obtener_respuesta(historial)
        except Exception as e:
            print(f"\n[Error al contactar con Ollama: {e}]")
            print("[Asegúrate de que Ollama está corriendo en segundo plano.]\n")
            historial.pop()  # Quitar el mensaje que falló
            continue

        print(respuesta)
        print()

        # Añadir respuesta al historial
        historial.append({"role": "assistant", "content": respuesta})

        # Recortar historial si es necesario
        historial = recortar_historial(historial)


# ── PUNTO DE ENTRADA ─────────────────────────────────────────
if __name__ == "__main__":
    iniciar_chat()