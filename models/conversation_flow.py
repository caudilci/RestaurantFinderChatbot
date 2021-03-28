from enum import Enum

class Question(Enum):
    FOOD = 1
    LOC = 2
    NONE = 3

class ConversationFlow:
    def __init__(self, last_question_asked: Question = Question.NONE,):
        self.last_question_asked = last_question_asked