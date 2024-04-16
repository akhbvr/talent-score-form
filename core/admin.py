from django.contrib import admin
from nested_admin import (
    NestedModelAdmin,
    NestedTabularInline
)
from django.template.loader import render_to_string
from django.utils.html import format_html
from nested_admin import NestedModelAdmin

from core.models import (
    Stage,
    SubStage,
    Question,
    Answer,

    FormStage,
    FormSubStage,
    FormQuestion,
    FormAnswer,
    FormResult
)


# ---------------------------- Data from the users --------------------------- #

class FormAnswerInline(NestedTabularInline):
    model = FormAnswer
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False


class FormQuestionInline(NestedTabularInline):
    model = FormQuestion
    inlines = [FormAnswerInline]
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False


class FormSubStageInline(NestedTabularInline):
    model = FormSubStage
    inlines = [FormQuestionInline]
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False


class FormStageInline(NestedTabularInline):
    model = FormStage
    inlines = [FormSubStageInline]
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(FormResult)
class FormResultAdmin(NestedModelAdmin):
    inlines = [FormStageInline]
    extra = 0
    def has_add_permission(self, request, obj=None):
        return False

# ---------------------------- Data from the users --------------------------- #



# ----------------------------- For administrator ---------------------------- #

class SubStageLine(admin.TabularInline):
    model = SubStage


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    inlines = [SubStageLine]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

# ----------------------------- For administrator ---------------------------- #
