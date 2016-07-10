from rest_framework.views import APIView
from rest_framework.response import Response
from ama_app.exercise.models import Question
import json


class QuestionsView(APIView):
    FETCH_NUM = 10

    def _set_question(self, params):
        question = Question(score=params.get('score'), tag=params.get('tag'))
        content_data = json.loads(params.get('content'))
        question.set_content(content_type=params.get('content_type'), content_data=content_data)
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
                "tag": request.GET.get('tag')
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
        data = self._set_question(params)
        return Response(data)


class QuestionView(APIView):

    def put(self, request):
        pass
