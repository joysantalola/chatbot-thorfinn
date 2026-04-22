# ============================================================
# CHATBOT DE THORFINN - INTERFAZ WEB CON GRADIO 6.13
# Archivo: app.py
# ============================================================

import gradio as gr
import ollama
import os
import base64
from persona import SYSTEM_PROMPT

# ── CONFIGURACIÓN ────────────────────────────────────────────
MODELO = "thorfinn"
MAX_MENSAJES_HISTORIAL = 20
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ── CARGAR IMAGEN EN BASE64 PARA EL HEADER ──────────────────
def cargar_imagen_base64():
    avatar_path = os.path.join(BASE_DIR, "img", "thorfinn.png")
    if os.path.exists(avatar_path):
        with open(avatar_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{data}"
    return None

IMAGEN_B64 = cargar_imagen_base64()
AVATAR_PATH = os.path.join(BASE_DIR, "img", "thorfinn.png")


# ── CONVERSIÓN SEGURA DEL HISTORIAL ─────────────────────────
def extraer_texto(content) -> str:
    """
    Gradio moderno puede guardar el contenido como:
      - str                       → lo devuelve tal cual
      - list de bloques           → [{'type': 'text', 'text': '...'}, ...]
    Esta función siempre devuelve un string plano.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        partes = []
        for bloque in content:
            if isinstance(bloque, dict) and bloque.get("type") == "text":
                partes.append(bloque.get("text", ""))
            elif isinstance(bloque, str):
                partes.append(bloque)
        return " ".join(partes)
    return str(content) if content is not None else ""


def mensaje_a_dict(m) -> dict:
    """
    Gradio 6.13+ puede pasar el historial como ChatMessage o como dict,
    y el content puede ser str o lista de bloques multimodal.
    Esta función normaliza todos los casos.
    """
    if isinstance(m, dict):
        role = m.get("role", "user")
        content = extraer_texto(m.get("content", ""))
    else:
        role = m.role
        content = extraer_texto(m.content)
    return {"role": role, "content": content}


# ── FUNCIÓN PRINCIPAL DE RESPUESTA ──────────────────────────
def responder(mensaje: str, historial: list):
    if not mensaje.strip():
        return historial, ""

    # Convertir historial a dicts para Ollama
    historial_ollama = [mensaje_a_dict(m) for m in historial]

    # Recortar si es muy largo
    if len(historial_ollama) > MAX_MENSAJES_HISTORIAL:
        historial_ollama = historial_ollama[-MAX_MENSAJES_HISTORIAL:]

    # System prompt + historial + mensaje nuevo
    mensajes_completos = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + historial_ollama
        + [{"role": "user", "content": mensaje}]
    )

    try:
        resultado = ollama.chat(
            model=MODELO,
            messages=mensajes_completos,
            options={"temperature": 0.75, "num_predict": 300, "repeat_penalty": 1.15}
        )
        texto = resultado["message"]["content"]

    except Exception as e:
        texto = (
            f"[Error: No se pudo conectar con Ollama. "
            f"Asegúrate de que está corriendo en segundo plano. "
            f"Detalle: {e}]"
        )

    # Siempre guardar como dicts simples para evitar problemas de formato
    historial = list(historial) + [
        {"role": "user", "content": mensaje},
        {"role": "assistant", "content": texto},
    ]

    return historial, ""


# ── DISEÑO DE LA INTERFAZ ────────────────────────────────────
def crear_interfaz():

    DESCRIPCION = (
        "Habla con Thorfinn Karlsefni, explorador nórdico y pacifista "
        "en busca de Vinland. Sabio, tranquilo, con el peso de su pasado."
    )

    EJEMPLOS = [
        "¿Qué es Vinland para ti?",
        "¿Tienes enemigos?",
        "Háblame de tu padre Thors.",
        "¿Merece la pena construir la paz?",
        "¿Qué pasó con Askeladd?",
        "¿Quién es Einar para ti?",
    ]

    # Construir el bloque de cabecera con o sin imagen
    if IMAGEN_B64:
        header_html = f"""
            <div style="text-align:center; padding:1.5rem 0 0.5rem;">
                <img src="{IMAGEN_B64}"
                     style="width:120px; height:120px; border-radius:50%;
                            object-fit:cover; margin-bottom:12px;
                            border:2px solid #94a3b8;"
                     alt="Thorfinn Karlsefni"/>
                <h1 style="font-size:1.6rem; font-weight:600; margin:0;">
                    ⚔️ Thorfinn Karlsefni
                </h1>
                <p style="font-size:0.9rem; opacity:0.7; margin:4px 0 0;">
                    Vinland Saga — Chatbot de IA local con llama + Ollama
                </p>
                <span style="display:inline-block; font-size:0.75rem;
                             padding:2px 10px; border-radius:99px;
                             background:#e2e8f0; color:#475569; margin-top:6px;">
                    Adulto — Rumbo a Vinland
                </span>
            </div>
        """
    else:
        header_html = """
            <div style="text-align:center; padding:1.5rem 0 0.5rem;">
                <h1 style="font-size:1.6rem; font-weight:600; margin:0;">
                    ⚔️ Thorfinn Karlsefni
                </h1>
                <p style="font-size:0.9rem; opacity:0.7; margin:4px 0 0;">
                    Vinland Saga — Chatbot de IA local con llama + Ollama
                </p>
                <span style="display:inline-block; font-size:0.75rem;
                             padding:2px 10px; border-radius:99px;
                             background:#e2e8f0; color:#475569; margin-top:6px;">
                    Adulto — Rumbo a Vinland
                </span>
            </div>
        """

    with gr.Blocks(title="Thorfinn — Vinland Saga Chatbot") as interfaz:

        gr.HTML(header_html)

        chatbot = gr.Chatbot(
            label="",
            height=420,
            show_label=False,
            avatar_images=(
                None,
                AVATAR_PATH if os.path.exists(AVATAR_PATH) else None,
            ),
        )

        with gr.Row():
            entrada = gr.Textbox(
                placeholder="Escribe tu mensaje...",
                show_label=False,
                scale=9,
                container=False,
                autofocus=True,
            )
            boton_enviar = gr.Button(
                "Enviar",
                scale=1,
                variant="primary",
            )

        with gr.Row():
            boton_limpiar = gr.Button("🗑️  Nueva conversación", size="sm")

        gr.Examples(
            examples=EJEMPLOS,
            inputs=entrada,
            label="Preguntas de ejemplo",
        )

        gr.Markdown(f"> {DESCRIPCION}")

        # ── EVENTOS ─────────────────────────────────────────
        boton_enviar.click(
            fn=responder,
            inputs=[entrada, chatbot],
            outputs=[chatbot, entrada],
        )

        entrada.submit(
            fn=responder,
            inputs=[entrada, chatbot],
            outputs=[chatbot, entrada],
        )

        boton_limpiar.click(
            fn=lambda: ([], ""),
            outputs=[chatbot, entrada],
        )

    return interfaz


# ── PUNTO DE ENTRADA ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n⚔️  Iniciando Thorfinn Chatbot...")
    print(f"   Modelo  : {MODELO}")
    print(f"   Avatar  : {AVATAR_PATH}")
    print(f"   Imagen header: {'✓ cargada' if IMAGEN_B64 else '✗ no encontrada'}")
    print("   Etapa   : ADULTO — Rumbo a Vinland")
    print("   Abriendo navegador en http://localhost:7860\n")

    app = crear_interfaz()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        show_error=True,
        allowed_paths=[BASE_DIR],
        theme=gr.themes.Soft(
            primary_hue="slate",
            secondary_hue="gray",
        ),
    )