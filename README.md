Smart Exam Evaluator - Django Starter
------------------------------------
This project is a minimal starter for a Smart Exam Evaluator system that:
- Lets students upload scanned answer pages (images).
- Uses pytesseract (Tesseract OCR) to extract text.
- Saves OCR text as a Submission record.
- Provides a teacher view where the teacher can review OCR text, download the uploaded image, and enter marks/feedback.

Setup (local):
1. Install system Tesseract (required):
   - Ubuntu: sudo apt install tesseract-ocr libtesseract-dev
   - Windows: install Tesseract and add to PATH
2. Create virtualenv and install python deps:
   python -m venv venv
   source venv/bin/activate   (or venv\Scripts\activate on Windows)
   pip install -r requirements.txtfjkjdl
3. Run migrations and start server:
   python manage.py migrate
   python manage.py createsuperuser   # to use admin / teacher account
   python manage.py runserver
4. Open http://127.0.0.1:8000/ to access upload page and teacher views.

Notes:
- This is a starter scaffold. Improve OCR preprocessing, PDF support, layout mapping and authentication as needed.
