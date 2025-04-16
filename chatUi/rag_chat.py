import gradio as gr
import requests

#Prod URL
# WEBHOOK_URL = "http://localhost:5678/webhook/rag/query"

#Test URL
WEBHOOK_URL = "http://localhost:5678/webhook-test/rag/query"

def chat_fn(message, history):
    payload = {
        "question": message,
        "history": history or []
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        answer = data.get("text", "Keine Antwort erhalten.")
    except Exception as e:
        answer = f"Fehler beim Abrufen der Antwort: {e}"
    history = history or []
    history.append((message, answer))
    return "", history

with gr.Blocks() as demo:
    gr.Markdown("IWF AI (Ultra Smart)")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Deine Frage eingeben und Enter drücken...")
    clear = gr.Button("Chat leeren")
    msg.submit(chat_fn, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()