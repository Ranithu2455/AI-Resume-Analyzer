from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from docx import Document
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_pdf_text(path):
    text = ""
    reader = PdfReader(path)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    return text


def extract_docx_text(path):
    doc = Document(path)

    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("resume")

    if not file or file.filename == "":
        return "No file selected."

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    if file.filename.lower().endswith(".pdf"):
        text = extract_pdf_text(filepath)
    elif file.filename.lower().endswith(".docx"):
        text = extract_docx_text(filepath)
    else:
        return "Only PDF and DOCX files are supported."

    score, sections = analyze_resume(text)
    feedback = generate_feedback(sections)


return render_template(
    "result.html",
    score=score,
    feedback=feedback
)



def analyze_resume(text):
    text = text.lower()

    score = 0

    sections = {
        "skills": False,
        "education": False,
        "experience": False,
        "projects": False
    }

    if "skills" in text:
        sections["skills"] = True
        score += 25

    if "education" in text:
        sections["education"] = True
        score += 25

    if "experience" in text:
        sections["experience"] = True
        score += 25

    if "project" in text or "projects" in text:
        sections["projects"] = True
        score += 25

    return score, sections

feedback = generate_feedback(sections)

if score >= 80:
    rating = "Excellent"
elif score >= 60:
    rating = "Good"
else:
    rating = "Needs Improvement"

return render_template(
    "result.html",
    score=score,
    rating=rating,
    feedback=feedback
)
