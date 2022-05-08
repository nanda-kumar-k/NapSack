from django.contrib import messages


def my_view(request):
    messages.add_message(request, 50, 'A serious error occurred.')