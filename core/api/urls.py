from django.urls import path
from core.api.views import (
        StageAPI,
        SubStageAPI,
        QuestionAPI,
        AnswerAPI,
        testAPI
    )


urlpatterns = [
    path('stages/', StageAPI.as_view(), name="api_stages"),

    path('sub-stages/', SubStageAPI.as_view(), name="api_sub_stages"),
    path('sub_stages/<uuid:stage_id>/', SubStageAPI.as_view(), name='api_sub_stage'),

    path('questions/', QuestionAPI.as_view(), name="api_questions"),
    path('questions/<uuid:sub_stage_id>/', QuestionAPI.as_view(), name="api_question"),

    path('answers/', AnswerAPI.as_view(), name="api_answers"),
    path('test/', testAPI.as_view(), name="api_test"),
]