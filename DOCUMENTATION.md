# Turito WhatsApp AI Bot - Technical Documentation

## Overview
The Turito WhatsApp AI Bot is a FastAPI-based application designed to provide automated, AI-driven responses to students and parents for the Turito education platform. It integrates WhatsApp via **Picky Assist** and core AI logic using **OpenAI's GPT-4o-mini**.

## System Architecture

The system operates as a reactive webhook service:

1.  **Picky Assist Webhook**: Incoming WhatsApp messages are delivered to the `/webhook` endpoint.
2.  **Processing Layer**: The application extracts the sender's number and message, applying URL decoding and sanitization.
3.  **AI Engine**: Messages are sent to OpenAI with a curated system prompt that defines the Turito persona, course information, and tone.
4.  **Response Delivery**: The generated response is pushed back to the user via Picky Assist's Direct API v2.

### Failover & Reliability
-   **AI Fallback**: If the OpenAI API is unreachable or returns an error (e.g., quota exceeded), the bot sends a polite fallback message directing the user to the Turito website.
-   **API Fallback**: If the Picky Assist Direct API v2 fails (e.g., 401 Unauthorized), the system automatically attempts to deliver the message via a pre-configured **Connector URL** fallback.

## Service Breakdown

### 1. Webhook (`/webhook`)
-   **Method**: `POST`
-   **Function**: Primary entry point. It handles raw payload parsing from Picky Assist, triggers the AI response, and automates the reply process.

### 2. Picky Assist Integration (`/api/v2/push`)
-   **Method**: `POST`
-   **Function**: Acts as a local proxy for the Picky Assist Direct API. This allows for centralized logging and easy updates to the push logic without touching the core webhook flow.

### 3. OpenAI Service (`app/services/openai_service.py`)
-   **Model**: `gpt-4o-mini`
-   **Context**: Injected via a comprehensive system prompt covering SAT, ACT, K-12 Tutoring, STEM, and Global Admissions support.

## Configuration (Environment Variables)

The bot requires the following keys in a `.env` file:

-   `OPENAI_API_KEY`: API key for OpenAI.
-   `PICKY_API_TOKEN`: Secret token from Picky Assist project settings.
-   `PICKY_APP_ID`: Application ID provided by Picky Assist.

## Maintenance and Logging
-   **Logs**: All interactions are logged to `bot.log` and the standard output.
-   **Error Tracking**: Critical errors in the webhook or services are caught and logged with stack traces for rapid debugging.
