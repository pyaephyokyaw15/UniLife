from django.urls import reverse


def home(request):
    return reverse("api:post-list")