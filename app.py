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
    file = request.files["resume"]

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        if file.filename.endswith(".pdf"):
            text = extract_pdf_text(filepath)
            return text[:1000]

        elif file.filename.endswith(".docx"):
            text = extract_docx_text(filepath)
            return text[:1000]

        return "Only PDF and DOCX files are supported."

    return "No file selected."


if __name__ == "__main__":
    app.run(debug=True)






def analyze_resume(text):
    text = text.lower()

    sections = {
        "skills": False,
        "education": False,
        "experience": False,
        "projects": False
    }

    if "skills" in text:
        sections["skills"] = True

    if "education" in text:
        sections["education"] = True

    if "experience" in text:
        sections["experience"] = True

    if "project" in text or "projects" in text:
        sections["projects"] = True

    return sections

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

def generate_feedback(sections):
    feedback = []

    for section, exists in sections.items():
        if exists:
            feedback.append(f"✓ {section.title()} section found")
        else:
            feedback.append(f"✗ {section.title()} section missing")

    return feedback
