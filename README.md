# GPT-CLI
I created a command-line based utility that enabled you to have conversations with GPT-4 using Python. This was originally made in May 2023.

The goal of the project was to learn how to use env files within my projects. Concepts used:

1. Using Python Classes
2. Connecting to external APIs (Such as OpenAI's API)
3. Connecting to locally-hosted LLMs in LM Studio

The OpenAI Chat was supposed to be used for building a front-end for storing multiple:
- Conversations: Including the conversation history between a user and a LLM
- Models: Intended to be used to store GPT-3.5-Turbo, GPT-4, and Any locally-hosted models available in LM Studio
- Roles: These were the saved system messages that could help change the type of conversation I would be having with the AI. This means the instructions and provided context could be saved and managed, allowing for switching between roles fairly quickly
- Settings: This was intended to be used for changing setting such as whether TTS was enabled, saved settings between sessions, and helped ensure that model-switching (storing an ENV for each model such as GPT-4, GPT 3.5, or a Llama model running in LM Studio)
