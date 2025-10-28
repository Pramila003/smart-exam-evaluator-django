from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import SubmissionForm, ReviewForm
from .models import Submission, Exam
from .models import StudyMaterial
from .forms import StudyMaterialForm
from django.contrib.auth.decorators import login_required
import pytesseract
from PIL import Image
import io

# ------------------ Existing Views ------------------

def index(request):
    exams = Exam.objects.all()
    return render(request, 'index.html', {'exams': exams})

def upload_submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            sub = form.save(commit=False)
            # perform OCR
            f = request.FILES['uploaded_file']
            try:
                img = Image.open(f)
                text = pytesseract.image_to_string(img, lang='eng')
            except Exception as e:
                text = f'OCR error: {e}'
            sub.ocr_text = text
            sub.save()
            return redirect('submission_detail', submission_id=sub.id)
    else:
        form = SubmissionForm()
    return render(request, 'upload.html', {'form': form})

def submission_detail(request, submission_id):
    sub = get_object_or_404(Submission, pk=submission_id)
    return render(request, 'submission_detail.html', {'sub': sub})

@login_required
def teacher_dashboard(request):
    subs = Submission.objects.all().order_by('-created_at')
    return render(request, 'teacher_dashboard.html', {'subs': subs})

@login_required
def review_submission(request, submission_id):
    sub = get_object_or_404(Submission, pk=submission_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=sub)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = ReviewForm(instance=sub)
    return render(request, 'review.html', {'sub': sub, 'form': form})

# ------------------ New Signup View ------------------

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup(request):
    app_name = "Smart Exam Evaluator"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = form.cleaned_data['role']
            login(request, user)

            if role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'hide_nav': True, 'app_name': app_name})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    app_name = "Smart Exam Evaluator"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect based on role
            role = getattr(user, 'role', None)  # assuming role is stored on user
            if role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('index')  # fallback
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'hide_nav': True, 'app_name': app_name})



# Teacher upload study material
@login_required
def upload_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_material')
    else:
        form = StudyMaterialForm()

    materials = StudyMaterial.objects.all().order_by('-uploaded_at')
    return render(request, 'upload_material.html', {'form': form, 'materials': materials})

# Student dashboard - view study material
@login_required
def student_dashboard(request):
    materials = StudyMaterial.objects.all().order_by('-uploaded_at')
    return render(request, 'student_dashboard.html', {'materials': materials})



@login_required
def delete_material(request, material_id):
    material = get_object_or_404(StudyMaterial, pk=material_id)
    if request.method == 'POST':
        # Delete the file from storage
        material.file.delete(save=False)
        # Delete the database record
        material.delete()
    return redirect('upload_material')

from django.shortcuts import render, redirect
from .forms import CertificateForm

@login_required
def upload_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.student = request.user
            cert.save()
            return redirect('student_dashboard')
    else:
        form = CertificateForm()
    
    return render(request, 'upload_certificate.html', {'form': form})


# views.py
from django.shortcuts import render, get_object_or_404
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
from .models import Submission, AnswerKey, ExamPaper

def evaluate_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    # --- Step 1: OCR extract ---
    if submission.answer_sheet:
        try:
            image = Image.open(submission.answer_sheet.path)
            student_text = pytesseract.image_to_string(image)
            submission.extracted_text = student_text
        except Exception as e:
            submission.extracted_text = f"OCR failed: {e}"
    else:
        submission.extracted_text = "No file uploaded."

    # --- Step 2: Fetch AnswerKey ---
    # Get the exam paper linked to this submission
    exam_paper = ExamPaper.objects.filter(id=submission.exam.id).first()
    if exam_paper and exam_paper.answerkey_set.exists():
        answer_key = exam_paper.answerkey_set.first()
        correct_answer = answer_key.text_answer or ""
    else:
        correct_answer = ""

    # --- Step 3: Compare similarity ---
    similarity = SequenceMatcher(None, submission.extracted_text, correct_answer).ratio()
    submission.similarity_score = round(similarity * 100, 2)  # %

    # --- Step 4: Calculate marks ---
    max_marks = 100  # you can customize per exam
    submission.marks_awarded = round(max_marks * similarity, 2)

    # --- Step 5: Save submission ---
    submission.save()

    # --- Step 6: Render result page ---
    return render(request, "result.html", {"student": submission})