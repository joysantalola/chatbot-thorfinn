# Thorfinn Chatbot — Vinland Saga AI

Chatbot de inteligencia artificial que simula a **Thorfinn Karlsefni**,
el protagonista del manga *Vinland Saga* de Makoto Yukimura.

![Thorfinn](img/thorfinn.png)

---

## Tecnologías

| Herramienta | Función |
|---|---|
| [Ollama](https://ollama.com) | Motor LLM local (sin internet, sin coste) |
| Llama 3 (Meta) | Modelo de lenguaje base |
| Python 3.11+ | Backend del chatbot |
| Gradio 6 | Interfaz web |

---

## Características

- 100% local — sin APIs de pago, sin envío de datos a la nube
- Personalidad profunda basada en el lore real del manga
- Memoria conversacional (recuerda el contexto de la conversación)
- Dos modos: interfaz web (Gradio) y terminal
- System prompt con prompt engineering avanzado

---

## Cómo ejecutarlo

### Requisitos previos
- [Ollama](https://ollama.com) instalado y corriendo
- Python 3.11 o superior

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/joysantalola/chatbot-thorfinn.git
cd chatbot-thorfinn

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Descargar el modelo
ollama pull llama3
```

### Ejecutar

**Interfaz web** (recomendado):
```bash
python app.py
```
Abre automáticamente en `http://localhost:7860`

**Terminal**:
```bash
python chatbot.py
```

---

## Estructura del proyecto

```
chatbot-thorfinn/
├── app.py           # Interfaz web con Gradio
├── chatbot.py       # Versión de terminal
├── persona.py       # Personalidad y system prompt de Thorfinn
├── requirements.txt # Dependencias Python
└── img/
    └── thorfinn.png # Avatar del chatbot
```

---

## Aprendizajes aplicados

- Integración de LLMs locales con Python
- **Prompt engineering** — diseño de personalidad compleja con lore real
- Memoria conversacional con gestión de historial
- Interfaz web con Gradio
- Estructura de proyecto limpia para portfolio

---
