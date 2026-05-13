from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.base import ContentFile


def generate_resume_pdf(generated_resume, context):

    html_string = render_to_string(
        "resumes/modern_resume.html",
        context
    )

    pdf_file = HTML(
        string=html_string
    ).write_pdf()

    generated_resume.file.save(
        f"resume_{generated_resume.id}.pdf",
        ContentFile(pdf_file)
    )

    return generated_resume.file.url 