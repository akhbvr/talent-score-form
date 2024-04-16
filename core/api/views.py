from rest_framework.views import APIView
from django.http import JsonResponse
import re
from django.db import transaction

from core.models import (
    Stage,
    SubStage,
    Question,
    Answer,
    FormStage,
    FormSubStage,
    FormQuestion,
    FormAnswer,
    FormResult,
)
from core.api.serializers import (
    StageSerializer,
    SubStageSerializer,
    QuestionSerializer,
    AnswerSerializer,
    FormSerializer,
    StageAllDataSerializer,
)


class StageAPI(APIView):

    def get(self, *args, **kwargs):
        stages = Stage.objects.prefetch_related("sub_stages__questions__answers")
        # serializer = StageSerializer(stages, many=True)
        serializer = StageAllDataSerializer(stages, many=True)

        return JsonResponse(serializer.data, safe=False)


class SubStageAPI(APIView):

    def get(self, *args, **kwargs):
        stage_id = self.kwargs.get("stage_id")
        if stage_id:
            sub_stage = SubStage.objects.filter(parent_stage=stage_id).prefetch_related(
                "questions"
            )
            if not sub_stage:
                return JsonResponse({"message": "Sub stage not found!"})
            serializer = SubStageSerializer(sub_stage, many=True)
        else:
            sub_stages = SubStage.objects.all()
            serializer = SubStageSerializer(sub_stages, many=True)

        return JsonResponse(serializer.data, safe=False)


class QuestionAPI(APIView):

    def get(self, *atgs, **kwargs):
        sub_stage_id = self.kwargs.get("sub_stage_id")
        if sub_stage_id:
            question = Question.objects.filter(sub_stage=sub_stage_id).prefetch_related(
                "answers"
            )
            if not question:
                return JsonResponse({"message": "Questions and answers not found!"})
            serializer = QuestionSerializer(question, many=True)
        else:
            question = Question.objects.prefetch_related("answers")
            serializer = QuestionSerializer(question, many=True)

        return JsonResponse(serializer.data, safe=False)


class AnswerAPI(APIView):

    def get(self, *args, **kwargs):
        answers = Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)

        print(serializer)

        return JsonResponse(serializer.data, safe=False)


class FormResultAPI(APIView):

    def get(self, *args, **kwargs):
        form = FormResult.objects.prefetch_related(
            "form_stages__form_sub_stages__form_questions__form_answers"
        )
        serializer = FormSerializer(form, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):

        def is_valid_value(value):
            pattern = r"^[\w\s.,?()-]+$"
            return bool(re.match(pattern, str(value)))

        def validate_json(data, key):
            if not data.get(key) or not is_valid_value(data.get(key)):
                if not is_valid_value(data.get(key)):
                    return {"message": f"Invalid value in {data.get(key)}"}
                return {"message": f"Invalid key, change to '{key}'"}

        data = request.data

        form_results = [FormResult()]
        form_stages = []
        form_sub_stages = []
        form_questions = []
        form_answers = []

        for stage_data in data:
            if validate_json(stage_data, "title"):
                return JsonResponse({"message": validate_json(stage_data, "title")})

            form_stage = FormStage(
                title=stage_data["title"], form_result=form_results[0]
            )
            form_stages.append(form_stage)

            for sub_stage_data in stage_data["sub_stages"]:
                if validate_json(sub_stage_data, "title"):
                    return JsonResponse(
                        {"message": validate_json(sub_stage_data, "title")}
                    )

                form_sub_stage = FormSubStage(
                    title=sub_stage_data["title"], form=form_stage
                )
                form_sub_stages.append(form_sub_stage)

                for question_data in sub_stage_data["questions"]:
                    if validate_json(question_data, "question"):
                        return JsonResponse(
                            {"message": validate_json(question_data, "question")}
                        )

                    form_question = FormQuestion(
                        question=question_data["question"],
                        form_sub_stage=form_sub_stage,
                    )
                    form_questions.append(form_question)

                    for answer in question_data["answers"]:
                        if validate_json(answer, "answer"):
                            return JsonResponse(validate_json(answer, "answer"))

                        form_answer = FormAnswer(
                            answer=answer["answer"], form_question=form_question
                        )
                        form_answers.append(form_answer)

        with transaction.atomic():
            FormResult.objects.bulk_create(form_results)
            FormStage.objects.bulk_create(form_stages)
            FormSubStage.objects.bulk_create(form_sub_stages)
            FormQuestion.objects.bulk_create(form_questions)
            FormAnswer.objects.bulk_create(form_answers)

        return JsonResponse({"message": "Form data saved successfully."}, safe=False)
