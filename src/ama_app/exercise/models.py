#! encoding=UTF-8
from __future__ import unicode_literals

from mongoengine import DynamicDocument, IntField, StringField, ListField, EmbeddedDocument
from ama_app.exercise.excepts import ContentExcept, AnswerNotExistExcept

import logging
log = logging.getLogger(__file__)

class Choice(EmbeddedDocument):
    question = StringField(require=True)
    options = ListField(StringField(), require=True)
    answer = StringField(require=True)

    def set_content(self, content_data):
        for k, v in content_data.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

        if self.answer not in self.options:
            log.warning("set content failed: answer {0} not in content {1}".format(str(self.answer), str(self.options)))
            raise AnswerNotExistExcept


class Question(DynamicDocument):
    CHOICE = 'CHOICE'
    Q_TYPE = (CHOICE, 'choice')
    Q_TYPE_DICT = {CHOICE: Choice}
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'
    LEVEL= ((EASY, 'easy'),
            (MEDIUM, 'medium'),
            (HARD, 'hard'),
           )

    type = StringField(choices=Q_TYPE)
    score = IntField(min_value=1, default=1)
    # content = EmbeddedDocumentField(require=True)
    avg_time = IntField()
    level = StringField(choices=LEVEL, default=MEDIUM)
    tag = StringField()
    like =  IntField(min_value=0, default=0)
    dislike =  IntField(min_value=0, default=0)
    render_time = IntField(min_value=0, default=0)
    author = IntField()
    meta = {'collection': 'question',
            'indexes':[
                ('type', 'like', 'dislike', 'render_time')
            ],
           }

    def set_content(self, content_type, content_data):
        if content_type not in self.Q_TYPE_DICT:
            log.warning("set content faild: content type {0} not support".format(content_type))
            raise ContentExcept
        self.type = content_type
        Content = self.Q_TYPE_DICT.get(content_type)
        content = Content()
        content.set_content(content_data)
        self.content = content
