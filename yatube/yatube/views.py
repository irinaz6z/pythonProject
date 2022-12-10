from django.shortcuts import render


def not_found(request, exception):
    template = '404_not_found.html'
    return render(request, template, status=404)
