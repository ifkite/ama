class QuestionExcept(Exception):
    pass


class ContentExcept(QuestionExcept):
    pass


class ChoiceExcept(Exception):
    pass


class AnswerNotExistExcept(ChoiceExcept):
    pass
