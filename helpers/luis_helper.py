# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# Heavily modified from original
# Original can be found at https://github.com/Microsoft/BotBuilder-Samples

from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext
from models.restaurant_query import RestaurantQuery


class Intent(Enum):
    RESTAURANT = "restaurant"
    CANCEL = "Cancel"
    NONE_INTENT = "None"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            intent = list(recognizer_result.intents.keys())[0]

            if intent == Intent.RESTAURANT.value:
                result = RestaurantQuery()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                food_entities = recognizer_result.entities.get("$instance", {}).get(
                    "food", []
                )
                if len(food_entities) > 0:
                    result.food = food_entities[0]["text"]
                else:
                    result.food = None

                loc_entities = recognizer_result.entities.get("$instance", {}).get(
                    "location", []
                )
                if len(loc_entities) > 0:
                    result.loc = loc_entities[0]["text"].capitalize()
                else:
                    result.loc = None

        except Exception as exception:
            print(exception)

        return intent, result
