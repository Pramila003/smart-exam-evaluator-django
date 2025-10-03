from django.contrib import admin
from .models import Exam, Submission, ExamPaper, AnswerKey

# Register Exam and Submission
admin.site.register(Exam)
admin.site.register(Submission)


# ExamPaper Admin
@admin.register(ExamPaper)
class ExamPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_at', 'exam_image')
    search_fields = ('title', 'subject')
    list_filter = ('subject', 'created_at')


# AnswerKey Admin
@admin.register(AnswerKey)
class AnswerKeyAdmin(admin.ModelAdmin):
    list_display = ('exam_paper', 'answer_image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    list_filter = ('uploaded_at',)