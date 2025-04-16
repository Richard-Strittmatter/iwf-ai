# RAG Chat-System mit n8n

> Ein Retrieval-Augmented Generation Chat-System basierend auf n8n-Workflows und ChromaDB.

## 📋 Übersicht

Dieses Projekt integriert ein RAG (Retrieval-Augmented Generation) Chat-System mit n8n-Workflows. Es ermöglicht das Verarbeiten von Dokumenten und das Durchführen von kontextbezogenen Chats basierend auf den bereitgestellten Daten.

## 🔧 Voraussetzungen 

- **n8n**: Lokal installierte Instanz
- **Node.js**: Version 18 oder neuer
- **Python**: Für die Chat-UI und Datenvektorisierung

### Installation von n8n
```bash
# n8n global installieren
npm install -g n8n

# Auf die neueste Version aktualisieren
npm update -g n8n
```
> 📚 [Offizielle n8n-Dokumentation zur Installation](https://docs.n8n.io/hosting/installation/npm/#install-globally-with-npm)

## 🚀 Einrichtung

1. **n8n starten**:
   ```bash
   n8n
   ```
   Nach dem Start mit Ihren Anmeldedaten einloggen oder einen neuen Account erstellen.

2. **n8n Workflow importieren**:
   - Kopieren Sie den Inhalt der Datei `n8n_workflow.json` (siehe unten)
   - In n8n: Workflows > + > Import from clipboard
   - **Wichtig:** Passen Sie im Workflow den Pfad im "Execute Command"-Knoten an:
     ```
     =/Users/{DeinName}/repositories/iwf-ai/.venv/bin/python /Users/{DeinName}/repositories/iwf-ai/query.py {{$json["body"]["question"]}}
     ```
     Ersetzen Sie `{DeinName}` mit Ihrem tatsächlichen Benutzernamen/Pfad

3. **Chat-UI starten**:
   ```bash
   # Im Chat-UI-Ordner ausführen
   python rag_chat.py
   ```
   Die Chat-Benutzeroberfläche ist dann unter [http://127.0.0.1:7860](http://127.0.0.1:7860) erreichbar.

## 🔄 Webhooks konfigurieren

Im n8n-Workflow können du zwischen zwei Modi wählen:
- **Produktionsmodus**: Aktiver Workflow für den regulären Betrieb
- **Testmodus**: Für Debugging-Zwecke

Setzen Du die entsprechende Webhook-URL in `rag_chat.py`:
- Produktions-URL: `http://localhost:5678/webhook/rag/query`
- Test-URL: `http://localhost:5678/webhook-test/rag/query`

## 📊 Datensatz erstellen

Um eine neue RAG-Datenbank zu erstellen oder bestehende Daten zu aktualisieren:

1. Falls vorhanden, lösche den `chroma_db`-Ordner im Projekt
2. Führe das Ingest-Skript aus:
   ```bash
   python ingest.py
   ```

Das Skript verarbeitet alle Dateien im `data`-Ordner mit folgenden Formaten:
`.md`, `.txt`, `.php`, `.js`, `.jsx`, `.ts`, `.tsx`, `.yaml`, `.yml`, `.json`, `.xml`, `.pdf`

> 💡 **Hinweis**: Der Vektorisierungsprozess ist besonders effizient auf Mac-Systemen und kann mehrere tausend Dateien in Sekundenschnelle verarbeiten.

## 🐛 Fehlerbehebung

Wenn du folgende Python-Fehlermeldung erhält:
```bash
   error: externally-managed-environment × This environment is externally managed ╰─> To install Python packages system-wide, try brew
   ```
Aktiviere eine virtuelle Umgebung im Repository:
```bash
source .venv/bin/activate
```

## 🏗️ Projektstruktur

- `/data` - Ordner für zu verarbeitende Dokumente
- `/chroma_db` - Generierte Vektordatenbank (wird automatisch erstellt)
- `rag_chat.py` - Hauptscript für die Chat-UI
- `ingest.py` - Script zur Verarbeitung und Vektorisierung von Dokumenten
- `query.py` - Hilfsskript zum Testen von Abfragen gegen die Vektordatenbank

## 📌 Hauptkomponenten

- **ChromaDB**: Vektordatenbank zur Speicherung der Dokumenteinbettungen
- **Hugging Face Embeddings**: Für die Umwandlung von Text in Vektordarstellungen
- **n8n Workflows**: Orchestrierung der RAG-Anfragen und Antworten
- **Gradio UI**: Einfache Web-Oberfläche für die Interaktion mit dem System
