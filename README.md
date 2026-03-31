# Turito WhatsApp Bot

An automated AI assistant for Turito integrated with WhatsApp via Picky Assist.

## Prerequisites
- Python 3.10+
- OpenAI API Key
- Picky Assist Account and API Token

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Deshavath-Venkateswara-Naik/Whatsapp-Bot.git
    cd Whatsapp-Bot
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_openai_key
    PICKY_API_TOKEN=your_picky_assist_token
    PICKY_APP_ID=your_picky_app_id
    ```

## Running the Bot

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The server will be available at `http://localhost:8000`.

## Endpoints
-   `GET /`: Health check.
-   `POST /webhook`: Message entry point for Picky Assist.
-   `POST /api/v2/push`: Local proxy for Picky Assist API.

## Project Structure
-   `app/main.py`: Main FastAPI application.
-   `app/services/`: Integration services (OpenAI, Picky Assist).
-   `app/config.py`: Configuration management.
-   `DOCUMENTATION.md`: Full technical overview.
