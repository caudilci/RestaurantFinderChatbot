# Nearest Restaurant Finder Chatbot

This bot was bootstrapped using example code from https://github.com/microsoft/BotBuilder-Samples.

This is a chatbot made to return nearest restaurants meeting user search parameters utilizing Microsoft Botbuilder SDK, LUIS from Azure Cognitive Services, and Google Places API

## Usage

API keys should be placed in a `config.ini` file in the project root directory (where `app.py` is)

config.ini format:
```
[DEFAULT]
GOOGLE_PLACES_API_KEY=[Your key here]
LUIS_APP_ID=[Your key here]
LUIS_ENDPOINT_KEY=[Your key here]
LUIS_ENDPOINT=[Your endpoint here]
```

Dependencies can be installed with `pip install -r requirements.txt`

To run the bot on localhost, just run `app.py`