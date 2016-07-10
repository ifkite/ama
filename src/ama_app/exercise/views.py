from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ama_app.exercise.models import Question
import ama_app.exercise.excepts as excepts
import json
from mongoengine.errors import ValidationError, DoesNotExist
import logging

log = logging.getLogger(__file__)


class QuestionsView(APIView):
    FETCH_NUM = 10

    def _set_question(self, params):
        question = Question(score=params.get('score'), tag=params.get('tag'))
        question.set_content(content_type=params.get('content_type'), content_data=json.loads(params.get('content')))
        question.save()
        # serialize
        return {"data": json.loads(question.to_json())}

    def _get_questions(self, params):
        tag = params.get('tag')
        if tag:
            questions = Question.objects.filter(tag).order_by('rank')[:self.FETCH_NUM]
        else:
            questions = Question.objects.all().order_by('rank')[:self.FETCH_NUM]

        return {
                "data": [json.loads(question.to_json()) for question in questions]
        }

    def get(self, request):
        '''
        get questions
        '''
        params = {
                'tag': request.GET.get('tag')
        }
        data = self._get_questions(params)
        return Response(data)

    def post(self, request):
        '''
        create a new question
        '''

        params = {
                'content_type': request.POST.get('type'),
                'content': request.POST.get('content'),
                'score': request.POST.get('score'),
                #'author': request.user,
                'tag': request.POST.get('tag'),
        }
        try:
            data = self._set_question(params)
            return Response(data)
        except (ValueError, excepts.AnswerNotExistExcept) as e:
            log.warning("params: {0}, err_msg: {1}".format(str(params), e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.warning("params: {0}, err_msg: {1}".format(str(params), e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionView(APIView):
    def _update_question(self, params):
        question = Question.objects.get(id=params.get('id'))

        for k, v in params.iteritems():
            if k in ('tag', 'score'):
                setattr(question, k, v)

        content_type, content_data = params.get('content_type'), params.get('content')
        if content_type and content_data:
            question.set_content(content_type=content_type, content_data=json.loads(content_data))

        question.save()
        return {
                "data": json.loads(question.to_json())
        }

    def put(self, request, id):
        params = {
                'id': id,
                'content_type': request.data.get('type'),
                'content': request.data.get('content'),
                'score': request.data.get('score'),
                'tag': request.data.get('tag'),
        }
        try:
            data = self._update_question(params)
            return Response(data)
        except (DoesNotExist, ValidationError) as e:
            log.warning("params: {0}, err_msg: {1}".format(str(params), e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            log.warning("params: {0}, err_msg: {1}".format(str(params), e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
