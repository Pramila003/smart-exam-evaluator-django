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
