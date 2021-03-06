from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from services.gmaps_service import GoogleMapsService

class RestaurantFinderDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(RestaurantFinderDialog, self).__init__(dialog_id or RestaurantFinderDialog.__name__)
        self.gmaps_service = GoogleMapsService()
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.food_step,
                    self.location_step,
                    self.confirm_step,
                    self.results1_step,
                    self.results2_step,
                    self.results3_step,
                ],
            )
        )
        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def food_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        restaurant_details = step_context.options

        if restaurant_details.food is None:
            message_text = "What would you like to eat?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(restaurant_details.food)
    
    async def location_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        restaurant_details = step_context.options

        # Capture the response to the previous step's prompt
        restaurant_details.food = step_context.result
        if restaurant_details.loc is None:
            message_text = "In what area do you want to eat?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(restaurant_details.loc)
    
    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        restaurant_details = step_context.options

        # Capture the results of the previous step
        restaurant_details.loc = step_context.result
        message_text = (
            f"So you're looking to eat {restaurant_details.food} in {restaurant_details.loc}, is that right?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
    
    async def results1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            restaurant_details = step_context.options
            result = self.gmaps_service.find_nearest(restaurant_details.food, restaurant_details.loc)
            msg_txt = f"The nearest restaurant meeting your search criteria is {result['name']} at {result['vicinity']}"
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
            message_text = (
            "Would you like to see the next closest restaurant?"
            )
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )

            # Offer a YES/NO prompt.
            return await step_context.prompt(
                ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
            await step_context.context.send_activity(message)
        elif result == None and step_context.result:
            msg_txt = f"Sorry, I couldn't find any restaurants meeting your requirements."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
            return await step_context.end_dialog()
        else:
            return await step_context.end_dialog()
    
    async def results2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        result = self.gmaps_service.find_next()
        if result != None and step_context.result:
            msg_txt = f"The next nearest restaurant meeting your search criteria is {result['name']} at {result['vicinity']}"
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
            message_text = (
            "Would you like to see the next closest restaurant?"
            )
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )

            # Offer a YES/NO prompt.
            return await step_context.prompt(
                ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
            await step_context.context.send_activity(message)
        elif result == None and step_context.result:
            msg_txt = f"Sorry, I couldn't find any restaurants meeting your requirements."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
            return await step_context.end_dialog()
        else:
            return await step_context.end_dialog()
    
    async def results3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        result = self.gmaps_service.find_next()
        if result != None and step_context.result:
            msg_txt = f"The next nearest restaurant meeting your search criteria is {result['name']} at {result['vicinity']}"
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
        elif result == None and step_context.result:
            msg_txt = f"Sorry, I couldn't find any restaurants meeting your requirements."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
        return await step_context.end_dialog()