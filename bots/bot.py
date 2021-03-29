# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from models.conversation_flow import ConversationFlow, Question
from models.restaurant_query import RestaurantQuery
from config.config import ConfigReader
from helpers.luis_helper import LuisHelper, Intent
from helpers.dialog_helper import DialogHelper

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, ConversationState
from botbuilder.schema import ChannelAccount
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer
from botbuilder.dialogs import Dialog


class RestaurantBot(ActivityHandler):
    # initialize bot conversation state
    def __init__(self, conversation_state: ConversationState, dialog: Dialog):
        if conversation_state is None:
            raise TypeError(
                "[RestaurantBot]: Missing parameter. conversation_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[RestaurantBot]: Missing parameter. dialog is required")
        self.dialog = dialog
        self.conversation_state = conversation_state

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! I am the restaurant expert bot!")
                await DialogHelper.run_dialog(
                    self.dialog,
                    turn_context,
                    self.conversation_state.create_property("DialogState"),
                )
        await self.conversation_state.save_changes(turn_context, False)

    async def on_message_activity(self, turn_context: TurnContext):
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
        await self.conversation_state.save_changes(turn_context, False)
        