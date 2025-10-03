from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Submission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='submissions')
    student_name = models.CharField(max_length=200)
    uploaded_file = models.FileField(upload_to='uploads/')
    ocr_text = models.TextField(blank=True)
    marks_awarded = models.FloatField(null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.student_name} - {self.exam.title}"

class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} Certificate"

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class ExamPaper(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    exam_image = models.ImageField(upload_to='exam_papers/', blank=True, null=True)

    def _str_(self):
        return self.title

from django.utils import timezone

class AnswerKey(models.Model):
    exam_paper = models.ForeignKey(ExamPaper, on_delete=models.CASCADE, default=1)
    text_answer = models.TextField(blank=True, null=True)
    answer_image = models.ImageField(upload_to='answer_keys/', blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now) 

    def _str_(self):
        return f"AnswerKey for {self.exam_paper.title}"