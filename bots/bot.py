# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from models.conversation_flow import ConversationFlow, Question
from models.query import Query

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState
from botbuilder.schema import ChannelAccount
# from botbuilder.dialogs import Dialog
import googlemaps

class RestaurantBot(ActivityHandler):
    # initialize bot conversation state
    def __init__(self, conversation_state: ConversationState):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        
        self.conversation_state = conversation_state
        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.query_accessor = self.conversation_state.create_property("Query")

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! I am the restaurant expert bot!")

    async def on_message_activity(self, turn_context: TurnContext):
        flow = await self.flow_accessor.get(turn_context, ConversationFlow)
        query = await self.query_accessor.get(turn_context, Query)
        await self._get_restaurant_info(flow, query, turn_context)
        await self.conversation_state.save_changes(turn_context)
    
    async def _get_restaurant_info(self, flow: ConversationFlow, query: Query, turn_context: TurnContext):
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
            await turn_context.send_activity(
                MessageFactory.text(f"Data: {query.food}, {query.loc}")
            )
            flow.last_question_asked = Question.NONE

        return
