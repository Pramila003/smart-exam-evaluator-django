from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('index/', views.index, name='index'),

    path('upload/', views.upload_submission, name='upload'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),

    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/review/<int:submission_id>/', views.review_submission, name='review_submission'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),   # ✅ also student dashboard
    path('teacher/upload_material/', views.upload_material, name='upload_material'),
    path('teacher/delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
    path('student/upload_certificate/', views.upload_certificate, name='upload_certificate'),

]
