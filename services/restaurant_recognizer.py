# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# Heavily modified from original
# Original can be found at https://github.com/Microsoft/BotBuilder-Samples

from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer
from botbuilder.core import Recognizer, RecognizerResult, TurnContext
from config.config import ConfigReader

class RestaurantRecognizer(Recognizer):
    def __init__(self):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.luis_app_id=self.configuration['LUIS_APP_ID']
        self.luis_endpoint_key = self.configuration['LUIS_ENDPOINT_KEY']
        self.luis_endpoint = self.configuration['LUIS_ENDPOINT']
        self.luis_app = LuisApplication(self.luis_app_id,self.luis_endpoint_key,self.luis_endpoint)
        self.luis_options = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.luis_recognizer = LuisRecognizer(application=self.luis_app,prediction_options=self.luis_options,include_api_results=True)

    @property
    def is_configured(self) -> bool:
        # Returns true if luis is configured in the config.py and initialized.
        return self.luis_recognizer is not None

    async def recognize(self, turn_context: TurnContext) -> RecognizerResult:
            return await self.luis_recognizer.recognize(turn_context)