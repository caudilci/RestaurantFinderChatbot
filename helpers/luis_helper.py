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

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.RESTAURANT.value:
                result = RestaurantQuery()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                food_entities = recognizer_result.entities.get("$instance", {}).get(
                    "food", []
                )
                if len(food_entities) > 0:
                    if recognizer_result.entities.get("food", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.food = to_entities[0]["text"].capitalize()
                    else:
                        result.food = None

                from_entities = recognizer_result.entities.get("$instance", {}).get(
                    "location", []
                )
                if len(from_entities) > 0:
                    if recognizer_result.entities.get("location", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.loc = from_entities[0]["text"].capitalize()
                    else:
                        result.loc = None

        except Exception as exception:
            print(exception)

        return intent, result
