# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from models.conversation_flow import ConversationFlow, Question
from models.restaurant_query import RestaurantQuery
from config.config import ConfigReader
from services.gmaps_service import GoogleMaps_Service

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState
from botbuilder.schema import ChannelAccount
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer


class RestaurantBot(ActivityHandler):
    # initialize bot conversation state
    def __init__(self, conversation_state: ConversationState):
        if conversation_state is None:
            raise TypeError(
                "[RestaurantBot]: Missing parameter. conversation_state is required but None was given"
            )
        self.gmaps_service = GoogleMaps_Service()
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.luis_app_id=self.configuration['LUIS_APP_ID']
        self.luis_endpoint_key = self.configuration['LUIS_ENDPOINT_KEY']
        self.luis_endpoint = self.configuration['LUIS_ENDPOINT']
        self.luis_app = LuisApplication(self.luis_app_id,self.luis_endpoint_key,self.luis_endpoint)
        self.luis_options = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.luis_recognizer = LuisRecognizer(application=self.luis_app,prediction_options=self.luis_options,include_api_results=True)
        self.conversation_state = conversation_state
        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.query_accessor = self.conversation_state.create_property("RestaurantQuery")

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! I am the restaurant expert bot!")

    async def on_message_activity(self, turn_context: TurnContext):
        flow = await self.flow_accessor.get(turn_context, ConversationFlow)
        query = await self.query_accessor.get(turn_context, RestaurantQuery)
        await self._luis_get_restaurant_info(query, turn_context)
        await self.conversation_state.save_changes(turn_context)
    
    async def _luis_get_restaurant_info(self, query: RestaurantQuery, turn_context: TurnContext):
        luis_result = await self.luis_recognizer.recognize(turn_context)
        result = luis_result.properties["luisResult"]
        print(result)


    async def _get_restaurant_info(self, flow: ConversationFlow, query: RestaurantQuery, turn_context: TurnContext):
        user_input = turn_context.activity.text.strip()

        if flow.last_question_asked == Question.NONE:
            await turn_context.send_activity(
                MessageFactory.text("Let's get started. What do you want to eat?")
            )
            flow.last_question_asked = Question.FOOD
        
        elif flow.last_question_asked == Question.FOOD:
            query.food = user_input
            await turn_context.send_activity(
                MessageFactory.text("Good choice!")
            )
            await turn_context.send_activity(
                MessageFactory.text("Where are you?")
            )
            flow.last_question_asked = Question.LOC
        
        elif flow.last_question_asked == Question.LOC:
            query.loc = user_input
            await turn_context.send_activity(
                MessageFactory.text("Great! Let me find something for you!")
            )
            nearest = self.gmaps_service.find_nearest(query.food, query.loc)
            if nearest != None:
                await turn_context.send_activity(
                    MessageFactory.text(f"The closest {query.food} restaurant is {nearest['name']}")
                )
            flow.last_question_asked = Question.NONE

        return
