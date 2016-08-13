"""ama_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from ama_app.exercise.apis import QuestionsView, QuestionView
from ama_app.exercise.views import home, publish

question_patterns = [
    url(r'^questions/(?P<id>[^/]*)/?$', QuestionView.as_view(), name='v1_question'),
    url(r'^questions/?$', QuestionsView.as_view(), name='v1_questions'),
]

urlpatterns = [
    url(r'^api/v1/', include(question_patterns)),
    url(r'^$', home, name='home'),
    url(r'^publish$', publish, name='publish'),
]
