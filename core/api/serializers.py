from rest_framework import serializers
from core.models import (
        Stage,
        SubStage,
        Question,
        Answer,

        FormResult,
        FormStage,
        FormSubStage,
        FormQuestion,
        FormAnswer,
    )


# ------------------------- For all data serializers ------------------------- #

class StageAllDataSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = (
            'id',
            'title',
            'sub_stages'
        )

    def get_sub_stages(self, obj):
        serializer = SubStageForStageSerializer(obj.stages.all(), many=True)
        return serializer.data


class SubStageForStageSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = SubStage
        fields = (
            'title',
            'questions'
        )

    def get_questions(self, obj):
        serializer = QuestionSerializer(obj.sub_stages.all(), many=True)
        return serializer.data


# ------------------------- For all data serializers ------------------------- #



# -------------------------------- Serializers ------------------------------- #

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = (
            'id',
            'title',
        )


class SubStageSerializer(serializers.ModelSerializer):
    # parent_stage = StageSerializer()
    class Meta:
        model = SubStage
        fields = (
            'id',
            'title',
            # 'parent_stage'
        )


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'question_type',
            'hidden',
            'question',
            'answers'
        )
    def get_answers(self, obj):
        serializer = AnswerSerializer(obj.questions.all(), many=True)
        return serializer.data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'id',
            'answer',
            'question'
        )

# -------------------------------- Serializers ------------------------------- #

class FormSerializer(serializers.ModelSerializer):
    stages = serializers.SerializerMethodField()
    class Meta:
        model = FormResult
        fields = (
                'id',
                'created_at',
                'stages'
            )

    def get_stages(self, obj):
        serializer = StageForFormSerializer(obj.form_results.all(), many=True)
        return serializer.data


class StageForFormSerializer(serializers.ModelSerializer):
    sub_stages = serializers.SerializerMethodField()
    class Meta:
        model = FormStage
        fields = ('title', 'sub_stages')

    def get_sub_stages(self, obj):
        serializer = SubStageForFormSerializer(obj.form_stages.all(), many=True)
        return serializer.data


class SubStageForFormSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    class Meta:
        model = FormSubStage
        fields = (
            'title',
            'questions'
        )

    def get_questions(self, obj):
        serializer = QuestionForFormSerializer(obj.form_sub_stage.all(), many=True)
        return serializer.data


class QuestionForFormSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = FormQuestion
        fields = (
            'question',
            'answers'
        )

    def get_answers(self, obj):
        serializer = AnswerForFormSerializer(obj.form_questions.all(), many=True)
        return serializer.data


class AnswerForFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswer
        fields = (
            'answer',
        )


