from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import uuid


def generate_resume_pdf(generated_resume, context):

    html_string = render_to_string(
        "resumes/modern_resume.html",
        context
    )

    pdf_file = HTML(
        string=html_string
    ).write_pdf()

    filename = f"{uuid.uuid4()}.pdf"

    generated_resume.file.save(
        filename,
        ContentFile(pdf_file)
    )

    return generated_resume.file.url
     