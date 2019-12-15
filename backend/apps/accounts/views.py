from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


def index(request):
    if request.method == "POST" and request.is_ajax():
        email = request.POST.get("email")
        subject = "Aanmelding Mancelot"
        from_email = "info@mancelot.app"
        text_content = "Welkom bij Mancelot! We laten van ons horen zodra de app online is."
        html_content = render_to_string("accounts/signup.html")
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({"email": email}, status=200)

    # Default (for GET requests)
    return render(request, "index.html")


def tmp_signup_email(request):  # TODO: remove
    from django.contrib.auth import get_user_model
    timo = get_user_model().objects.filter(email="timo@halbesma.com").first()
    return render(request, "accounts/signup.html", {"user": timo})
