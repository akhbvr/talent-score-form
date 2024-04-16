from django.urls import path
from core.api.views import (
        StageAPI,
        SubStageAPI,
        QuestionAPI,
        AnswerAPI,
        FormResultAPI
    )


urlpatterns = [
    path('stages/', StageAPI.as_view()),

    path('sub-stages/<uuid:stage_id>/', SubStageAPI.as_view()),
    path('sub-stages/', SubStageAPI.as_view()),

    path('questions/<uuid:sub_stage_id>/', QuestionAPI.as_view()),
    path('questions/', QuestionAPI.as_view()),

    path('answers/', AnswerAPI.as_view()),
    path('test/', FormResultAPI.as_view()),
]