from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from ama_app.exercise.models import Question
import json


def home(request):
    '''
    this is a temparory solution.
    final soluton relies on the solution of front end
    '''
    tag = request.GET.get('tag')
    if tag:
        questions = Question.objects.filter(tag).order_by('rank')[:10]
    else:
        questions = Question.objects.all().order_by('rank')[:10]

    context = {"questions" : questions}
    # which `home.html` not exists yet
    return render_to_response("home.html", context=context)


def publish_handler(params, *args, **kwargs):
    question = Question(score=params.get('score'), tag=params.get('tag'))
    question.set_content(content_type=params.get('content_type'), content_data=json.loads(params.get('content')))
    question.save()
    return redirect(reverse('home'))


def publish_page(request):
    return render(request, "publish.html")


@login_required
@require_http_methods(["GET", "POST"])
def publish(request):
    if request.method == "POST":
        params = {
                "score": request.POST.get('score'),
                "tag": request.POST.get('tag'),
                "content_type": request.POST.get('content_type'),
                "content": request.POST.get('content')
        }

        return publish_handler(params, request=request)
    else:
        return publish_page(request)
