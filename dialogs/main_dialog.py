from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints

from services.restaurant_recognizer import RestaurantRecognizer
from helpers.luis_helper import LuisHelper, Intent
from dialogs.restaurant_finder_dialog import RestaurantFinderDialog

class MainDialog(ComponentDialog):
    def __init__(self, luis_recognizer: RestaurantRecognizer, restaurant_finder_dialog: RestaurantFinderDialog):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self._luis_recognizer = luis_recognizer
        self._restaurant_finder_dialog_id = restaurant_finder_dialog.id
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(restaurant_finder_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        print("intro_step")
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
    
    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        print("act_step")
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )
        print(intent)
        if intent == Intent.RESTAURANT.value and luis_result:
            return await step_context.begin_dialog(self._restaurant_finder_dialog_id, luis_result)
        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)
        return step_context.next(None)
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result is not None:
            result = step_context.result
            msg_txt = f"The nearest restaurant meeting your search criteria is [Name Here]"
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
        
        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)