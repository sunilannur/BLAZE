"""

This file defines the 5 different commmands that the bot supports. 

"""

from webex_bot.models.command import Command 
from webex_bot.models.response import response_from_adaptive_card

from webexteamssdk.models.cards import TextBlock, FontWeight, FontSize, Column, AdaptiveCard, ColumnSet, \
    Text, Image, HorizontalAlignment

from webexteamssdk.models.cards.actions import OpenUrl
from help import SummarizeTranscripts,SearchTranscripts,ListMeetingTranscripts

class EmptySpace(Command): 
    def __init__(self): 
        super().__init__(
            command_keyword="cls",
            help_message="cls: (do not use) debugging/visualization purposes", 
            card = None
        )

    def execute(self, message, attachment_actions, query_info):
        return 

class ListTranscripts(Command):
    def __init__(self): 
        super().__init__(
            command_keyword="list",
            help_message="list: List all meetings", 
            card = None
        )

    def execute(self, message, attachment_actions, query_info):
        res = ListMeetingTranscripts()
        return f"{res}"


class SummarAcross(Command): 
    def __init__(self, transcriptFileName): 
        super().__init__(
            command_keyword="summarize",
            help_message="summarize [<meeting_id>,<meeting_id>,...] or all: Summarize across all meeting transcripts", 
            card = None
        )
        self.transcriptFileName = transcriptFileName 

    def execute(self, message, attachment_actions, query_info):
        res = SummarizeTranscripts(self.transcriptFileName,message)
        return f"{res}"


class SearchAcross(Command): 
    def __init__(self, transcriptFileName): 
        super().__init__(
            command_keyword="search",
            help_message="search <query>: Search across all meeting transcripts", 
            card = None
        )
        self.transcriptFileName = transcriptFileName 

    def execute(self, message, attachment_actions, query_info):
        res = SearchTranscripts(message)
        return f"{res}"

