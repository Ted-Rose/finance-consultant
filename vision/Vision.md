## Goal of users experience with MVP
1. User clicks button
2. Asks a question regarding his transactions that are previously stored in the project
3. Gets an AI generated response in text format

## Tech stack
- UI (button, AI output text):
    - Plain html
- Audio transcription:
    - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- AI:
    - Containerized [Ollama](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image)