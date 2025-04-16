# How to use?

## Setup

- Grundsätzlich muss mal n8n als lokale instanz gestartet sein.
- `n8n` ausführen
- Mit Credentials einloggen (oder Account erstellen)
- Damit das Chat UI funktioniert, muss man  `python rag_chat.py` innerhalb des chat UI ordners ausführen.
- Dann sollte das Chat UI unter http://127.0.0.1:7860 erreichbar sein.

## Test / Production Webhook
- Im N8n Workflow kann man einstellen, ob der Workflow nun aktiv (production) oder test für Debugging ist.
- Je nachdem was mann machen will, muss man im `rag_chat.py` die entsprechende Webhook URL setzen:
  - Prod URL = "http://localhost:5678/webhook/rag/query"
  - Test URL = "http://localhost:5678/webhook-test/rag/query"

## Dataset Erstellung
- Möchte man eine neue RAG DB erstellen oder neue Daten hinzufügen, muss die Chroma RAG-DB neu generiert werden.
- Existiert bereits ein chroma_db Ordner im Projekt muss der gelöscht werden.
- Falls nicht kann einfach `python ingest.py` ausgeführt werden.
- Das Script loopt durch alle Inhalte des data Ordners mit filetype ".md", ".txt", ".php", ".js", ".jsx", ".ts", ".tsx", ".yaml", ".yml", ".json", ".xml", ".pdf" und vektorisiert die Daten.
- Das geht wirklich erstaunlich gut mit den Macs und >3000 files dauern nur wenige Sekunden.

## Debugging
Wenn mal python am neven ist und sowas ähnliches ausspuckt: 
`error: externally-managed-environment
× This environment is externally managed
╰─> To install Python packages system-wide, try brew`

Dann im repo eine virtuelle Umgebung aktivieren: `source .venv/bin/activate`
