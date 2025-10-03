from django import forms
from .models import Submission, StudyMaterial

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['exam', 'student_name', 'uploaded_file']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks_awarded', 'teacher_feedback']

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file']
from .models import Certificate
from django import forms

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_file']

# evaluator/forms.py
from django import forms
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
)

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
