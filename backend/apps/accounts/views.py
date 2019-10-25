from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


def index(request):
    if request.method == "POST" and request.is_ajax():
        email = request.POST.get("email")
        print("POST via AJAX on index /w email:", email)
        return JsonResponse({"email": email}, status=200)

    # Default (for GET requests)
    return render(request, "index.html")
