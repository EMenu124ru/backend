from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

TEMPLATES = {
    "create": "courses/course_create.html",
    "attendance": "courses/course_attendance.html",
    "entered": "courses/entered_to_course.html",
}


def send_email(
    action,
    user,
    course=None,
):
    """Function for send email with html template."""
    context = {
        "app_label": settings.APP_LABEL,
    }
    html = get_template(TEMPLATES[action])

    context["course"] = course.name
    context["topics"] = (
        "<ul>"
        + "".join([f"<li>{topic.title}</li>" for topic in course.topics.all()])
        + "</ul>"
    )
    context["count_students"] = course.students.count()
    html_content = html.render(context)
    msg = EmailMultiAlternatives(
        subject=user.username,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
