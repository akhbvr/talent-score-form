from django.db import models
from uuid import uuid4


# ------------------------- Models for administrator ------------------------- #

class Stage(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(verbose_name="Stage name")

    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    def __str__(self):
        return self.title


class SubStage(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(verbose_name="Sub Stage name")
    parent_stage = models.ForeignKey(
        Stage,
        verbose_name="Stage",
        on_delete=models.CASCADE,
        related_name="stages",
    )

    class Meta:
        verbose_name = "Sub Stage"
        verbose_name_plural = "Sub Stages"

    def __str__(self):
        return f"{self.parent_stage.title} --> {self.title}"


class Question(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    QUESTION_TYPE_CHOICES = (
        ("text", "Text"),
        ("date", "Date"),
        ("number", "Number"),
        ("radio", "Radio"),
        ("tel", "Telephone"),
        ("option", "Option"),
    )
    question = models.CharField(verbose_name="Question")
    question_type = models.CharField(
        verbose_name="Question type",
        max_length=10,
        choices=QUESTION_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    hidden = models.BooleanField(verbose_name="Hide from forms", default=False)
    sub_stage = models.ForeignKey(
        SubStage,
        verbose_name="Sub Stage",
        on_delete=models.CASCADE,
        related_name="sub_stages",
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.sub_stage.title} --> {self.question} --> {self.question_type}"


class Answer(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    answer = models.CharField(verbose_name="Answer")
    question = models.ForeignKey(
        Question,
        verbose_name="Question",
        on_delete=models.CASCADE,
        related_name="questions",
    )

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.answer

# ------------------------- Models for administrator ------------------------- #



# ----------------------------- Models for users ----------------------------- #

class FormResult(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Form Result"
        verbose_name_plural = "Form Results"

    def __str__(self):
        return f"{self.created_at.strftime("%H:%M:%S | %d-%m-%Y") if self.created_at else 'None'}"


class FormStage(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Form stage title")
    form_result = models.ForeignKey(FormResult, on_delete=models.CASCADE, related_name="form_results")

    class Meta:
        verbose_name = "Form stage"
        verbose_name_plural = "Form stages"

    def __str__(self):
        return self.title


class FormSubStage(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Form sub stage title")
    form = models.ForeignKey(FormStage, on_delete=models.CASCADE, related_name="form_stages")

    class Meta:
        verbose_name = "Form sub stage"
        verbose_name_plural = "Form sub stages"

    def __str__(self):
        return self.title


class FormQuestion(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    question = models.CharField(max_length=255, verbose_name="Question")
    form_sub_stage = models.ForeignKey(FormSubStage, on_delete=models.CASCADE, related_name="form_sub_stage")

    class Meta:
        verbose_name = "Form question"
        verbose_name_plural = "Form questions"

    def __str__(self):
        return self.question


class FormAnswer(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    answer = models.CharField(max_length=255, verbose_name="Answer")
    form_question = models.ForeignKey(FormQuestion, on_delete=models.CASCADE, related_name="form_questions")

    class Meta:
        verbose_name = "Form answer"
        verbose_name_plural = "Form answers"

    def __str__(self):
        return self.answer

# ----------------------------- Models for users ----------------------------- #
